from typing import Any, Literal, TypeVar

from polycrud.entity import ModelEntity

T = TypeVar("T", bound=ModelEntity)


class BaseConnector:
    """
    Base class for all connectors.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the connector with the given parameters.
        """
        self.params = kwargs

    async def connect(self, **kwargs: Any) -> None:
        """
        Connect to the data source.
        """
        raise NotImplementedError("Connect method not implemented.")

    async def disconnect(self) -> None:
        """
        Disconnect from the data source.
        """
        raise NotImplementedError("Disconnect method not implemented.")

    async def health_check(self) -> None:
        """
        Check the health of the connection.
        """
        raise NotImplementedError("Health check method not implemented.")

    async def insert_one(self, obj: T) -> T:
        """
        Insert a single object into the data source.
        """
        raise NotImplementedError("Insert one method not implemented.")

    async def insert_many(self, objs: list[T]) -> list[T]:
        """
        Insert multiple objects into the data source.
        """
        raise NotImplementedError("Insert many method not implemented.")

    async def update_one(self, obj: T) -> T:
        """
        Update a single object in the data source.
        """
        raise NotImplementedError("Update one method not implemented.")

    async def find_one(self, collection: type[T], query: str | None = None, **kwargs: Any) -> T:
        """
        Find a single object in the data source.
        """
        raise NotImplementedError("Find one method not implemented.")

    async def find_many(
        self,
        collection: type[T],
        limit: int = 10_000,
        page: int = 1,
        sort_field: str = "id",
        sort_dir: Literal["asc", "desc"] = "asc",
        query: str | None = None,
        **kwargs: Any,
    ) -> list[T]:
        """
        Find multiple objects in the data source.
        """
        raise NotImplementedError("Find many method not implemented.")

    async def delete_one(self, collection: type[T], query: str | None = None, **kwargs: Any) -> T:
        """
        Delete a single object from the data source.
        """
        raise NotImplementedError("Delete one method not implemented.")

    async def delete_many(self, collection: type[T], query: str | None = None, **kwargs: Any) -> list[T]:
        """
        Delete multiple objects from the data source.
        """
        raise NotImplementedError("Delete many method not implemented.")

    async def count(self, collection: type[T], query: str | None = None, **kwargs: Any) -> int:
        """
        Count the number of objects in the data source.
        """
        raise NotImplementedError("Count method not implemented.")
