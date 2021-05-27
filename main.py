import asyncio
import websockets

test = set()


async def server(web,p):
    test.add(web)
    try:

        async for message in web:
            for conn in test:
                    await conn.send(f'msg : '+message)
    finally:
        test.remove(web)


start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

