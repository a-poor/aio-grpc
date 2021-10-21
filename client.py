import sys
import asyncio
import logging

import grpc
import app_pb2
import app_pb2_grpc


PORT = 50052

async def run() -> None:
    async with grpc.aio.insecure_channel(f"localhost:{PORT}") as channel:
        stub = app_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(
            app_pb2.HelloRequest(name='World')
        )
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    asyncio.run(run())
