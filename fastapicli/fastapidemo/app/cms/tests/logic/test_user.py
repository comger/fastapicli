import sys
import os
path = os.getcwd()
sys.path.append(path)

from cms.logic.common.user import crud_user, UserCreate, User
from cms.core.db import get_session, m2d
from cms.core.logger import logger


async def __test_curd():
    pgdvm = get_session()
    obj_in = UserCreate(username="comger",
                        nickname="comger",
                        password="123456",
                        email="comger@gmail.com")

    obj = await crud_user.create(pgdvm=pgdvm, obj_in=obj_in)
    obj1 = await crud_user.get(pgdvm, obj.id)
    assert obj == obj1


async def __test_m2d():
    pgdvm = get_session()
    lst = await crud_user.get_multi(pgdvm=pgdvm)
    data = m2d(lst)

    assert len(data) == 0