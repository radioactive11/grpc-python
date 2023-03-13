import os
import time

import grpc
from loguru import logger

import ping_pb2
import ping_pb2_grpc

MESSAGES = [
    "I like shiny things",
    "But I will marry you",
    "with paper rings",
]


def message_iter():
    for message in MESSAGES:
        yield ping_pb2.Ping(client_message=message)

    time.sleep(2)


def run():
    message: str = ""
    pid = os.getpid()

    with grpc.insecure_channel("[::]:8080") as channel:
        stub = ping_pb2_grpc.PingPongServiceStub(channel)
        try:

            response = stub.client_stream(message_iter())

            message_from_server = response.num_pings
            logger.info(f"Server said there were {message_from_server} messages")

        except KeyboardInterrupt as ki:
            logger.critical("Bye!")
            channel.unsubscribe(channel.close())
            exit()


if __name__ == "__main__":
    run()
