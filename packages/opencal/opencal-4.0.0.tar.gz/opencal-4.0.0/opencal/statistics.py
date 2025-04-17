import datetime
import pandas as pd
from sqlalchemy import func
import sqlmodel
from uuid import UUID

from opencal.card import Card
from opencal.io.database import engine
from opencal.models import AcquisitionReview, ConsolidationReview


TIME_DELTA_OF_FIRST_REVIEWS = datetime.timedelta()    # Null time delta (0 day). TODO?
INIT_VALIDATED_TIME_DELTA = datetime.timedelta()      # Null time delta (0 day). TODO?


def count_card_creation(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> int:
    raise NotImplementedError("This function is not yet implemented.") # TODO


def count_acquisition_reviews(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> int:
    """
    Count the number of acquisition reviews in the database between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until the latest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    int
        The number of acquisition reviews in the database within the specified date range.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    # Convert string dates to datetime.date if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    # Check if dates are in correct order when both are provided
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError(f"start_date ({start_date}) must be earlier than or equal to end_date ({end_date})")

    with sqlmodel.Session(engine) as session:
        query = sqlmodel.select(func.count()).select_from(AcquisitionReview)
        
        if start_date is not None:
            query = query.where(AcquisitionReview.review_datetime_utc >= start_date)
        if end_date is not None:
            query = query.where(AcquisitionReview.review_datetime_utc <= end_date)

        num_reviews = session.exec(query).one()

    return num_reviews


def count_consolidation_reviews(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> int:
    """
    Count the number of consolidation reviews in the database between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until the latest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    int
        The number of consolidation reviews in the database within the specified date range.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    # Convert string dates to datetime.date if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    # Check if dates are in correct order when both are provided
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError(f"start_date ({start_date}) must be earlier than or equal to end_date ({end_date})")

    with sqlmodel.Session(engine) as session:
        query = sqlmodel.select(func.count()).select_from(ConsolidationReview)
        
        if start_date is not None:
            query = query.where(ConsolidationReview.review_datetime_utc >= start_date)
        if end_date is not None:
            query = query.where(ConsolidationReview.review_datetime_utc <= end_date)

        num_reviews = session.exec(query).one()

    return num_reviews


def card_dataframe(
    card_list: list[Card],      # TODO: TEMPORARY WORKAROUND
    start_date: datetime.date | str | None = None, 
    end_date: datetime.date | str | None = None
) -> pd.DataFrame:
    """
    Generate a DataFrame that contains the card information between two dates.

    Parameters
    ----------
    card_list : list[Card]
        List of cards to process
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest card.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until the latest card.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    pandas.DataFrame
        A DataFrame that contains the card information within the specified date range.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    # Convert string dates to datetime.date if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    # Check if dates are in correct order when both are provided
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError(f"start_date ({start_date}) must be earlier than or equal to end_date ({end_date})")

    flat_card_list: list[dict[str, UUID | datetime.datetime | bool]] = []

    for card in card_list:
        card_date = card.creation_datetime.date() if isinstance(card.creation_datetime, datetime.datetime) else card.creation_datetime

        # Filter cards based on dates
        if (start_date is None or card_date >= start_date) and (end_date is None or card_date <= end_date):
            flat_card_list.append({
                "uuid": card.uuid,
                "creation_datetime": card.creation_datetime,
                "is_hidden": card.is_hidden,
            })

    card_df = pd.DataFrame(flat_card_list)
    return card_df


def acquisition_review_dataframe(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> pd.DataFrame:
    """
    Generate a DataFrame that contains the acquisition review information between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until the latest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    pandas.DataFrame
        A DataFrame that contains the acquisition review information within the specified date range.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    # Convert string dates to datetime.date if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    # Check if dates are in correct order when both are provided
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError(f"start_date ({start_date}) must be earlier than or equal to end_date ({end_date})")

    flat_review_list: list[dict[str, UUID | datetime.datetime | bool | int | None]] = []

    with sqlmodel.Session(engine) as session:
        query = sqlmodel.select(AcquisitionReview)
        
        if start_date is not None:
            query = query.where(AcquisitionReview.review_datetime_utc >= start_date)
        if end_date is not None:
            query = query.where(AcquisitionReview.review_datetime_utc <= end_date)

        reviews = session.exec(query)

        for review in reviews:
            flat_review_list.append(
                {
                    "uuid": review.uuid,
                    "card_uuid": review.card_uuid,
                    "review_datetime": review.review_datetime_utc,
                    "is_right_answer": review.is_right_answer,
                    "user_response_time_ms": review.user_response_time_ms,
                    # "timedelta": review.timedelta,
                    # "last_validated_timedelta": review.last_validated_timedelta
                }
            )

    review_df = pd.DataFrame(flat_review_list)

    return review_df


def consolidation_review_dataframe(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> pd.DataFrame:
    """
    Generate a DataFrame that contains the consolidation review information between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until the latest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    pandas.DataFrame
        A DataFrame that contains the consolidation review information within the specified date range.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    # Convert string dates to datetime.date if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    # Check if dates are in correct order when both are provided
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError(f"start_date ({start_date}) must be earlier than or equal to end_date ({end_date})")

    flat_review_list: list[dict[str, UUID | datetime.datetime | bool | int | None]] = []

    with sqlmodel.Session(engine) as session:
        query = sqlmodel.select(ConsolidationReview)
        
        if start_date is not None:
            query = query.where(ConsolidationReview.review_datetime_utc >= start_date)
        if end_date is not None:
            query = query.where(ConsolidationReview.review_datetime_utc <= end_date)

        reviews = session.exec(query)

        for review in reviews:
            flat_review_list.append(
                {
                    "uuid": review.uuid,
                    "card_uuid": review.card_uuid,
                    "review_datetime": review.review_datetime_utc,
                    "is_right_answer": review.is_right_answer,
                    "user_response_time_ms": review.user_response_time_ms,
                    # "timedelta": review.timedelta,
                    # "last_validated_timedelta": review.last_validated_timedelta
                }
            )

    review_df = pd.DataFrame(flat_review_list)

    return review_df


def count_card_creation_per_day(
    card_list: list[Card],      # TODO: TEMPORARY WORKAROUND
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> pd.Series:
    """
    Count the number of cards creation per day in the database between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest card.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until today.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    pd.Series
        The number of cards creation per day in the database within the specified date range.
        Days with no card creation will have a count of 0.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    df = card_dataframe(card_list, start_date, end_date)

    # Convert string dates if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    if end_date is None:
        end_date = datetime.date.today()

    if df.empty:
        if start_date is None:
            return pd.Series(dtype=int)
        # Create empty series with specified date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        return pd.Series(0, index=date_range)

    # Group by creation datetime and count the number of cards creation on each day
    series = df.groupby(df.creation_datetime.dt.date).size()

    # Create complete date range
    if start_date is not None:
        min_date = start_date
    else:
        min_date = series.index.min()

    max_date = end_date  # Now always using end_date (which is either user-provided or today)

    # Create complete date range and reindex series
    complete_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    series = series.reindex(complete_date_range, fill_value=0)

    return series


def count_acquisition_reviews_per_day(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> pd.Series:
    """
    Count the number of acquisition reviews per day in the database between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until today.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    pd.Series
        The number of acquisition reviews per day in the database within the specified date range.
        Days with no reviews will have a count of 0.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    df = acquisition_review_dataframe(start_date, end_date)

    # Convert string dates if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    if end_date is None:
        end_date = datetime.date.today()

    if df.empty:
        if start_date is None:
            return pd.Series(dtype=int)
        # Create empty series with specified date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        return pd.Series(0, index=date_range)

    # Group by review datetime and count the number of cards reviewed on each day
    series = df.groupby(df.review_datetime.dt.date).size()

    # Create complete date range
    if start_date is not None:
        min_date = start_date
    else:
        min_date = series.index.min()

    max_date = end_date  # Now always using end_date (which is either user-provided or today)

    # Create complete date range and reindex series
    complete_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    series = series.reindex(complete_date_range, fill_value=0)

    return series


def count_consolidation_reviews_per_day(
    start_date: datetime.date | str | None = None,
    end_date: datetime.date | str | None = None
) -> pd.Series:
    """
    Count the number of consolidation reviews per day in the database between two dates.

    Parameters
    ----------
    start_date : Union[datetime.date, str], optional
        The start date for the search. If None, counts from the earliest review.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.
    end_date : Union[datetime.date, str], optional
        The end date for the search. If None, counts until today.
        Can be a datetime.date object or a string in 'YYYY-MM-DD' format.

    Returns
    -------
    pd.Series
        The number of consolidation reviews per day in the database within the specified date range.
        Days with no reviews will have a count of 0.

    Raises
    ------
    ValueError
        If start_date is later than end_date.
    """
    df = consolidation_review_dataframe(start_date, end_date)

    # Convert string dates if necessary
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    if end_date is None:
        end_date = datetime.date.today()

    if df.empty:
        if start_date is None:
            return pd.Series(dtype=int)
        # Create empty series with specified date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        return pd.Series(0, index=date_range)

    # Group by review datetime and count the number of cards reviewed on each day
    series = df.groupby(df.review_datetime.dt.date).size()

    # Create complete date range
    if start_date is not None:
        min_date = start_date
    else:
        min_date = series.index.min()

    max_date = end_date  # Now always using end_date (which is either user-provided or today)

    # Create complete date range and reindex series
    complete_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    series = series.reindex(complete_date_range, fill_value=0)

    return series


###################################################################################################

def compute_timedelta_and_last_validated_timedelta(card_list: list[Card]) -> dict[UUID, dict[str, datetime.datetime | bool | datetime.timedelta]]:
    """
    Compute the timedelta and last validated timedelta for each consolidation review in a list of Card objects.

    Parameters
    ----------
    card_list : list of Card
        The list of Card objects for which to compute the timedelta and last validated timedelta.

    Returns
    -------
    dict[UUID, dict[str, datetime.timedelta]]
        A dictionary containing the UUID of each consolidation review and the corresponding timedelta and last validated timedelta.
    """

    consolidation_reviews_dict: dict[UUID, dict[str, datetime.datetime | bool | datetime.timedelta]] = {}

    # TODO !

    # # # Process all the consolidation reviews
    # # with sqlmodel.Session(engine) as session:
    # #     statement = sqlmodel.select(ConsolidationReview)
    # #     review_iterator = session.exec(statement)

    # for card in card_list:
    #     if len(card.consolidation_reviews) > 0:
    #         review = card.consolidation_reviews[0]

    #         consolidation_reviews_dict[review.uuid] = {
    #             "review_datetime_utc": review.review_date,
    #             "is_right_answer": review.is_right_answer,
    #             "timedelta": TIME_DELTA_OF_FIRST_REVIEWS,
    #             "last_validated_timedelta": INIT_VALIDATED_TIME_DELTA
    #         }

    #         for i in range(1, len(card.consolidation_reviews)):
    #             review = card.consolidation_reviews[i]
    #             previous_review = card.consolidation_reviews[i-1]

    #             dt1 = previous_review.review_date
    #             dt2 = review.review_date
    #             previous_timedelta = consolidation_reviews_dict[previous_review.uuid]["timedelta"]
    #             is_right_previous_answer = previous_review.is_right_answer

    #             consolidation_reviews_dict[review.uuid] = {
    #                 "review_datetime_utc": review.review_date,
    #                 "is_right_answer": review.is_right_answer,
    #                 "timedelta": dt2 - dt1,
    #                 "last_validated_timedelta": previous_timedelta if is_right_previous_answer else INIT_VALIDATED_TIME_DELTA
    #             }
    
    return consolidation_reviews_dict


def review_delta_dataframe(card_list: list[Card]) -> pd.DataFrame:
    flat_review_list: list[dict[str, UUID | datetime.datetime | datetime.timedelta | bool | int | None]] = []

    consolidation_reviews_dict = compute_timedelta_and_last_validated_timedelta(card_list)

    for review_uuid, review_dict in consolidation_reviews_dict.items():
        timedelta = review_dict.get("timedelta")
        timedelta = int(timedelta.total_seconds() / (60 * 60 * 24)) if timedelta is not None else None

        last_validated_timedelta = review_dict.get("last_validated_timedelta")
        last_validated_timedelta = int(last_validated_timedelta.total_seconds() / (60 * 60 * 24)) if last_validated_timedelta is not None else None

        if timedelta is not None and last_validated_timedelta is not None:
            flat_review_list.append(
                {
                    "uuid": review_uuid,
                    "review_datetime_utc": review_dict["review_datetime_utc"],
                    "is_right_answer": int(review_dict["is_right_answer"]),
                    "timedelta_days": timedelta,
                    "last_validated_timedelta_days": last_validated_timedelta
                }
            )

    df = pd.DataFrame(flat_review_list)

    return df


if __name__ == "__main__":
    print(count_acquisition_reviews())
    print(count_consolidation_reviews())
    print(acquisition_review_dataframe())
    print(consolidation_review_dataframe())
