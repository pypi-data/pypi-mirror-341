from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from mm_base6.core.db import DValue
from mm_base6.server.cbv import cbv
from mm_base6.server.deps import BaseView

router: APIRouter = APIRouter(prefix="/api/system/dvalues", tags=["system"])


@cbv(router)
class CBV(BaseView):
    @router.get("/toml", response_class=PlainTextResponse)
    async def get_dvalues_as_toml(self) -> str:
        return self.core.system_service.export_dvalue_as_toml()

    @router.get("/{key}/toml", response_class=PlainTextResponse)
    async def get_dvalue_field_as_toml(self, key: str) -> str:
        return self.core.system_service.export_dvalue_field_as_toml(key)

    @router.get("/{key}/value")
    async def get_dvalue_value(self, key: str) -> object:
        return self.core.system_service.get_dvalue_value(key)

    @router.get("/{key}")
    async def get_dvalue_key(self, key: str) -> DValue:
        return await self.core.db.dvalue.get(key)
