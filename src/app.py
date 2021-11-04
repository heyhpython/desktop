"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: app.py
@time: 2021/10/27 14:20
"""

import logging
import time

import aioredis
import uvicorn
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, JSONResponse
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src import admin
from src import device
import src.dialogue as _  # noqa
from src.config import Config
from src.constants import __config__, __template__, __static__
from src.signals import configured, after_boot
from src.errors import BaseResponseError
from src import clients
from src.utils.admin import app as admin_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(filename)s [line:%(lineno)s]  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%SS'
)
logger = logging.getLogger(__name__)

TORTOISE_ORM = {
    "connections": {
        "default": ""
    },
    "apps": {
        "models": {
            "models": ["src.admin.models", "aerich.models", "src.device.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Asia/Shanghai"
}

app = FastAPI()
config = Config('')
config.load_config(__config__)
TORTOISE_ORM['connections'] = config['DB_CONNECTIONS']
register_tortoise(app, config=TORTOISE_ORM, add_exception_handlers=True, generate_schemas=True)


@app.middleware("http")
async def after_request(req: Request, call_nxt):
    start_time = time.time()
    response = await call_nxt(req)
    process_time = time.time() - start_time
    logger.error(f'{req.method}: {req.url} duration {process_time * 1000 // 1} ms')
    return response


@app.exception_handler(BaseResponseError)
async def handle_exception(req, exc):
    logger.error(exc)
    return JSONResponse(
        status_code=exc.code,
        content=dict(
            code=exc.code,
            message=exc.message
        )
    )


@app.get("/admin")
async def index():
    return RedirectResponse(url="/admin/user/list")


@app.on_event("startup")
async def init_static():
    app.mount("/static", StaticFiles(directory=__static__), name="static")


@app.on_event("startup")
async def init_admin():
    redis = await aioredis.from_url(config['REDIS_URL'], encoding="utf8")
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[__template__],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[UsernamePasswordProvider(
            admin_model=admin.User,
            login_logo_url="https://preview.tabler.io/static/logo.svg"
        )],
        redis=redis,
        # admin_path='/admin/user/list'
    )


app.mount("/admin", admin_app)
admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)
configured.send(config)
after_boot.send(app)


if __name__ == '__main__':
    uvicorn.run(app, port=10000)