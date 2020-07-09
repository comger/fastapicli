"""
author comger@gmail.com
统一异常处理机制
"""
import logging
import traceback
from cms.core import config
from starlette.responses import HTMLResponse


log = logging.getLogger()


class ErrorHandler:

    @classmethod
    def handler(cls, e: Exception, ttype, tvalue, ttraceback):

        if config.DEBUG:
            log.error(e)
            content_html = f"<p>{ttype}</p>"
            for info in traceback.format_tb(ttraceback):
                content_html += f"<p>{info}</p>"

            html = f"<html><body><h2>{tvalue}</h2>{content_html}</body></html>"
            return HTMLResponse(content=html)
        else:
            msg = cls.get_error(ttype, e=e)
            return HTMLResponse(content=f"{msg},请联系开发人员")

    @classmethod
    def get_error(cls, ttype, e=None):
        name = ttype.__name__

        if name.endswith("DoesNotExist"):
            return "你输入的资源不存在"
        elif name.endswith("UniqueViolation"):
            return "你输入的资源已存在"
        elif name.endswith("IntegrityError"):
            return e.__str__()
        elif name.endswith("ForeignKeyViolation"):
            return "你输入的外键ID不存在"
        else:
            return "未知异常"
