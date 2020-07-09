import uuid
from peewee import CharField, ForeignKeyField, BooleanField
from playhouse.postgres_ext import HStoreField, ArrayField
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from cms.core.config import FIRST_USER, FIRST_USER_PASSWORD
from cms.core.db import DataViewsionManage, DBBaseModel
from cms.core.auth import verify_password, get_password_hash
from cms.logic.common.crud import CRUDBase, ModelType


class UserRole(DBBaseModel):
    name = CharField(unique=True)
    scopes = ArrayField(CharField, null=True, default=[])


class RoleBase(BaseModel):
    name: str = Field(None,
                      title="角色名称",
                      description="名称不可为空, 字符长度范围2~40",
                      max_length=40,
                      min_length=2)

    scopes: Optional[List[str]] = Field([], title="权限节点列表")


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int = Field(..., title="ID")


class CRUDRole(CRUDBase[UserRole, RoleCreate, RoleUpdate, RoleOut]):
    pass


class User(DBBaseModel):
    uid = CharField(default=str(uuid.uuid1()), index=True, unique=True)
    username = CharField(unique=True)
    nickname = CharField(null=True, default="")
    email = CharField(unique=True, default="")
    password = CharField()
    tel = CharField(null=True, default="")
    is_superuser = BooleanField(default=False, null=True)
    is_active = BooleanField(default=True, null=True)
    role = ForeignKeyField(UserRole, backref='user', null=True)
    attrs = HStoreField(default={})


class UserBase(BaseModel):
    nickname: str = Field(None,
                          title="昵称",
                          description="昵称不可为空, 字符长度范围2~40",
                          max_length=40,
                          min_length=2)
    email: EmailStr = Field(None,
                            title="邮箱",
                            description="邮箱不可为空, 具备唯一性, 字符长度范围6~40")
    tel: Optional[str] = Field(None, title="手机号", description="长度必须为11. 允许为空.")
    is_superuser: Optional[bool] = Field(0,
                                         title="是否为超管",
                                         description="此处为用户中心超管, 0:非超管, 1: 超管")
    is_active: Optional[bool] = Field(1,
                                      title="是否禁用",
                                      description="禁用后,用户不能正常登录,0： 禁用, 1: 启用")
    role_id: Optional[int] = Field(None, title="角色id", description="角色外键")


class UserUpdate(UserBase):
    pass


class UserUpdateMe(UserBase):
    pass


class UserCreate(UserBase):
    username: str = Field(...,
                          title="用户名",
                          description="用户名不可为空, 具备唯一性, 字符长度范围6~40",
                          max_length=40,
                          min_length=6)
    password: str = Field(...,
                          title="密码",
                          description="密码不可为空, 字符长度范围6~40",
                          max_length=40,
                          min_length=6)
    nickname: str = Field(...,
                          title="昵称",
                          description="昵称不可为空, 字符长度范围2~40",
                          max_length=40,
                          min_length=2)
    email: EmailStr = Field(...,
                            title="邮箱",
                            description="邮箱不可为空, 具备唯一性, 字符长度范围6~40")


class UserOut(UserUpdate):
    id: int = Field(..., title="ID")
    username: str = Field(...,
                          title="用户名",
                          description="用户名不可为空, 具备唯一性, 字符长度范围6~40",
                          max_length=40,
                          min_length=6)
    role: RoleOut = Field(None, title="角色信息")


class Token(BaseModel):
    access_token: str
    token_type: str


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate, UserOut]):
    async def create(self, pgdvm: DataViewsionManage, *,
                     obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["password"] = get_password_hash(obj_in.password)
        obj = await pgdvm.create(self.model, **obj_in_data)
        return obj

    async def login(self, pgdvm: DataViewsionManage, username: str,
                    password: str):
        """
        用户登录验证
        返回
            true, user
            false, message
        """

        try:
            user = await pgdvm.get(User, username=username)
            if not verify_password(password, user.password):
                return False, "密码错误"
            if not user.is_active:
                return False, "用户已被禁用"

            return True, user
        except User.DoesNotExist:
            return False, "用户名不存在"

    async def get_multi(self,
                        pgdvm: DataViewsionManage,
                        *,
                        skip: int = 0,
                        limit: int = 100,
                        ref: bool = True,
                        **kwargs) -> List[ModelType]:
        """
        支持查询参数query key , 可匹配 username, nickname, email, tel
        """
        querykey = kwargs.get("querykey", None)
        query = self.model.select()
        if querykey:
            query_where = (User.username**f"%{querykey}%") | (
                User.email**f"%{querykey}%") | (User.tel**f"%{querykey}%") | (
                    User.nickname**f"%{querykey}%")
            query = query.where(query_where)

        query = query.order_by(User.id.desc()).offset(skip).limit(limit)
        # if not ref:
        #     query = query.dicts()
        lst = await pgdvm.execute(query)
        return lst


def init_super_user():
    """
    初始化超管
    """
    try:
        User.create(**{
            "username": FIRST_USER,
            "nickname": 'admin',
            "email": FIRST_USER,
            "password": get_password_hash(FIRST_USER_PASSWORD),
            "is_superuser": True,
            "is_active": True
        })
    except Exception as e:
        print("Has Init First User", e)


crud_user = CRUDUser(User)
crud_role = CRUDRole(UserRole)
