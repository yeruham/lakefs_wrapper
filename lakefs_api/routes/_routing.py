from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.routing import APIRoute


class NotImplementedRoute(APIRoute):
    def get_route_handler(self):
        async def route_handler(_: Request):
            raise HTTPException(status_code=501, detail='Not implemented')

        return route_handler