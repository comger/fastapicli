from typing import List
from fastapi import APIRouter, Depends, Path, Body, Query

from cms.core.auth import get_current_user
from cms.core.db import depends_db, m2d
from cms.core.logger import logger
from cms.logic.{{ str.lower(Model) }} import crud_{{ str.lower(Model) }}, {{ Model }}Out, {{ Model }}Create, {{ Model }}Update

router = APIRouter()


@router.post("/{{ str.lower(Model) }}s", summary="添加{{ name }}", response_model={{ Model }}Out)
async def create(obj_in: {{ Model }}Create = Body(..., title="{{ name }}信息"),
                 pgdb=Depends(depends_db),
                 current_user=Depends(get_current_user)):
    """ 添加{{ name }} """
    obj = await crud_{{ str.lower(Model) }}.create(pgdvm=pgdb, obj_in=obj_in)
    return m2d(obj)


@router.get("/{{ str.lower(Model) }}s", summary="{{ name }}列表", response_model=List[{{ Model }}Out])
async def get_list(pgdb=Depends(depends_db),
                   current_user=Depends(get_current_user)):
    """ {{ name }}列表 """
    lst = await crud_{{ str.lower(Model) }}.get_multi(pgdvm=pgdb, project_id=project_id, status=status)
    return m2d(lst)


@router.delete("/{{ str.lower(Model) }}s/{id}", summary="删除{{ name }}", response_model={{ Model }}Out)
async def create(id: int = Path(..., title="{{ name }}ID"),
                 pgdb=Depends(depends_db),
                 current_user=Depends(get_current_user)):
    """ 删除{{ name }} """
    obj = await crud_{{ str.lower(Model) }}.remove(pgdvm=pgdb, id=id)
    return m2d(obj)


@router.put("/{{ str.lower(Model) }}s/{id}", summary="修改{{ name }}", response_model={{ Model }}Out)
async def update(id: int = Path(..., title="{{ name }}ID"),
                 obj_in: {{ Model }}Update = Body(..., title="{{ name }}信息"),
                 pgdb=Depends(depends_db),
                 current_user=Depends(get_current_user)):
    """ 修改{{ name }} """
    obj = await crud_{{ str.lower(Model) }}.get(pgdvm=pgdb, id=id)
    obj = await crud_{{ str.lower(Model) }}.update(pgdvm=pgdb, db_obj=obj, obj_in=obj_in)
    return m2d(obj)
