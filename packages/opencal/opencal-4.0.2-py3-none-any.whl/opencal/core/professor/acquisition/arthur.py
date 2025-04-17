"""Professor Arthur is used for knowledge acquisition (or "learning phase"), i.e. the initial stage when knowledge is introduced and learned.

Professor Arthur selects `max_num_active_cards` cards from the `remaining_cards_list` in order to create a subset of "active cards" (`active_cards_list`).
He then quizzes the user on each of these cards.
The number of correct and incorrect answers for each card is recorded in the `success_rate_dict`.

After each incorrect answer, the card is placed at the end of the `active_cards_list`.
When an answer is correct, the card’s success rate is checked.
If this rate is strictly higher than `success_rate_threshold`, it is removed from the `active_cards_list` and replaced by the first card from the `remaining_cards_list`.
Otherwise, the card is again placed at the end of the `active_cards_list`.
"""

from collections.abc import Callable
from dataclasses import dataclass
import datetime
import logging
import math
from uuid import UUID

from opencal.card import Card
from opencal.core.professor.professor import utcnow
from opencal.core.professor.acquisition.professor import AbstractAcquisitionProfessor
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR


DEFAULT_NUM_ACTIVE_CARDS: int = 5
SUCCESS_ANSWERS_RATE_THRESHOLD: float = 0.5

@dataclass
class ReviewsSuccessRate:
    """Class for keeping track of reviews."""
    num_right_answers: int = 0
    num_wrong_answers: int = 0

    def success_rate(self) -> float:
        """Calculate the success rate."""
        if self.num_right_answers + self.num_wrong_answers == 0:
            return float("nan")
        else:
            num_right_answers = float(self.num_right_answers)
            num_wrong_answers = float(self.num_wrong_answers)
            return num_right_answers / (num_right_answers + num_wrong_answers)


class ProfessorArthur(AbstractAcquisitionProfessor):

    def __init__(
        self,
        card_list: list[Card],
        max_num_active_cards: int = DEFAULT_NUM_ACTIVE_CARDS,
        success_rate_threshold: float = SUCCESS_ANSWERS_RATE_THRESHOLD,
        current_datetime_fn: Callable[[], datetime.datetime] = utcnow
    ):
        super().__init__(current_datetime_fn=current_datetime_fn)

        self.initial_card_list: list[Card] = []
        self.acquired_cards_list: list[Card] = []
        self.skipped_cards_list: list[Card] = []

        self.active_cards_list: list[Card] = []
        self.remaining_cards_list: list[Card] = []
        self.success_rate_dict: dict[UUID, ReviewsSuccessRate] = {}

        self.max_num_active_cards = max_num_active_cards
        self.success_rate_threshold = success_rate_threshold

        self.update_card_list(card_list)


    @property
    def current_card(self):
        if len(self.active_cards_list) > 0:
            return self.active_cards_list[0]
        else:
            # Review is completed
            print("Review completed")
            return None


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

        super().current_card_reply(answer, hide, user_response_time_ms, confidence)

        if self.current_card is not None:
            card = self.active_cards_list.pop(0)

            if answer == RIGHT_ANSWER_STR:
                self.success_rate_dict[card.uuid].num_right_answers += 1

                # If the answer is correct, check the success rate of the card
                if self.success_rate_dict[card.uuid].success_rate() > self.success_rate_threshold:
                    # The success rate is high enough, the card is "acquired". 
                    # It is then removed from the `active_cards_list` and replaced by a new card.
                    self.acquired_cards_list.append(card)

                    if len(self.remaining_cards_list) > 0:
                        new_card = self.remaining_cards_list.pop(0)
                        self.active_cards_list.append(new_card)
                        self.success_rate_dict[new_card.uuid] = ReviewsSuccessRate()
                else:
                    # The success rate is too low, the card is not "acquired" yet.
                    # It is then reintroduced in the `active_cards_list` to be reviewed again.
                    self.active_cards_list.append(card)

            elif answer == WRONG_ANSWER_STR:
                # If the answer is wrong, put the card back to the end of the `active_cards_list`
                self.success_rate_dict[card.uuid].num_wrong_answers += 1
                self.active_cards_list.append(card)

            elif answer == "skip":
                self.skipped_cards_list.append(card)

                # The card is not reintroduced in the `active_cards_list`, thus it is removed from the review session
                if len(self.remaining_cards_list) > 0:
                    new_card = self.remaining_cards_list.pop(0)
                    self.active_cards_list.append(new_card)
                    self.success_rate_dict[new_card.uuid] = ReviewsSuccessRate()

            else:
                raise ValueError(f"Unknown answer : {answer}")
        else:
            logging.warning("`current_card_reply` is called but `current_card` is `None`. There is a bug somewhere in the function that called `current_card_reply` (i.e. a missing check).")


    def update_card_list(
        self,
        card_list: list[Card],
        review_hidden_cards: bool = False
    ):
        self.initial_card_list = [card for card in card_list if ((not card.is_hidden) or review_hidden_cards)]
        self.acquired_cards_list = []
        self.skipped_cards_list = []

        self.remaining_cards_list = [card for card in self.initial_card_list]
        self.active_cards_list = []
        self.success_rate_dict = {}

        while (len(self.remaining_cards_list) > 0) and (len(self.active_cards_list) < self.max_num_active_cards):
            card = self.remaining_cards_list.pop(0)
            self.active_cards_list.append(card)
            self.success_rate_dict[card.uuid] = ReviewsSuccessRate()


    @property
    def feedback_msg(self) -> str:
        success_rate_list = []

        for card in self.active_cards_list:
            success_rate = self.success_rate_dict[card.uuid].success_rate()

            if math.isnan(success_rate):
                success_rate_list.append("-")
            else:
                success_rate_list.append(f"{success_rate:.2f}") 

        msg = (
            "Professor feedback: "
            f"{ len(self.active_cards_list) } active + {len(self.remaining_cards_list)} remaining / "
            f"{ len(self.initial_card_list) } total "
            f"({ len(self.acquired_cards_list) } acquired, { len(self.skipped_cards_list) } skipped) | "
            f"active cards success rate: [{ ','.join(success_rate_list) }]"
        )
        return msg