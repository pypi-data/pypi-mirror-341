"""Doreen is the fourth *consolidation professor*, implemented for long-term memory training in OpenCAL.

Doreen est similaire à Celia excepté que chaque niveau peut être triés selon des critères différents."""

from collections.abc import Callable
from dataclasses import dataclass
import datetime
import logging
import json
import math
import sqlmodel
from typing import Any
from uuid import UUID, uuid4
import warnings

from opencal.card import Card
from opencal.core.professor.professor import utcnow
from opencal.core.professor.consolidation.professor import AbstractConsolidationProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR
from opencal.io.database import engine
from opencal.models import ConsolidationReview

GRADE_DONT_REVIEW_THIS_CARD_TODAY: int = -1
GRADE_REVIEWED_TODAY_WITH_RIGHT_ANSWER: int = -2

DEFAULT_MAX_CARDS_PER_GRADE: int = 5

DEFAULT_PRIORITY: float = 1.0
DEFAULT_DIFFICULTY: float = 1.0

VERBOSE: bool = True


# TODO: use pydantic.BaseModel instead?
# @dataclass
class ReviewData(sqlmodel.SQLModel, table=False):
    review_date: datetime.date
    is_right_answer: bool

# # @dataclass
# class CardData(sqlmodel.SQLModel, table=False):
#     uuid: UUID
#     reviews: list[ReviewData]
#     grade: int
#     priority: float
#     difficulty: float
#     tags: list[str]
#     is_hidden: bool
#     creation_datetime: datetime.datetime


class ProfessorDoreen(AbstractConsolidationProfessor):

    def __init__(
        self,
        card_list: list[Card],
        max_cards_per_grade: int = DEFAULT_MAX_CARDS_PER_GRADE,
        tag_priorities: dict[str, float] | None = None,
        tag_difficulties: dict[str, float] | None = None,
        priorities_per_level: dict[int | str, list[dict[str, Any]]] | None = None,
        current_datetime_fn: Callable[[], datetime.datetime] = utcnow,
    ):
        super().__init__(current_datetime_fn=current_datetime_fn)

        self.current_sub_list: list[Card] | None = None

        self.max_cards_per_grade = max_cards_per_grade
        self.tag_priority_dict = tag_priorities if tag_priorities is not None else {}
        self.tag_difficulty_dict = tag_difficulties if tag_difficulties is not None else {}
        self.priorities_per_level = priorities_per_level

        if self.priorities_per_level is None:
            self.priorities_per_level = {
                0: [
                    {"sort_fn": "tag", "reverse": True},
                    {"sort_fn": "date", "reverse": True},
                ],
                "default": [{"sort_fn": "tag", "reverse": True}],
            }

        if VERBOSE:
            logging.info("Professor Doreen")
            logging.info(f"max_cards_per_grade = {self.max_cards_per_grade}")
            logging.info(f"tag_priority_dict = {self.tag_priority_dict}")
            logging.info(f"tag_difficulty_dict = {self.tag_difficulty_dict}")
            logging.info(f"priorities_per_level = {self.priorities_per_level}")

        with open("/tmp/doreen_priorities_per_level_nuc.json", "w") as fd:                # <-
            priorities_per_level_dict = {str(k): v for k, v in self.priorities_per_level.items()} # <-
            json.dump(priorities_per_level_dict, fd, sort_keys=True, indent=4, default=str)   # <-

        self._card_list_dict: dict[int, list[Card]] = {}
        self.num_right_answers_per_grade: dict[int, float] = {}  # key: grade, value: sum of "difficulties"
        self.num_wrong_answers = 0  # TODO: BUG -> doesn't take into account wrong answers from previous executions...

        # Set card's grade and card's difficulty
        # Initialize and update self.num_right_answers_per_grade
        # Initialize and update self._card_list_dict
        score_dict: dict[str, int] = {} # <-

        card_dict: dict[UUID, list[ReviewData]] = get_card_dict()

        for card in card_list:
            if not card.is_hidden:
                card.consolidation_reviews = card_dict.get(card.uuid, [])   # TODO: temporary workaround for the SQLModel refactoring

                # Set card's grade
                grade = self.assess(card)
                score_dict[str(card.uuid)] = grade # <-
                card.grade = grade

                # Estimate the priority of each card
                card.priority = estimate_card_priority(card, self.tag_priority_dict)

                # Set card's difficulty
                card.difficulty = estimate_card_difficulty(
                    card, self.tag_difficulty_dict
                )

                # Initialize and update self.num_right_answers_per_grade
                if grade == GRADE_REVIEWED_TODAY_WITH_RIGHT_ANSWER:

                    grade_without_today_answers = self.assess(card, ignore_today_answers=True)

                    if (
                        grade_without_today_answers
                        not in self.num_right_answers_per_grade
                    ):
                        self.num_right_answers_per_grade[
                            grade_without_today_answers
                        ] = 0
                    self.num_right_answers_per_grade[
                        grade_without_today_answers
                    ] += card.difficulty

                elif grade != GRADE_DONT_REVIEW_THIS_CARD_TODAY:

                    # Initialize and update self._card_list_dict
                    if grade not in self._card_list_dict:
                        self._card_list_dict[grade] = []
                    self._card_list_dict[grade].append(card)

                    # Initialize self.num_right_answers_per_grade
                    if grade not in self.num_right_answers_per_grade:
                        self.num_right_answers_per_grade[grade] = 0

        with open("/tmp/doreen_score_dict_nuc.json", "w") as fd:             # <-
            json.dump(score_dict, fd, sort_keys=True, indent=4, default=str) # <-

        with open("/tmp/doreen_card_list_per_level_nuc.json", "w") as fd:    # <-
            card_list_per_level_dict = {str(k): [str(card.uuid) for card in v] for k, v in self._card_list_dict.items()} # <-
            json.dump(card_list_per_level_dict, fd, sort_keys=True, indent=4, default=str) # <-

        self._switch_grade_loop()


    def _switch_grade_loop(self):
        # TODO: smelly code...
        self._switch_grade()

        while (self.current_grade is not None) and (
            self.num_right_answers_per_grade[self.current_grade]
            >= self.max_cards_per_grade
        ):
            self._switch_grade()

    def _switch_grade(self):
        if len(self._card_list_dict) > 0:
            self.current_grade = sorted(self._card_list_dict.keys())[0]
            self.current_sub_list = self._card_list_dict.pop(
                self.current_grade
            )  # rem: this remove current_grade from _card_list_dict

            # Sort the current sub_list
            sort_sub_list(
                self.current_sub_list,
                self.current_grade,
                self.tag_priority_dict,
                self.priorities_per_level,
            )
        else:
            self.current_grade = None
            self.current_sub_list = None

    @property
    def current_card(self):
        if VERBOSE:
            self._print_number_of_cards_to_review_per_grade()

        # Switch to the next grade if the card sub list of the current grade is empty
        # or if the current grade's quotas has been reached
        if self.current_sub_list is not None:
            if (
                len(self.current_sub_list) == 0
                or self.num_right_answers_per_grade[self.current_grade]
                >= self.max_cards_per_grade
            ):
                self._switch_grade_loop()

        return self.current_sub_list[0] if self.current_sub_list is not None else None

    def _print_number_of_cards_to_review_per_grade(self):
        for k, v in sorted(
            self.num_right_answers_per_grade.items(), key=lambda item: item[0]
        ):
            if k == self.current_grade:
                num_cards = len(self.current_sub_list)
            else:
                num_cards = len(self._card_list_dict.get(k, []))
            print(
                f"{k}: {v:0.1f} / {self.max_cards_per_grade} ({num_cards if num_cards > 0 else '-'})"
            )
        print("Number of wrong answers:", self.num_wrong_answers)
        print("---")

    def current_card_reply(
        self,
        answer: str,
        hide: bool = False,
        user_response_time_ms: int | None = None,
        confidence: float | None = None,
    ) -> None:
        """
        Handle the reply to the current card.

        Parameters
        ----------
        answer : str
            The answer provided by the user.
        hide : bool, optional
            Whether to hide the card after the reply (default is False).
        user_response_time_ms : int|None, optional
            The time taken by the user to respond, in milliseconds (default is None).
        confidence : float|None, optional
            The confidence level of the user's answer (default is None).

        Returns
        -------
        None
            This function does not return any value.
        """
        assert self.current_sub_list is not None

        if len(self.current_sub_list) > 0:
            card: Card = self.current_sub_list.pop(0)

            if answer == RIGHT_ANSWER_STR:

                with sqlmodel.Session(engine) as session:
                    review = ConsolidationReview(
                        uuid=uuid4(),
                        card_uuid=card.uuid,
                        review_datetime_utc=self.current_datetime_fn(),
                        is_right_answer=True,
                        user_response_time_ms=user_response_time_ms,
                    )
                    # card.consolidation_reviews.append(review)
                    self.num_right_answers_per_grade[self.current_grade] += card.difficulty

                    session.add(review)
                    session.commit()

            elif answer == WRONG_ANSWER_STR:

                with sqlmodel.Session(engine) as session:
                    review = ConsolidationReview(
                        uuid=uuid4(),
                        card_uuid=card.uuid,
                        review_datetime_utc=self.current_datetime_fn(),
                        is_right_answer=False,
                        user_response_time_ms=user_response_time_ms,
                    )
                    # card.consolidation_reviews.append(review)
                    self.num_wrong_answers += 1

                    session.add(review)
                    session.commit()

            elif answer == "skip":
                pass
            elif answer == "skip level":
                self.current_sub_list = []
            else:
                raise ValueError(f"Unknown answer : {answer}")

            if hide:
                card.is_hidden = True

    def assess(
        self,
        card: Card,
        ignore_today_answers: bool = False,
    ):
        return assess(card, ignore_today_answers, self.current_datetime_fn)


def datetime_to_date(d: datetime.datetime | datetime.date) -> datetime.date:
    """If the object is an instance of datetime.datetime then convert it to a datetime.datetime.date object.

    If it's already a date object, do nothing."""

    if isinstance(d, datetime.datetime):
        # Convert the utc datetime to a local datetime
        d = d.astimezone().replace(tzinfo=None)

        # Convert the datetime to a date
        d = d.date()

    return d


def get_card_dict() -> dict[UUID, list[ReviewData]]:
    card_dict: dict[UUID, list[ReviewData]] = {}

    # Get reviews with SQLModel
    with sqlmodel.Session(engine) as session:
        statement = sqlmodel.select(ConsolidationReview).order_by(sqlmodel.col(ConsolidationReview.review_datetime_utc).asc())
        reviews = session.exec(statement)

        for review_model in reviews:
            card_uuid = review_model.card_uuid

            if card_uuid not in card_dict:
                card_dict[card_uuid] = []

            review = ReviewData(
                review_date = datetime_to_date(review_model.review_datetime_utc),
                is_right_answer = review_model.is_right_answer
            )

            card_dict[card_uuid].append(review)

    return card_dict


def assess(
    card: Card,
    ignore_today_answers: bool = False,
    current_datetime_fn: Callable[[], datetime.datetime] = utcnow,
):
    grade: int = 0
    cdate: datetime.date = datetime_to_date(card.creation_datetime)
    today: datetime.date = datetime_to_date(current_datetime_fn())

    if ignore_today_answers:
        review_list = [
            review
            for review in card.consolidation_reviews
            if review.review_date < today
        ]
    else:
        review_list = card.consolidation_reviews

    if len(review_list) > 0:
        # Reviews are supposed to be sorted!
        assert all(
            review_list[i].review_date <= review_list[i + 1].review_date
            for i in range(len(review_list) - 1)
        )
        # review_list.sort(key=lambda x: x.review_date)

        yesterday = today - datetime.timedelta(days=1)
        last_review_is_right_answer = review_list[-1].is_right_answer
        last_review_rdate = review_list[-1].review_date

        if last_review_rdate == today and last_review_is_right_answer:
            grade = GRADE_REVIEWED_TODAY_WITH_RIGHT_ANSWER
        else:
            expected_revision_date = get_expected_revision_date(cdate, grade)

            for review in review_list:
                rdate = review.review_date
                is_right_answer = review.is_right_answer

                if rdate <= today:  # Ignore future reviews
                    if is_right_answer:
                        if rdate >= expected_revision_date:  # "rdate before expected_revision_date"
                            grade += 1
                            expected_revision_date = get_expected_revision_date(rdate, grade)
                    else:
                        grade = 0
                        expected_revision_date = get_expected_revision_date(rdate, grade)
                else:
                    logging.warning(f"Review {review.uuid} of card {card.uuid} is defined with a future date!")

            if expected_revision_date > today:  # "today before expected_revision_date"
                # It's too early to review this card. The card will be hide
                grade = GRADE_DONT_REVIEW_THIS_CARD_TODAY
    else:
        expected_revision_date = get_expected_revision_date(cdate, grade)

        if expected_revision_date > today:
            grade = GRADE_DONT_REVIEW_THIS_CARD_TODAY

    return grade


def get_expected_revision_date(last_revision_date, grade: int):
    """Get the expected (next) revision date knowing the last revision date and the grade."""
    return last_revision_date + datetime.timedelta(days=delta_days(grade))


def delta_days(grade: int):
    """Return the delta day (time between expectedRevisionDate and rdate) knowing the grade.

    delta = 2^grade.
    """
    return int(math.pow(2, grade))


def estimate_card_priority(card: Card, tag_priority_dict: dict[str, float]):
    # TODO: estimate the priority of each card... -> utilise deux liste de liste tags definie dans le fichier de config .yaml :$
    # prof_doreen = [['maths', 'algebre', ...], ['accenta'], ['important', 'high priority', ...], ...] ;
    # prof_berebice_low_priority_tags = [[...], ...] -> chaque sous liste est un ensemble de tags équivalant ;
    # chaque tag ds high priority => card priority += 1 ; chaque tag dans low_prio_list => card priority -= 1

    tag_priority_list = [
        tag_priority_dict.get(tag, DEFAULT_PRIORITY) for tag in card.tags
    ]

    if len(tag_priority_list) == 0:
        card_priority = DEFAULT_PRIORITY
    else:
        if min(tag_priority_list) < 0:
            card_priority = min(tag_priority_list)
        else:
            card_priority = max(
                tag_priority_list
            )  # Each tag = one priority value => take the max

    return card_priority


def estimate_card_difficulty(card: Card, tag_difficulty_dict: dict[str, float]) -> float:
    # TODO: tags (+ maybe rate of right answer and avg response time)

    tag_difficulty_list = []

    for tag in card.tags:
        if tag in tag_difficulty_dict:
            tag_difficulty_list.append(tag_difficulty_dict[tag])

    if len(tag_difficulty_list) == 0:
        card_difficulty = DEFAULT_DIFFICULTY
    else:
        card_difficulty = max(
            tag_difficulty_list
        )  # Each tag = one difficulty value => take the max

    return card_difficulty


def sort_sub_list(
    sub_list: list[Card],
    sub_list_grade: int,
    tag_priority_dict,
    priorities_per_level: dict[int | str, list[dict[str, Any]]],
):
    """Une "sub_list" est un liste de cartes où toutes les cartes ont le même "grade"

    mis dans une fonction à part pour pouvoir être testé plus facilement dans des tests unitaires
    """
    if sub_list_grade not in priorities_per_level.keys():
        sub_list_grade = "default"

    priority_list = priorities_per_level[sub_list_grade]

    for priority_dict in priority_list:
        if priority_dict["sort_fn"] == "tag":
            sort_fn = lambda _card: _card.priority
        elif priority_dict["sort_fn"] == "date":
            # sort_fn = get_last_review_date_of_card
            sort_fn = lambda _card: max(
                [_card.creation_datetime.date()]
                + [review.review_date for review in _card.consolidation_reviews]
            )
        else:
            raise Exception(
                f'Unknown sort function {priority_dict["sort_fn"]}; available functions are: "tag" or "date"'
            )

        sub_list.sort(key=sort_fn, reverse=priority_dict["reverse"])


# def get_last_review_date_of_card(card: Card) -> datetime.date:
#     # Retrieve the last review date of the card
#     with sqlmodel.Session(engine) as session:
#         statement = sqlmodel.select(ConsolidationReview).where(ConsolidationReview.card_uuid == card.uuid).order_by(ConsolidationReview.review_datetime_utc.asc())
#         results = session.exec(statement)
#         review_list = results.all()

#         if len(review_list) > 0:
#             last_review_date = datetime_to_date(review_list[-1].review_datetime_utc)
#         else:
#             last_review_date = datetime_to_date(card.creation_datetime)

#     return last_review_date


# if __name__ == "__main__":
#     print(get_card_dict())
