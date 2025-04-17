import uuid
from typing import TypeVar, Type, Generic, Optional, List, Dict, Literal, Union, Sequence
from sqlalchemy import select, delete, update, and_, func, desc, inspect
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, InstrumentedAttribute, selectinload, RelationshipProperty

from rb_commons.http.exceptions import NotFoundException
from rb_commons.orm.exceptions import DatabaseException, InternalException

ModelType = TypeVar('ModelType', bound=declarative_base())

def with_transaction_error_handling(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IntegrityError as e:
            await self.session.rollback()
            raise InternalException(f"Constraint violation: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Database error: {str(e)}") from e
        except Exception as e:
            await self.session.rollback()
            raise InternalException(f"Unexpected error: {str(e)}") from e
    return wrapper

class BaseManager(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.data = None
        self.filters = []
        self._filtered = False
        self._limit = None

    async def _smart_commit(self, instance: Optional[ModelType] = None) -> Optional[ModelType]:
        if not self.session.in_transaction():
            await self.session.commit()

        if instance:
            await self.session.refresh(instance)
            return instance

    async def get(self, pk: Union[str, int, uuid.UUID], load_relations: Sequence[str] = None) -> Optional[ModelType]:
        """
           get object based on conditions
       """
        stmt = select(self.model).filter_by(id=pk)

        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise NotFoundException(
                message="Object does not exist",
                status=404,
                code="0001",
            )

        return instance

    def _apply_eager_loading(self, stmt, load_all_relations: bool = False):
        if not load_all_relations:
            return stmt

        opts = []
        visited = set()

        def recurse(model, loader=None):
            mapper = inspect(model)
            if mapper in visited:
                return
            visited.add(mapper)

            for rel in mapper.relationships:
                attr = getattr(model, rel.key)
                if loader is None:
                    this_loader = selectinload(attr)
                else:
                    this_loader = loader.selectinload(attr)
                opts.append(this_loader)
                recurse(rel.mapper.class_, this_loader)

        recurse(self.model)
        return stmt.options(*opts)

    def filter(self, **kwargs) -> 'BaseManager[ModelType]':
        """
           Dynamically apply filters to the query.

           Supported operators:
             - __eq       (e.g., field__eq=value) or just field=value
             - __ne       (field__ne=value)
             - __gt       (field__gt=value)
             - __lt       (field__lt=value)
             - __gte      (field__gte=value)
             - __lte      (field__lte=value)
             - __in       (field__in=[val1, val2, ...])
             - __contains (field__contains='text')
             - __null     (field__null=True/False) - True for IS NULL, False for IS NOT NULL

           Additionally supports nested paths, e.g.,
             product__shop_id=None
             product__shop__country='US'
        """
        self._filtered = True
        self.filters = []

        for key, value in kwargs.items():
            parts = key.split("__")

            operator = "eq"

            if parts[-1] in {"eq", "ne", "gt", "lt", "gte", "lte", "in", "contains", "null"}:
                operator = parts.pop()

            current_attr = self.model

            for field_name in parts:
                attr_candidate = getattr(current_attr, field_name, None)
                if attr_candidate is None:
                    raise ValueError(f"Invalid filter field: {'.'.join(parts)}")

                if hasattr(attr_candidate, "property") and isinstance(attr_candidate.property, RelationshipProperty):
                    current_attr = attr_candidate.property.mapper.class_
                else:
                    current_attr = attr_candidate

            if operator == "eq":
                # e.g., column == value
                self.filters.append(current_attr == value)

            elif operator == "ne":
                # e.g., column != value
                self.filters.append(current_attr != value)

            elif operator == "gt":
                self.filters.append(current_attr > value)

            elif operator == "lt":
                self.filters.append(current_attr < value)

            elif operator == "gte":
                self.filters.append(current_attr >= value)

            elif operator == "lte":
                self.filters.append(current_attr <= value)

            elif operator == "in":
                if not isinstance(value, list):
                    raise ValueError(f"{'.'.join(parts)}__in requires a list, got {type(value)}")
                self.filters.append(current_attr.in_(value))

            elif operator == "contains":
                # e.g., column ILIKE %value%
                self.filters.append(current_attr.ilike(f"%{value}%"))
                
            elif operator == "null":
                if value is True:
                    self.filters.append(current_attr.is_(None))
                else:
                    self.filters.append(current_attr.isnot(None))

        return self

    def _ensure_filtered(self):
        """Ensure that `filter()` has been called before using certain methods."""
        if not self._filtered:
            raise RuntimeError("You must call `filter()` before using this method.")

    async def _execute_query_and_unique_data(self, stmt, load_all_relations: bool) -> List[ModelType]:
        stmt = self._apply_eager_loading(stmt, load_all_relations)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        unique_by_pk = {obj.id: obj for obj in rows}
        return list(unique_by_pk.values())

    async def all(self, load_all_relations: bool = False) -> List[ModelType] | None:
        try:
            stmt = select(self.model)

            if self._filtered:
                stmt = stmt.filter(and_(*self.filters))

            if self._limit:
                stmt = stmt.limit(self._limit)

            self._clear_query_state()

            return await self._execute_query_and_unique_data(stmt, load_all_relations)
        finally:
            self._clear_query_state()

    def _clear_query_state(self):
        """Clear all query state after execution"""
        self._filtered = False
        self.filters = []
        self._limit = None

    async def paginate(self, limit: int = 10, offset: int = 0, load_all_relations: bool = False) -> List[ModelType]:
        self._ensure_filtered()
        stmt = select(self.model).filter(and_(*self.filters)).limit(limit).offset(offset)
        return await self._execute_query_and_unique_data(stmt, load_all_relations)

    def limit(self, value: int) -> 'BaseManager[ModelType]':
        """
        Set a limit on the number of results returned by queries like `all()` or `first()`.
        """
        self._limit = value
        return self

    async def first(self, load_relations: Sequence[str] = None) -> Optional[ModelType]:
        """Return the first matching object, or None."""
        self._ensure_filtered()

        stmt = select(self.model).filter(and_(*self.filters))

        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def last(self, load_relations: Sequence[str] = None) -> Optional[ModelType]:
        """Return the last matching object, or None."""

        self._ensure_filtered()

        stmt = select(self.model).filter(and_(*self.filters)).order_by(desc(self.model.id))

        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def count(self) -> int:
        """Return the count of matching records."""

        self._ensure_filtered()
        query = select(func.count()).select_from(self.model).filter(and_(*self.filters))
        result = await self.session.execute(query)
        return result.scalar_one()

    @with_transaction_error_handling
    async def create(self, **kwargs) -> ModelType:
        """
               Create a new object
        """
        obj = self.model(**kwargs)

        self.session.add(obj)
        await self.session.flush()
        return await self._smart_commit(obj)

    @with_transaction_error_handling
    async def delete(self, instance: ModelType = None) -> bool:
        """
        Delete object(s) with flexible filtering options
            - If `instance` is provided, delete that single instance.
            - If `instance` is not provided, delete according to self.filters.

        :arg instance: Model instance to delete.
        :return: Number of deleted records or None
        """

        if instance is not None:
            await self.session.delete(instance)
            await self.session.commit()
            return True

        self._ensure_filtered()

        try:
            delete_stmt = delete(self.model).where(and_(*self.filters))
            await self.session.execute(delete_stmt)
            await self.session.commit()
            return True
        except NoResultFound:
            return False

    @with_transaction_error_handling
    async def bulk_delete(self) -> int:
        """
            Bulk delete with flexible filtering.

            Automatically commits if not inside a transaction.

            :return: Number of deleted records
        """
        self._ensure_filtered()

        delete_stmt = delete(self.model).where(and_(*self.filters))
        result = await self.session.execute(delete_stmt)
        await self._smart_commit()
        return result.rowcount  # ignore

    @with_transaction_error_handling
    async def update_by_filters(self, filters: Dict, **update_fields) -> Optional[ModelType]:
        """
        Update object(s) with flexible filtering options

        :param filters: Conditions for selecting records to update
        :param update_fields: Fields and values to update
        :return: Number of updated records
        """
        if not update_fields:
            raise InternalException("No fields provided for update")

        update_stmt = update(self.model).filter_by(**filters).values(**update_fields)
        await self.session.execute(update_stmt)
        await self.session.commit()
        updated_instance = await self.get(**filters)
        return updated_instance

    @with_transaction_error_handling
    async def update(self, instance: ModelType, **update_fields) -> Optional[ModelType]:
        """
        Update an existing database instance with new fields

        :param instance: The database model instance to update
        :param update_fields: Keyword arguments of fields to update
        :return: The updated instance

        :raises InternalException: If integrity violation
        :raises DatabaseException: For database-related errors
        """
        # Validate update fields
        if not update_fields:
            raise InternalException("No fields provided for update")

        # Apply updates directly to the instance
        for key, value in update_fields.items():
            setattr(instance, key, value)

        self.session.add(instance)
        await self._smart_commit()

        return instance

    @with_transaction_error_handling
    async def save(self, instance: ModelType) -> Optional[ModelType]:
        """
        Save instance

        :param instance: The database model instance to save
        :return: The saved instance

        Automatically commits if not inside a transaction.

        :raises InternalException: If integrity violation
        :raises DatabaseException: For database-related errors
        """
        self.session.add(instance)
        await self.session.flush()
        return await self._smart_commit(instance)

    @with_transaction_error_handling
    async def lazy_save(self, instance: ModelType, load_relations: Sequence[str] = None) -> Optional[ModelType]:
        self.session.add(instance)
        await self.session.flush()
        await self._smart_commit(instance)

        if load_relations is None:
            mapper = inspect(self.model)
            load_relations = [rel.key for rel in mapper.relationships]

        if not load_relations:
            return instance

        stmt = select(self.model).filter_by(id=instance.id)

        for rel in load_relations:
            stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)
        loaded_instance = result.scalar_one_or_none()

        if loaded_instance is None:
            raise NotFoundException(
                message="Object saved but could not be retrieved with relationships",
                status=404,
                code="0001",
            )

        return loaded_instance

    async def is_exists(self, **kwargs) -> bool:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    @with_transaction_error_handling
    async def bulk_save(self, instances: List[ModelType]) -> None:
        """
        Bulk save a list of instances into the database.

        If inside a transaction, flushes only.
        If not in a transaction, commits after flush.

        :param instances: List of instances
        :raises DatabaseException: If any database error occurs
        :raises InternalException: If any unexpected error occurs
        """
        if not instances:
            return

        self.session.add_all(instances)
        await self.session.flush()

        if not self.session.in_transaction():
            await self.session.commit()

    def has_relation(self, relation_name: str) -> 'BaseManager[ModelType]':
        """
           Check if a relationship exists between models using an EXISTS subquery.

           :param relation_name Name of the relationship to check. Must be a valid relationship
                   defined in the model.

           :return BaseManager[ModelType]: Self instance for method chaining.

           :raise DatabaseException: If there's an error constructing the subquery.
           :raise InternalException: If there's an unexpected error in relationship handling.

           Notes:
               - The relationship must be properly defined in the SQLAlchemy model
               - Uses a non-correlated EXISTS subquery for better performance
               - Silently continues if the relationship doesn't exist
           """
        # Get the relationship property
        relationship = getattr(self.model, relation_name)

        # Create subquery using select
        subquery = (
            select(1)
            .select_from(relationship.property.mapper.class_)
            .where(relationship.property.primaryjoin)
            .exists()
        )

        # Add the exists condition to filters
        self.filters.append(subquery)

        return self

    def model_to_dict(self, instance: ModelType, exclude: set = None):
        exclude = exclude or set()

        return {
            c.key: getattr(instance, c.key)
            for c in inspect(instance).mapper.column_attrs
            if c.key not in exclude
        }

