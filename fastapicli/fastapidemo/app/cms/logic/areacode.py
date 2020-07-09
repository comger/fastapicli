from pydantic import BaseModel, Field
from typing import List
from peewee import CharField, ForeignKeyField, CompositeKey
from cms.core.db import DataViewsionManage, DBBaseModel, pgdb
from cms.logic.common.crud import CRUDBase
from cms.core.logger import Logger

logger = Logger().getLogger()


class AreaCode(DBBaseModel):
    """ 地区组织, 嵌套结构 """
    name = CharField()
    parent = ForeignKeyField('self', null=True, backref='children')


class AreaCodeBase(BaseModel):
    name: str = Field(None, max_length=40, min_length=2, title='地区名称')
    parent_id: int = Field(None, title="父节点ID")


class AreaCodeCreate(AreaCodeBase):
    pass


class AreaCodetUpdate(AreaCodeBase):
    id: int = Field(..., title="分组id")


class AreaCodeOut(AreaCodetUpdate):
    parent: AreaCodetUpdate = Field(None, title="父节点")


class CRUDAreaCode(CRUDBase[AreaCode, AreaCodeCreate, AreaCodetUpdate, AreaCodeOut]):
    
    async def get_multi(
        self, pgdvm: DataViewsionManage, *, parent_id=0,skip: int = 0, limit: int = 100, **kwargs
    ) -> List[AreaCodeOut]:
        query = self.model.select().where(AreaCode.parent==parent_id).offset(skip).limit(limit)
        lst = await pgdvm.execute(query)
        return lst

crud_AreaCode = CRUDAreaCode(AreaCode)
