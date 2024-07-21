from io import BytesIO

import aiohttp


async def http_get(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def http_post(url: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url,
            json=data,
        ) as response:
            response.raise_for_status()
            return await response.json()


async def http_post_file(url: str, data_bytes_io: BytesIO) -> dict:
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field(
            name="file",
            value=data_bytes_io,
            content_type="application/octet-stream",
        )
        async with session.post(
            url=url,
            data=data,
        ) as response:
            response.raise_for_status()
            return await response.json()
