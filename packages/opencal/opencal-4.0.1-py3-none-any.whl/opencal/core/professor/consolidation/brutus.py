"""Brutus pick all cards. For each right answer, the card is removed.
This teacher is only used for the in the ForwardTest tab.
"""

from collections.abc import Callable
import datetime
import logging
import sqlmodel
from uuid import uuid4

from opencal.card import Card
from opencal.core.professor.professor import AbstractProfessor, utcnow
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR
from opencal.io.database import engine
from opencal.models import ConsolidationReview


class ProfessorBrutus(AbstractProfessor):

    def __init__(
        self,
        card_list: list[Card],
        current_datetime_fn: Callable[[], datetime.datetime] = utcnow,
    ):
        super().__init__(current_datetime_fn=current_datetime_fn)

        self.update_card_list(card_list)

    @property
    def current_card(self):
        return self._card_list[0] if len(self._card_list) > 0 else None

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

        if len(self._card_list) > 0:
            card: Card = self._card_list.pop(0)

            if answer == RIGHT_ANSWER_STR:

                with sqlmodel.Session(engine) as session:
                    review = ConsolidationReview(
                        uuid=uuid4(),
                        card_uuid=card.uuid,
                        review_datetime_utc=self.current_datetime_fn(),
                        is_right_answer=True,
                        user_response_time_ms=user_response_time_ms
                    )
                    # card.consolidation_reviews.append(review)             # TODO: REMOVE THIS (DON'T KEEP THE REVIEWS IN MEMORY)

                    session.add(review)
                    session.commit()

            elif answer == WRONG_ANSWER_STR:

                with sqlmodel.Session(engine) as session:
                    review = ConsolidationReview(
                        uuid=uuid4(),
                        card_uuid=card.uuid,
                        review_datetime_utc=self.current_datetime_fn(),
                        is_right_answer=False,
                        user_response_time_ms=user_response_time_ms
                    )
                    # card.consolidation_reviews.append(review)             # TODO: REMOVE THIS (DON'T KEEP THE REVIEWS IN MEMORY)

                    session.add(review)
                    session.commit()

            elif answer == "skip":
                pass
            elif answer == "skip level":
                pass
            else:
                raise ValueError(f"Unknown answer : {answer}")

            if hide:
                card.is_hidden = True

            self.notify_observers_of_reply()

    def update_card_list(
        self,
        card_list: list[Card],
        review_hidden_cards: bool = False,
    ):
        self._card_list = [
            card for card in card_list if ((not card.is_hidden) or review_hidden_cards)
        ]
        # self.notify_observers()

    @property
    def remaining_cards(self):
        return len(self._card_list)
