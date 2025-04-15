#!/usr/bin/env Python
# -*- coding: utf-8 -*-
import os

from meutils.pipe import *
from meutils.caches import rcache
from meutils.decorators.retry import retrying


@rcache(ttl=60 - 5)
@retrying()
async def get_proxy_list():
    secret_id = os.getenv("KDLAPI_SECRET_ID") or "owklc8tk3ypo00ohu80o"
    signature = os.getenv("KDLAPI_SIGNATURE") or "8gqqy7w64g7uunseaz9tcae7h8saa24p"
    url = f"https://dps.kdlapi.com/api/getdps/?secret_id={secret_id}&signature={signature}&num=1&pt=1&format=json&sep=1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        proxy_list = response.json().get('data').get('proxy_list')

        return [f"http://{proxy}" for proxy in proxy_list]


async def get_one_proxy():
    proxy_list = await get_proxy_list()
    return proxy_list[-1]


if __name__ == '__main__':
    arun(get_proxy_list())
