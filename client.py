import asyncio

import aiohttp


async def main():
    client = aiohttp.ClientSession()

    # response = await client.post(
    #     "http://127.0.0.1:8080/user",
    #     json={"name": "user_my", "password": "TGFet53ggr54%"},
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.get(
    #     "http://127.0.0.1:8080/user/7",
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.patch(
    #     "http://127.0.0.1:8080/user/7",
    #     json={"name": "new_user",},
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.get(
    #     "http://127.0.0.1:8080/user/4",
    # )
    # print(response.status)
    # print(await response.json())
    
    # await client.close()

    # response = await client.delete(
    #     "http://127.0.0.1:8080/user/7",
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.get(
    #     "http://127.0.0.1:8080/user/4",
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.post(
    # "http://127.0.0.1:8080/sticker",
    # json={"name": "new_sticker4", "description":"opisanie_1", "owner":8},
    # )
    # print(response.status)
    # print(await response.json())

    response = await client.get(
        "http://127.0.0.1:8080/sticker/7",
    )
    print(response.status)
    print(await response.json())

    # response = await client.patch(
    #     "http://127.0.0.1:8080/sticker/6",
    #     json={"name": "new_sticker_1",},
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.delete(
    #     "http://127.0.0.1:8080/sticker/5",
    # )
    # print(response.status)
    # print(await response.json())

    # #
    await client.close()


asyncio.run(main())
