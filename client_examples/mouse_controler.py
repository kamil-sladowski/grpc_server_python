from __future__ import print_function

import grpc

import canal_data_pb2
import canal_data_pb2_grpc
import time


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = canal_data_pb2_grpc.SendingMouseDataStub(channel)

    timestamp = 11010101212;
    move_x = 222;
    move_y = 3334;

    while True:
        response = stub.sendMouseData(canal_data_pb2.MouseMessage(
            move_x=move_x,
            move_y=move_y,
            timestamp=timestamp
        ))
        # print("Greeter client received: " + response.confirm)
        time.sleep(2)


if __name__ == '__main__':
    run()
