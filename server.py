import threading
import time
from concurrent import futures

import grpc
from loguru import logger

import ping_pb2
import ping_pb2_grpc


class Listener(ping_pb2_grpc.PingPongServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.message = ""

    def ping(self, request, context):
        self.message = request.message
        print(f"Client says: {self.message}")

        return ping_pb2.Pong(message=f"Server said: {self.message}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ping_pb2_grpc.add_PingPongServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:8080")
    server.start()

    while True:
        try:
            logger.debug(f"Server Running, threads: {threading.active_count()}")
            time.sleep(5)

        except KeyboardInterrupt:
            logger.critical("KILLSIG received")
            server.stop(0)
            break


if __name__ == "__main__":
    serve()
