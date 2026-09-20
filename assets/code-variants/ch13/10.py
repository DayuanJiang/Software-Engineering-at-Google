# Python has no @DoNotMock annotation; state the preferred alternative in the
# docstring and provide a real, easy-to-construct implementation instead.
class Query(ABC):
    """Use SimpleQuery.create() instead of mocking."""

    @abstractmethod
    def get_query_value(self) -> str: ...
