from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

from cms.core.auth import create_access_token, get_current_user
from cms.core.db import depends_db, m2d
from cms.core.logger import logger
from cms.logic.common.user import crud_user, Token, UserCreate, UserUpdate, UserUpdateMe, UserOut
from cms.logic.common.user import crud_role, RoleCreate, RoleUpdate


router = APIRouter()


@router.post("/login/access-token", response_model=Token, summary='用户登录')
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    pgdb=Depends(depends_db)
):
    """
    OAuth2 密码模式登录
    """
    status, user = await crud_user.login(pgdvm=pgdb, username=form_data.username, password=form_data.password)
    if not status:
        raise HTTPException(status_code=403, detail=user)

    data = {"id": user.id,
            "uid": user.uid,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "role_id": user.role_id,
            "attrs": user.attrs}

    return {
        "access_token": create_access_token(data=data),
        "token_type": "bearer"
    }


@router.get("/users", summary='获取用户列表', response_model=List[UserOut])
async def read_users(
    query: str = Query(None, title='搜索关键字',
                       description='模糊查询匹配(用户名, 昵称, 邮箱和电话)'),
    pgdb=Depends(depends_db),
    current_user=Depends(get_current_user),
):
    lst = await crud_user.get_multi(pgdvm=pgdb, querykey=query)
    return m2d(lst)


@router.get('/users/me', summary='获取当前登录用户信息', response_model=UserOut)
async def user_me(
    pgdb=Depends(depends_db),
    current_user=Depends(get_current_user)
):
    """
    获取当前登录用户信息
    """
    try:
        user = await crud_user.get(pgdvm=pgdb, id=current_user['id'])
        return m2d(user)
    except Exception as e:
        logger.error(e)


@router.put('/users/me', summary='修改当前登录用户信息')
async def update_user_me(
    user_in: UserUpdateMe,
    pgdb=Depends(depends_db),
    current_user=Depends(get_current_user)
):
    """
    获取当前登录用户信息
    """
    user = await crud_user.get(pgdvm=pgdb, id=current_user['id'])
    user = await crud_user.update(pgdvm=pgdb, db_obj=user, obj_in=user_in)
    return m2d(user)


@router.get('/users/{id}', summary='按ID获取信息', response_model=UserOut)
async def user_one(
    id: int = Path(..., title="ID"),
    pgdb=Depends(depends_db),
    current_user=Depends(get_current_user)
):
    """
    按ID获取信息
    """
    user = await crud_user.get(pgdvm=pgdb, id=id)
    logger.info(user.username)
    logger.info(f'role:{user.role_id}')
    return m2d(user)


@router.post("/users", summary='添加用户', status_code=201,  response_model=UserOut)
async def create_user(
        user_in: UserCreate,
        pgdb=Depends(depends_db),
        current_user=Depends(get_current_user)):
    """
    添加用户
    """
    user = await crud_user.create(pgdvm=pgdb, obj_in=user_in)
    return m2d(user)


@router.put("/users/{id}", summary='编辑用户', status_code=201, response_model=UserOut)
async def update_user(
        user_in: UserUpdate,
        id: int = Path(..., title="ID"),
        pgdb=Depends(depends_db),
        current_user=Depends(get_current_user)):
    """
    编辑用户, 覆盖编辑
    """
    user = await crud_user.get(pgdvm=pgdb, id=id)
    user = await crud_user.update(pgdvm=pgdb, db_obj=user, obj_in=user_in)
    return m2d(user)


@router.delete('/users/{id}', summary='按ID禁用信息')
async def del_user(
    id: int = Path(..., title="ID"),
    pgdb=Depends(depends_db),
    current_user=Depends(get_current_user)
):
    """
    按ID禁用信息
    """
    user = await crud_user.get(pgdvm=pgdb, id=id)
    user_in = UserUpdate(is_active=False)
    user = await crud_user.update(pgdvm=pgdb, db_obj=user, obj_in=user_in)
    return m2d(user)


@router.get("/roles", summary='获取角色列表')
async def read_roles(
    limit: int = Query(100, title="返回数量"),
    skip: int = Query(0, title="跳过数量"),
    pgdb=Depends(depends_db),
    current_user=Depends(get_current_user),
):
    lst = await crud_role.get_multi(pgdvm=pgdb, skip=skip, limit=limit)
    return m2d(lst)


@router.post("/roles", summary='添加角色', status_code=201)
async def create_role(
        obj_in: RoleCreate,
        pgdb=Depends(depends_db),
        current_user=Depends(get_current_user)):
    """
    添加角色
    """
    obj = await crud_role.create(pgdvm=pgdb, obj_in=obj_in)
    return m2d(obj)


@router.put("/roles/{id}", summary='编辑角色', status_code=201)
async def update_role(
        obj_in: RoleUpdate,
        id: int = Path(..., title="ID"),
        pgdb=Depends(depends_db),
        current_user=Depends(get_current_user)):
    """
    编辑角色, 覆盖编辑
    """
    obj = await crud_role.get(pgdvm=pgdb, id=id)
    obj = await crud_role.update(pgdvm=pgdb, db_obj=obj, obj_in=obj_in)
    return m2d(obj)


@router.delete("/roles/{id}", summary='删除角色', status_code=201)
async def del_role(
        id: int = Path(..., title="ID"),
        pgdb=Depends(depends_db),
        current_user=Depends(get_current_user)):
    """
    删除角色
    """
    await crud_role.remove(pgdvm=pgdb, id=id)
    return True
