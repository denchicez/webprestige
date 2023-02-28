import asyncio

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from handlers.stoloto import *

stoloto = APIRouter()


@stoloto.get("/stoloto/top3")
async def get_top3() -> HTMLResponse:
    while True:
        try:
            table = await stoloto_top3_table()
            break
        except:
            await asyncio.sleep(10)
    return HTMLResponse(content=convert_arr_table_to_html(table), status_code=200)


@stoloto.get("/stoloto/keno2")
async def get_keno2() -> HTMLResponse:
    while True:
        try:
            table = await stoloto_keno2_table()
            break
        except:
            await asyncio.sleep(10)
    return HTMLResponse(content=convert_arr_table_to_html(table), status_code=200)


@stoloto.get("/stoloto/bigloto")
async def get_keno2() -> HTMLResponse:
    while True:
        try:
            table = await stoloto_bigloto_table()
            break
        except:
            await asyncio.sleep(10)
    return HTMLResponse(content=convert_arr_table_to_html(table), status_code=200)
