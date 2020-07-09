from fastapi import APIRouter
from cms.logic.common.crud import CRUDBase


async def list():
    # 如何知道，当前Model
    pass


async def func():
    pass


class URiRouter(APIRouter):
    def fetch(self, model: CRUDBase):
        """
        通过数据表操作类，自动添加CRUD HTTP Api
        """
        response_model = None
        tags = []
        dependencies = []
        summary = "列表查询"
        description = "列表查询、支持limit, skip"
        response_description = None
        responses = None
        methods = ["GET"]
        name = "list_objs"
        callbacks = []
        self.add_api_route(
            "/items",
            func,
            response_model=response_model,
            status_code=201,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            methods=methods,
            name=name,
            callbacks=callbacks,
        )
