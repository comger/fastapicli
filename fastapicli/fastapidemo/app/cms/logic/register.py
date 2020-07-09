import requests

from cms.core import config
from cms.core.logger import logger


def register():
    modules = {
        "dataCheck": "测试功能",
    }

    resources = {
        "resource_project": "测试资源"
    }

    val = {
        "modules": modules,
        "resources": resources,
        "tenant_id": "1",
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "is_saas": True
    }
    try:
        r = requests.post(config.USERCENTER_HOST + "/api/v1/services/attr",
                          json=val)
        if len(r.json().get("modules", {})) == 0:
            logger.info(r.json())
    except Exception as e:
        logger.error(f"注册资源模块失败host:{config.USERCENTER_HOST},error:{e}")
