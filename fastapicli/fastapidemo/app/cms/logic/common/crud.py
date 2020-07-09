from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from cms.core.db import DataViewsionManage, DBBaseModel


ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)

class PageInfo(BaseModel):
    total: int = Field(..., title='总数')
    data: List[OutSchemaType] = Field([], title='列表')


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, OutSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, pgdvm: DataViewsionManage, id: Any) -> Optional[ModelType]:
        obj = await pgdvm.get(self.model, id=id)
        return obj

    async def get_multi(
        self, pgdvm: DataViewsionManage, *, skip: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        query = self.model.select().offset(skip).limit(limit)
        lst = await pgdvm.execute(query)
        return lst

    async def get_page(
        self, pgdvm: DataViewsionManage, *, page_index: int = 1, page_size: int = 100, **kwargs
    ) -> (int, List[ModelType]):
        count = await self.count(pgdvm=pgdvm)
        query = self.model.select().offset(page_size * (page_index - 1)).limit(page_size)
        lst = await pgdvm.execute(query)
        return count, lst


    async def count(self, pgdvm: DataViewsionManage, **kwargs) -> int:
        query = self.model.select()
        return await pgdvm.count(query)

    async def create(self, pgdvm: DataViewsionManage, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj = await pgdvm.create(self.model, **obj_in_data)
        return obj

    async def update(
        self,
        pgdvm: DataViewsionManage,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, val in update_data.items():
            setattr(db_obj, field, val)

        await pgdvm.update(db_obj)
        return db_obj

    async def remove(self, pgdvm: DataViewsionManage, *, id: int) -> ModelType:
        obj = await pgdvm.get(self.model, id=id)
        await pgdvm.delete(obj)
        return obj
