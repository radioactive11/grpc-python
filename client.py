import os
import time

import grpc
from loguru import logger

import ping_pb2
import ping_pb2_grpc


def run():
    message: str = ""
    pid = os.getpid()

    with grpc.insecure_channel("[::]:8080") as channel:
        stub = ping_pb2_grpc.PingPongServiceStub(channel)

        while True:
            try:
                message = input("Enter message: ")
                response = stub.ping(ping_pb2.Ping(client_message=message))

                message_from_server = response.server_message
                logger.info(message_from_server)

                time.sleep(0.01)

            except KeyboardInterrupt as ki:
                logger.critical("Bye!")
                channel.unsubscribe(channel.close())
                exit()


if __name__ == "__main__":
    run()
