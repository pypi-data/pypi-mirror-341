from collections.abc import Callable

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, NoResultFound

from ...types_app import _AS, TypeModel, TypePK
from .exceptions import AlreadyExists, NotFound, NotNullViolationError
from .messages import Message


# UTILS =============================================================
async def _exec(
    session: _AS,
    stmt,
    commit: bool = False,
    scalars: bool = True,
) -> sa.Result:
    result = await getattr(session, "scalars" if scalars else "execute")(stmt)
    if commit:
        await session.commit()
    return result


async def _get(
    session: _AS,
    model: TypeModel,
    **filter_data,
) -> sa.Result:
    return await _exec(
        session=session,
        stmt=sa.select(model).filter_by(**filter_data),
        commit=False,
    )


def _fetch_one(
    result: sa.Result,
    attributes: dict,
) -> TypeModel:
    try:
        return result.one()
    except NoResultFound:
        raise NotFound(Message.Error.NOT_FOUND.format(attrs=attributes))


async def _try_create(f: Callable, obj: TypeModel) -> TypeModel:
    try:
        return await f()
    except IntegrityError as e:
        if "asyncpg.exceptions.NotNullViolationError" in str(e):
            raise NotNullViolationError(e.args[0].split("\n")[0].split(": ")[-1])
        raise AlreadyExists(Message.Error.ALREADY_EXISTS.format(obj=obj))


# CRUD ===============================================
async def get_all(
    session: _AS,
    model: TypeModel,
    **filter_data,
) -> list[TypeModel]:
    """Get all rows from the table or from the filtered selection."""
    return (await _get(session, model, **filter_data)).all()


async def get_one(
    session: _AS,
    model: TypeModel,
    **filter_data,
) -> TypeModel:
    return _fetch_one(
        result=await _get(session, model, **filter_data),
        attributes=filter_data,
    )


async def create(
    session: _AS,
    obj: TypeModel,
    commit: bool = False,
) -> TypeModel:
    async def f() -> TypeModel:
        session.add(obj)
        await (session.commit() if commit else session.flush([obj]))
        await session.refresh(obj)
        return obj

    return await _try_create(f, obj)


async def insert(
    session: _AS,
    model: TypeModel,
    commit: bool = False,
    **data,
) -> TypeModel:
    async def f() -> TypeModel:
        return (
            await _exec(
                session=session,
                stmt=sa.insert(model).values(**data).returning(model),
                commit=commit,
            )
        ).one()

    return await _try_create(f, model(**data))


async def update(
    session: _AS,
    model: TypeModel,
    id: TypePK,
    commit: bool = False,
    **data,
) -> TypeModel:
    return _fetch_one(
        result=await _exec(
            session=session,
            stmt=sa.update(model).where(model.id == id).values(**data).returning(model),
            commit=commit,
        ),
        attributes={"id": id},
    )


async def delete(
    session: _AS,
    model: TypeModel,
    id: TypePK,
    commit: bool = False,
) -> TypeModel:
    return _fetch_one(
        result=await _exec(
            session=session,
            stmt=sa.delete(model).where(model.id == id).returning(model),
            commit=commit,
        ),
        attributes={"id": id},
    )


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(BaseModel.metadata.create_all)
