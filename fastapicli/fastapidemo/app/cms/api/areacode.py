from typing import List
from fastapi import APIRouter, Depends, Query, Path

from cms.core.auth import get_current_user
from cms.core.db import depends_db, m2d
from cms.logic.areacode import crud_AreaCode, AreaCodeCreate, AreaCodetUpdate, AreaCodeOut


router = APIRouter()



@router.get('/areacodes/{parent_id}', summary='按父ID获取信息', response_model=List[AreaCodeOut])
async def get_list(parent_id: int = Path(..., title="parent_id"),
                    pgdb=Depends(depends_db),
                    current_user=Depends(get_current_user)):
    """
    按ID获取信息
    """
    lst = await crud_AreaCode.get_multi(pgdvm=pgdb, parent_id=parent_id)
    return lst


@router.post("/areacodes", summary='添加', status_code=201, response_model=AreaCodeOut)
async def create(obj_in: AreaCodeCreate,
                       pgdb=Depends(depends_db),
                       current_user=Depends(get_current_user)):
    """
        添加
    """
    obj = await crud_AreaCode.create(pgdvm=pgdb, obj_in=obj_in)
    return m2d(obj)



@router.delete('/areacodes/{id}', summary='按ID删除信息')
async def delete(id: int = Path(..., title="ID"),
                    pgdb=Depends(depends_db),
                    current_user=Depends(get_current_user)):
    """
    按ID删除信息, 如果有下级或被关联,则无法删除
    """
    obj = await crud_AreaCode.remove(pgdvm=pgdb, id=id)
    return m2d(obj)
