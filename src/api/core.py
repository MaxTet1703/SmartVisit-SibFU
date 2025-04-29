import http
import typing

import fastapi
import pydantic

from src.entities.core import BaseReadModelSchema
from src.repositories.core import BaseRepository

RepositoryClass = typing.TypeVar(
    "RepositoryClass",
    bound=type[BaseRepository],
)


class CRUDViewSet(typing.Generic[RepositoryClass]):
    """Define base CRUD API for models."""

    repository: RepositoryClass
    read_schema_class: type[BaseReadModelSchema]
    write_schema_class: type[pydantic.BaseModel]

    async def get(self) -> list[dict]:
        """Return list of instances."""
        result = await self.repository.get_list()
        return [self.read_schema_class.model_dump(instance) for instance in result]

    async def retrieve(self, pk) -> dict:
        """Retrieve one instance."""
        instance = self.repository.retrieve_one(pk=pk)
        if instance is None:
            raise fastapi.exceptions.HTTPException(
                status_code=http.HTTPStatus.NOT_FOUND,
                detail={
                    "detail": "Not Found",
                },
            )
        return self.read_schema_class.model_validate(instance).model_dump(mode="json")

    async def post(self, request_body: type[pydantic.BaseModel]) -> dict:
        """Create instance."""
        new_instance = self.repository.create_one(
            request_body,
            request_body.model_dump(mode="json"),
        )
        return self.read_schema_class.model_validate(new_instance).model_dump(
            mode="json"
        )

    async def update(
        self,
        pk: int,
        request_body: type[pydantic.BaseModel],
    ) -> dict:
        """Update instance."""
        instance = await self.repository.retrieve_one(pk=pk)
        if instance is None:
            raise fastapi.exceptions.HTTPException(
                status_code=http.HTTPStatus.NOT_FOUND,
                detail={
                    "detail": "Not Found",
                },
            )
        updated_instance = await self.repository.update_one(
            pk=instance.id,
        )
        return self.read_schema_class.model_validate(updated_instance).model_dump(
            mode="json"
        )

    async def delete(
        self,
        pk: int,
    ) -> fastapi.Response:
        """Delete response."""
        is_deleted = await self.repository.delete_one(pk=pk)
        if not is_deleted:
            raise fastapi.exceptions.HTTPException(
                status_code=http.HTTPStatus.NOT_FOUND,
                detail={
                    "detail": "Not Found",
                },
            )
        return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)

    actions = {
        "get": get,
        "post": post,
        "update": update,
        "delete": delete,
    }
    # Exclude base actions for specified API
    exclude: tuple[str] = tuple()
