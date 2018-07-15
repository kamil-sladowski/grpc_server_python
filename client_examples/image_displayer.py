from __future__ import print_function

import grpc

import canal_data_pb2
import canal_data_pb2_grpc
import time


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = canal_data_pb2_grpc.SendingImageDataStub(channel)

    negative = True
    neutral = False
    positive = False
    black_screen = False
    image_name = b"Ne082"

    while True:
        response = stub.sendImageData(canal_data_pb2.ImageDataMessage(negative=negative,
                                                                      neutral=neutral,
                                                                      positive=positive,
                                                                      black_screen=black_screen,
                                                                      image_name=image_name))
        # print("Greeter client received: " + response.confirm)
        time.sleep(2)


if __name__ == '__main__':
    run()
