import typing

import sqlalchemy

import config as settings
from src.models.core import BaseModel

ModelClass = typing.TypeVar(
    "ModelClass",
    bound=type[BaseModel],
)


class BaseRepository(typing.Generic[ModelClass]):
    """Base repository class for interactive with database."""

    model: type[ModelClass]

    async def get_list(
        self,
    ) -> typing.Iterable[ModelClass]:
        """Return list of records from database."""
        session = await settings.session_generator().asend(None)
        raw_result = await session.execute(
            sqlalchemy.select(self.model),
        )
        return raw_result.scalars().all()

    async def create_one(
        self,
        **data: dict,
    ) -> ModelClass:
        """Create isntance."""
        session = await settings.session_generator().asend(None)
        raw_result = await session.execute(
            sqlalchemy.insert(self.model).values(**data),
        )
        return raw_result.scalar_one()

    async def retrieve_one(
        self,
        pk: int,
    ) -> ModelClass | None:
        """Retrun one instance by pk."""
        session = await settings.session_generator().asend(None)
        raw_result = await session.execute(
            sqlalchemy.select(self.model).where(self.model.id == pk),
        )
        return raw_result.scalar_one_or_none()

    async def update_one(self, pk: int, **data) -> ModelClass | None:
        """Update instance."""
        session = await settings.session_generator().asend(None)
        raw_result = await session.execute(
            sqlalchemy.update(self.model).where(self.model.id == pk).values(**data),
        )
        return raw_result.scalar_one_or_none()

    async def delete_one(
        self,
        pk: int,
    ) -> int:
        """Delete instance."""
        session = await settings.session_generator().asend(None)
        raw_result = await session.execute(
            sqlalchemy.delete(self.model).where(self.model.id == pk)
        )
        return raw_result.rowcount
