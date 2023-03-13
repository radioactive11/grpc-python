import threading
import time
from concurrent import futures

import grpc
from loguru import logger

import ping_pb2
import ping_pb2_grpc


class Listener(ping_pb2_grpc.PingPongServiceServicer):
    def ping(self, request, context):
        self.message = request.client_message
        print(f"Client says: {self.message}")

        return ping_pb2.Pong(server_message=f"Server said: {self.message}")

    def client_stream(self, request_iterator, context):
        self.sum = 0
        for item in request_iterator:
            print(f"Client says: {item.client_message}")
            self.sum += 1

        return ping_pb2.NumPings(num_pings=self.sum)


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
