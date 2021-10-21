import sys
import asyncio
import logging

import grpc
import app_pb2
import app_pb2_grpc

PORT = 50052

class Greeter(app_pb2_grpc.GreeterServicer):
    async def SayHello(
        self, 
        request: app_pb2.HelloRequest,
        context: grpc.aio.ServicerContext,
    ) -> app_pb2.HelloReply:
        client_md = context.invocation_metadata()
        print("CLIENT-METADATA >", client_md)

        await context.send_initial_metadata([
            ("md-initial-a", "abc123"),
            ("md-initial-b", "def456"),
        ])
        context.set_trailing_metadata([
            ("md-trailing-a", "789ghi"),
        ])
        return app_pb2.HelloReply(
            message="Hello, %s!" % request.name
        )

async def serve() -> None:
    # Create the server
    server = grpc.aio.server()
    
    # Add the service
    app_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # Add the port
    addr = f"[::]:{PORT}"
    server.add_insecure_port(addr)
    logging.info(f"Starging server on {addr}")
    
    # Start the server
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
    )
    asyncio.run(serve())
