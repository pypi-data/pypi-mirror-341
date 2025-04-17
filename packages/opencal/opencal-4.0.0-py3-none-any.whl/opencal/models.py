import datetime
from sqlalchemy import DateTime, func
from sqlmodel import Column, Field, Relationship, SQLModel
from uuid import UUID, uuid4

###############################################################################
# Card models                                                                 #
###############################################################################

# Define the Card model
class Card(SQLModel, table=True):
    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    # See https://github.com/fastapi/sqlmodel/issues/594#issuecomment-1575344153 and https://stackoverflow.com/a/71336392
    created_at_utc: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)    # Create a timezone-aware datetime object
    )
    # See https://github.com/fastapi/sqlmodel/issues/594#issuecomment-1578962030
    updated_at_utc: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
        # sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    question: str
    answer: str
    tags: str = ""                   # tags: list[str] = Field(default_factory=list) # TODO: str or list[str]?
    is_hidden: bool = False


# Define the CardUpdate model for partial updates
# See:
# - https://sqlmodel.tiangolo.com/tutorial/fastapi/update/
# - https://fastapi.tiangolo.com/tutorial/body-updates/
class CardUpdate(SQLModel):
    uuid: UUID | None = None
    question: str | None = None
    answer: str | None = None
    tags: str | None = None          # tags: list[str] | None = None # TODO: str or list[str]?
    is_hidden: bool | None = None


###############################################################################
# Review models                                                               #
###############################################################################

class AcquisitionReview(SQLModel, table=True):
    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    # card_uuid: UUID = Field(
    #     foreign_key="card.uuid"
    # )
    card_uuid: UUID = Field(index=True)
    # See https://github.com/fastapi/sqlmodel/issues/594#issuecomment-1575344153 and https://stackoverflow.com/a/71336392
    review_datetime_utc: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)    # Create a timezone-aware datetime object
    )
    is_right_answer: bool
    user_response_time_ms: int | None = None


class ConsolidationReview(SQLModel, table=True):
    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    # card_uuid: UUID = Field(
    #     foreign_key="card.uuid"
    # )
    card_uuid: UUID = Field(index=True)
    # See https://github.com/fastapi/sqlmodel/issues/594#issuecomment-1575344153 and https://stackoverflow.com/a/71336392
    review_datetime_utc: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)    # Create a timezone-aware datetime object
    )
    is_right_answer: bool
    user_response_time_ms: int | None = None

    # self.timedelta: datetime.timedelta | None = None  # TODO: IS THIS ATTRIBUTE REALLY USEFUL???
    # self.last_validated_timedelta: datetime.timedelta | None = None  # TODO: IS THIS ATTRIBUTE REALLY USEFUL???
