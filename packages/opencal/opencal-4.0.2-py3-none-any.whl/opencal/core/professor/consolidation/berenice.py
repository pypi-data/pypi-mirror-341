"""Berenice is the second *consolidation professor*, implemented for long-term memory training in OpenCAL."""

import datetime
import math

from typing import Optional, Union

from opencal.core.professor.consolidation.professor import AbstractConsolidationProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR
from typing import Optional

GRADE_CARD_NEVER_REVIEWED = -1
GRADE_CARD_WRONG_YESTERDAY = -2
GRADE_DONT_REVIEW_THIS_CARD_TODAY = -3
GRADE_REVIEWED_TODAY_WITH_RIGHT_ANSWER = -4

DEFAULT_MAX_CARDS_PER_GRADE = 5

DEFAULT_PRIORITY = 1.
DEFAULT_DIFFICULTY = 1.

VERBOSE = True

class ProfessorBerenice(AbstractConsolidationProfessor):

    def __init__(self,
                 card_list: list,
                 date_mock: Optional[datetime.date] = None,
                 max_cards_per_grade: int = DEFAULT_MAX_CARDS_PER_GRADE,
                 tag_priorities: Optional[dict] = None,
                 tag_difficulties: Optional[dict] = None,
                 reverse_level_0: bool = False):
        super().__init__()

        self.max_cards_per_grade = max_cards_per_grade
        self.tag_priority_dict = tag_priorities if tag_priorities is not None else {}
        self.tag_difficulty_dict = tag_difficulties if tag_difficulties is not None else {}

        if VERBOSE:
            print("Professor Berenice")
            print("max_cards_per_grade =", self.max_cards_per_grade)
            print("tag_priority_dict =", self.tag_priority_dict)
            print("tag_difficulty_dict =", self.tag_difficulty_dict)

        self._card_list_dict = {}
        self.num_right_answers_per_grade = {}
        self.num_wrong_answers = 0             # TODO: BUG -> doesn't take into account wrong answers from previous executions...

        if date_mock is None:
            self._date = datetime.date
        else:
            self._date = date_mock

        for card in card_list:
            if not card["hidden"]:
                grade = assess(card, date_mock=date_mock)
                card["grade"] = grade

                card["difficulty"] = estimate_card_difficulty(card, self.tag_difficulty_dict)

                if grade == GRADE_REVIEWED_TODAY_WITH_RIGHT_ANSWER:

                    grade_without_today_answers = assess(card, date_mock=date_mock, ignore_today_answers=True)

                    if grade_without_today_answers in (GRADE_CARD_NEVER_REVIEWED, GRADE_CARD_WRONG_YESTERDAY): 
                        grade_without_today_answers = 0

                    if grade_without_today_answers not in self.num_right_answers_per_grade:
                        self.num_right_answers_per_grade[grade_without_today_answers] = 0
                    self.num_right_answers_per_grade[grade_without_today_answers] += card["difficulty"]

                elif grade != GRADE_DONT_REVIEW_THIS_CARD_TODAY:

                    if grade in (GRADE_CARD_NEVER_REVIEWED, GRADE_CARD_WRONG_YESTERDAY): 
                        grade = 0

                    if grade not in self._card_list_dict:
                        self._card_list_dict[grade] = []
                    self._card_list_dict[grade].append(card)

                    if grade not in self.num_right_answers_per_grade:
                        self.num_right_answers_per_grade[grade] = 0

        # Another special rule for level 0
        if 0 in self._card_list_dict:
            # Sort level 0 cards by descending date
            if reverse_level_0:
                self._card_list_dict[0].sort(key=lambda item: item["cdate"], reverse=True)

            # Sort level 0 cards by ascending (actual) grade : GRADE_CARD_WRONG_YESTERDAY < GRADE_CARD_NEVER_REVIEWED < GRADE 0
            self._card_list_dict[0].sort(key=lambda item: item["grade"])

        self._switch_grade_loop()


    def _switch_grade_loop(self):
        # TODO: smelly code...
        self._switch_grade()

        while (self.current_grade is not None) and (self.num_right_answers_per_grade[self.current_grade] >= self.max_cards_per_grade):
            self._switch_grade()


    def _switch_grade(self):
        if len(self._card_list_dict.keys()) > 0:
            self.current_grade = sorted(self._card_list_dict.keys())[0]
            self.current_sub_list = self._card_list_dict.pop(self.current_grade)  # rem: this remove current_grade from _card_list_dict

            # Estimate the priority of each card
            for card in self.current_sub_list:
                card["priority"] = estimate_card_priority(card, self.tag_priority_dict)

            # Sort current_sub_list according to the priority level of each card
            self.current_sub_list.sort(key=lambda _card : _card["priority"], reverse=True)
        else:
            self.current_grade = None
            self.current_sub_list = None


    @property
    def current_card(self):
        if VERBOSE:
            for k, v in sorted(self.num_right_answers_per_grade.items(), key=lambda item: item[0]):
                if k == self.current_grade:
                    num_cards  = len(self.current_sub_list)
                else:
                    num_cards = len(self._card_list_dict.get(k, []))
                print(f"{k}: {v:0.1f} / {self.max_cards_per_grade} ({num_cards if num_cards > 0 else '-'})")
            print("Number of wrong answers:", self.num_wrong_answers)
            print("---")

        if self.current_sub_list is not None:
            if len(self.current_sub_list) == 0 or self.num_right_answers_per_grade[self.current_grade] >= self.max_cards_per_grade:
                self._switch_grade_loop()

        return self.current_sub_list[0] if self.current_sub_list is not None else None


    def current_card_reply(
            self,
            answer: str,
            hide: bool = False,
            user_response_time_ms: Optional[int] = None,
            confidence: Optional[float] = None
        ) -> None:
        """
        Handle the reply to the current card.

        Parameters
        ----------
        answer : str
            The answer provided by the user.
        hide : bool, optional
            Whether to hide the card after the reply (default is False).
        user_response_time_ms : Optional[int], optional
            The time taken by the user to respond, in milliseconds (default is None).
        confidence : Optional[float], optional
            The confidence level of the user's answer (default is None).

        Returns
        -------
        None
            This function does not return any value.
        """

        if len(self.current_sub_list) > 0:
            card = self.current_sub_list.pop(0)

            if answer == RIGHT_ANSWER_STR:
                review = {
                    "rdate": self._date.today(),
                    "result": RIGHT_ANSWER_STR
                }
                card["reviews"].append(review)
                self.num_right_answers_per_grade[self.current_grade] += card["difficulty"]
            elif answer == WRONG_ANSWER_STR:
                review = {
                    "rdate": self._date.today(),
                    "result": WRONG_ANSWER_STR
                }
                card["reviews"].append(review)
                self.num_wrong_answers += 1
            elif answer == "skip":
                pass
            elif answer == "skip level":
                self.current_sub_list = []
            else:
                raise ValueError(f"Unknown answer : {answer}")

            if hide:
                card["hidden"] = True


def datetime_to_date(d: Union[datetime.datetime, datetime.date]) -> datetime.date:
    '''If the object is an instance of datetime.datetime then convert it to a datetime.datetime.date object.

    If it's already a date object, do nothing.'''

    if isinstance(d, datetime.datetime):
        d = d.date()

    return d


def assess(card, date_mock=None, ignore_today_answers=False):
    grade = 0

    cdate = datetime_to_date(card["cdate"])

    if date_mock is None:
        today = datetime.date.today()
    else:
        today = date_mock.today()

    if "reviews" in card.keys():
        if ignore_today_answers:
            review_list = [review for review in card["reviews"] if datetime_to_date(review["rdate"]) < today]
        else:
            review_list = card["reviews"]
    else:
        review_list = []

    if len(review_list) > 0:
        # Reviews are supposed to be sorted!
        assert all(review_list[i]["rdate"] <= review_list[i+1]["rdate"] for i in range(len(review_list)-1))
        #review_list.sort(key=lambda x: x["rdate"])

        yesterday = today - datetime.timedelta(days=1)
        last_review_result = review_list[-1]["result"]
        last_review_rdate = datetime_to_date(review_list[-1]["rdate"])

        if last_review_rdate == yesterday and last_review_result == WRONG_ANSWER_STR:
            grade = GRADE_CARD_WRONG_YESTERDAY
        elif last_review_rdate == today and last_review_result == RIGHT_ANSWER_STR:
            grade = GRADE_REVIEWED_TODAY_WITH_RIGHT_ANSWER
        else:
            expected_revision_date = get_expected_revision_date(cdate, grade)

            for review in review_list:
                rdate = datetime_to_date(review["rdate"])
                result = review["result"]

                if rdate <= today:                            # Ignore future reviews
                    if result == RIGHT_ANSWER_STR:
                        if rdate >= expected_revision_date:   # "rdate before expected_revision_date"
                            grade += 1
                            expected_revision_date = get_expected_revision_date(rdate, grade)
                    else:
                        grade = 0
                        expected_revision_date = get_expected_revision_date(rdate, grade)

            if expected_revision_date > today:            # "today before expected_revision_date"
                # It's too early to review this card. The card will be hide
                grade = GRADE_DONT_REVIEW_THIS_CARD_TODAY
    else:
        expected_revision_date = get_expected_revision_date(cdate, grade)

        if expected_revision_date > today:
            grade = GRADE_DONT_REVIEW_THIS_CARD_TODAY
        else:
            grade = GRADE_CARD_NEVER_REVIEWED

    return grade


def get_expected_revision_date(last_revision_date, grade):
    """Get the expected (next) revision date knowing the last revision date and the grade."""
    return last_revision_date + datetime.timedelta(days=delta_days(grade))

     
def delta_days(grade):
    """Return the delta day (time between expectedRevisionDate and rdate) knowing the grade.
    
    delta = 2^grade.
    """
    return int(math.pow(2, grade))


def estimate_card_priority(card, tag_priority_dict):
    # TODO: estimate the priority of each card... -> utilise deux liste de liste tags definie dans le fichier de config .yaml :$
    # prof_berenice_high_priority_tags = [['maths', 'algebre', ...], ['accenta'], ['important', 'high priority', ...], ...] ;
    # prof_berebice_low_priority_tags = [[...], ...] -> chaque sous liste est un ensemble de tags équivalant ;
    # chaque tag ds high priority => card priority += 1 ; chaque tag dans low_prio_list => card priority -= 1

    tag_priority_list = [tag_priority_dict.get(tag, DEFAULT_PRIORITY) for tag in card["tags"]]

    if len(tag_priority_list) == 0:
        card_priority = DEFAULT_PRIORITY
    else:
        if min(tag_priority_list) < 0:
            card_priority = min(tag_priority_list)
        else:
            card_priority = max(tag_priority_list) # Each tag = one priority value => take the max

    return card_priority


def estimate_card_difficulty(card, tag_difficulty_dict):
    # TODO: tags (+ maybe rate of right answer and avg response time)

    tag_difficulty_list = []

    for tag in card["tags"]:
        if tag in tag_difficulty_dict:
            tag_difficulty_list.append(tag_difficulty_dict[tag])

    if len(tag_difficulty_list) == 0:
        card_difficulty = DEFAULT_DIFFICULTY
    else:
        card_difficulty = max(tag_difficulty_list) # Each tag = one difficulty value => take the max

    return card_difficulty
