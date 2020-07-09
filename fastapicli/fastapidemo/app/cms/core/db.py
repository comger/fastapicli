import asyncio
import peewee_async
import peewee_asyncext
import psycopg2

from datetime import datetime
from playhouse.shortcuts import model_to_dict
from starlette.requests import Request
from peewee import DateTimeField, SQL, Query
from playhouse.postgres_ext import Model
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from cms.core import config
from cms.core.logger import Logger

logger = Logger().getLogger()


def create_database():
    ''' 创建数据库实例 '''
    conn = psycopg2.connect(database="postgres",
                            port=config.POSTGRES_PORT,
                            host=config.POSTGRES_SERVER,
                            user=config.POSTGRES_USER,
                            password=config.POSTGRES_PASSWORD)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    CREATE_DB = "CREATE DATABASE {}".format(config.POSTGRES_DB)
    try:
        cursor.execute(CREATE_DB)
    except psycopg2.errors.DuplicateDatabase:
        logger.info('psycopg2.errors.DuplicateDatabase,{} is exist'.format(
            config.POSTGRES_DB))
    except psycopg2.errors.UniqueViolation:
        logger.info('psycopg2.errors.UniqueViolation,{} is exist'.format(
            config.POSTGRES_DB))
    finally:
        cursor.close()
        conn.close()


def create_hstore_extension():
    conn = psycopg2.connect(dbname=config.POSTGRES_DB,
                            port=config.POSTGRES_PORT,
                            host=config.POSTGRES_SERVER,
                            user=config.POSTGRES_USER,
                            password=config.POSTGRES_PASSWORD)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    CREATE_DB = f"CREATE EXTENSION hstore"
    try:
        cursor.execute(CREATE_DB)
    except Exception as e:
        logger.info(e)
    finally:
        cursor.close()
        conn.close()


create_database()
create_hstore_extension()

pgdb = peewee_asyncext.PooledPostgresqlExtDatabase(
    config.POSTGRES_DB,
    host=config.POSTGRES_SERVER,
    port=config.POSTGRES_PORT,
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    register_hstore=True,
    max_connections=10,
)


class DataViewsionManage(peewee_async.Manager):
    async def create(self, obj, **data):
        # 生成创建ID, XX,XX 字段记录
        with pgdb.atomic():
            newObj = await super().create(obj, **data)
            return newObj

    async def update(self, obj, only=None):
        # 生成修改ID, XX,XX 字段的记录
        with pgdb.atomic():
            obj.updated_at = datetime.now()
            return await super().update(obj, only=only)

    async def delete(self,
                     obj,
                     recursive=False,
                     delete_nullable=False,
                     remove=False):
        # 生成删除ID 的记录
        with pgdb.atomic():
            if remove:
                return await super().delete(obj)
            obj.updated_at = datetime.now()
            obj.deleted_at = datetime.now()
            return await super().update(obj)

    async def execute_notdel(self, query, deleted_at=True):
        """Execute query asyncronously.
        """
        if deleted_at:
            query = query.where(SQL('deleted_at is null'))
        query = self._swap_database(query)
        return (await super().execute(query))

    async def count_notdel(self, query, deleted_at=True):
        """Perform *COUNT* aggregated query asynchronously.
        :return: number of objects in ``select()`` query
        """
        if deleted_at:
            query = query.where(SQL('deleted_at is null'))
        query = self._swap_database(query)
        return (await super().count(query, clear_limit=False))

    async def get_notdel(self, source_, *args, **kwargs):
        """Get the model instance.
        :param source_: model or base query for lookup
        Example::
            async def my_async_func():
                obj1 = await objects.get(MyModel, id=1)
                obj2 = await objects.get(MyModel, MyModel.id==1)
                obj3 = await objects.get(MyModel.select().where(MyModel.id==1))
        All will return `MyModel` instance with `id = 1`
        """
        await super().connect()

        if isinstance(source_, Query):
            query = source_
            model = query.model
        else:
            query = source_.select()
            model = source_

        conditions = list(args) + [(getattr(model, k) == v)
                                   for k, v in kwargs.items()]

        if conditions:
            query = query.where(*conditions)

        try:
            result = await self.execute_notdel(query)
            return list(result)[0]
        except IndexError:
            raise model.DoesNotExist


def get_session():
    """ 返回async peewee PostgresqlExtDatabase Manager 的"""
    loop = asyncio.get_event_loop()
    return DataViewsionManage(pgdb, loop=loop)


def depends_db(request: Request):
    """ 获取当前请求的上下文的postgresql db 异步管理实现 """
    return request.state.pgdb


class DBBaseModel(Model):
    class Meta:
        database = pgdb

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    deleted_at = DateTimeField(null=True)


def m2d(obj):
    """ peewee model 实现转dict 方法"""
    if type(obj) == peewee_async.AsyncQueryWrapper:
        return [model_to_dict(o, recurse=True) for o in obj]
    else:
        vals = model_to_dict(obj, recurse=True)
        for key, val in vals.items():
            if type(val) == bytes:
                vals[key] = str(val, encoding="utf8")
        return vals
