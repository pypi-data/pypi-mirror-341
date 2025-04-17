import logging
import sqlmodel
from uuid import uuid4

from opencal.card import Card
from opencal.core.professor.professor import AbstractProfessor
from opencal.io.database import engine
from opencal.models import AcquisitionReview
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR


class AbstractAcquisitionProfessor(AbstractProfessor):

    def current_card_reply(
        self,
        answer: str,
        hide: bool = False,
        user_response_time_ms: int | None = None,
        confidence: float | None = None,
    ):
        card: Card = self.current_card

        if answer == RIGHT_ANSWER_STR:

            review = AcquisitionReview(
                uuid=uuid4(),
                card_uuid=card.uuid,
                review_datetime_utc=self.current_datetime_fn(),
                is_right_answer=True,
                user_response_time_ms=user_response_time_ms,
            )

            with sqlmodel.Session(engine) as session:
                session.add(review)
                session.commit()

        elif answer == WRONG_ANSWER_STR:

            review = AcquisitionReview(
                uuid=uuid4(),
                card_uuid=card.uuid,
                review_datetime_utc=self.current_datetime_fn(),
                is_right_answer=False,
                user_response_time_ms=user_response_time_ms,
            )

            with sqlmodel.Session(engine) as session:
                session.add(review)
                session.commit()

        elif answer == "skip":
            logging.info(f"Skipping card")
        elif answer == "skip level":
            logging.info(f"Skipping level")
        else:
            raise ValueError(f"Unknown answer : {answer}")


    def update_card_list(
        self,
        card_list: list[Card],
        review_hidden_cards: bool = False
    ):
        raise NotImplementedError()

