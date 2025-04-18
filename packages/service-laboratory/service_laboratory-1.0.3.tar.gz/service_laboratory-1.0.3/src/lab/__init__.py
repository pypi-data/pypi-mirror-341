"""
Configure litestar app with lab module:

from litestar import Litestar

from lab.auth.api import auth_router
from lab.auth.middleware import auth_middleware
from lab.core.database import alchemy
from lab.core.openapi import openapi_config

app = Litestar(
    route_handlers=[auth_router],
    plugins=[alchemy],
    middleware=[auth_middleware],
    openapi_config=openapi_config,
)
"""