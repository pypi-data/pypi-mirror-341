from collections.abc import Callable
import datetime
import warnings

class AbstractProfessorObserver:
    pass

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)  # Create a timezone-aware datetime object

class AbstractProfessor:

    def __init__(
        self,
        current_datetime_fn: Callable[[], datetime.datetime] = utcnow,
    ):
        self.observer_list: list[AbstractProfessorObserver] = []

        # Define the current date which can be either the real current date or a mock
        self.current_datetime_fn: Callable[[], datetime.datetime] = current_datetime_fn


    # ANSWER CALLBACK #################

    def add_reply_observer(self, observer: AbstractProfessorObserver):
        self.observer_list.append(observer)

    def remove_reply_observer(self, observer: AbstractProfessorObserver):
        try:
            self.observer_list.remove(observer)
        except ValueError as err:
            warnings.warn(f"observer {observer} not in prof {self}\n{err}")

    def notify_observers_of_reply(self):
        """This function is supposed to be called after each reply"""
        for observer in self.observer_list:
            observer.answer_callback()


    ###################################

    @property
    def current_card(self):
        raise NotImplementedError()


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
        raise NotImplementedError()


    @property
    def remaining_cards(self) -> float:
        # Some professor may ask the same questions for an infinite (or unpredictable) number of times
        return float("inf")


    @property
    def feedback_msg(self) -> str:
        return ""
