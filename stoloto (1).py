from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from handlers.stoloto import *

stoloto = APIRouter()


@stoloto.get("/stoloto/top3")
async def get_top3() -> HTMLResponse:
    table = await stoloto_top3_table()
    return HTMLResponse(content=convert_arr_table_to_html(table), status_code=200)
