import sys
import os
path = os.getcwd()
sys.path.append(path)

from cms.core.logger import logger, Logger


def __test_log():
    logger = Logger("autotest").getLogger()
    logger.debug("debug test")
    logger.info("info test")

    logger = Logger().getLogger()
    logger.info("info test")
    logger.debug("debug test")


def __test_db():
    # 自动创建数据库
    # 按定义创建表
    from peewee import CharField, IntegerField
    from playhouse.postgres_ext import BinaryJSONField, ArrayField, HStoreField
    from playhouse.shortcuts import model_to_dict
    from cms.core.db import pgdb, DBBaseModel

    class DemoModel(DBBaseModel):
        name = CharField()
        status = IntegerField()
        source = BinaryJSONField()
        actions = ArrayField(CharField)
        video_set = HStoreField(null=True, default={})

    pgdb.create_tables([DemoModel])
    DemoModel.create(name="test",
                     status=1,
                     source=dict(tt=11, dd=22),
                     actions=["aa", "bb"]
                     )

    lst = list(DemoModel.select().execute())
    for item in lst:
        logger.info(model_to_dict(item))

    count = DemoModel.select().count()
    DemoModel.delete().execute()

    assert count == 1
