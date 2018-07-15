from __future__ import print_function

import grpc

import canal_data_pb2
import canal_data_pb2_grpc
import time


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = canal_data_pb2_grpc.SendingQuakeEventStub(channel)

    timestamp = 11010101212
    timestamp2 = 35445454545
    event_id = 3
    player_id = 1
    player_id2 = 0
    new_hp_value = 100
    injury_id = 4

    while True:
        response = stub.sendQuakeEventData(canal_data_pb2.QuakeEventMessage(
            timestamp=timestamp,
            event_id=event_id,
            player_id=player_id
        ))
        # print("Greeter client received: " + response.confirm)
        time.sleep(2)

        response2 = stub.sendInjuryData(canal_data_pb2.InjuryDataMessage(
            timestamp=timestamp2,
            injury_id=injury_id,
            player_id=player_id2,
            new_hp_value=new_hp_value
        ))
        # print("Greeter client received: " + response.confirm)
        time.sleep(2)


if __name__ == '__main__':
    run()