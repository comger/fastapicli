from pydantic import BaseModel, Field
from typing import List
from peewee import CharField, ForeignKeyField
from cms.core.db import DataViewsionManage, DBBaseModel, pgdb
from cms.logic.common.crud import CRUDBase
from cms.core.logger import Logger

logger = Logger().getLogger()


class {{Model}}(DBBaseModel):
    """ {ModelName} """
    name = CharField()



class {{Model}}Base(BaseModel):
    name: str = Field(None, max_length=40, min_length=2, title='名称')



class {{Model}}Create({{Model}}Base):
    pass


class {{Model}}tUpdate({{Model}}Base):
    id: int = Field(..., title="id")


class {{Model}}Out({{Model}}tUpdate):
    pass


class CRUD{{Model}}(CRUDBase[{{Model}}, {{Model}}Create, {{Model}}tUpdate, {{Model}}Out]): 
    pass

crud_{{ str.lower(Model) }} = CRUD{{Model}}({{Model}})
