from concurrent import futures
import time

import grpc

import canal_data_pb2 as canal_data_pb2
import canal_data_pb2_grpc as canal_data_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ImageDataSample:
    def __init__(self, negative, neutral, positive, black_screen, image_name):
        self.negative = negative
        self.neutral = neutral
        self.positive = positive
        self.black_screen = black_screen
        self.image_name = image_name


class MouseDataSample:
    def __init__(self, move_x, move_y, timestamp):
        self.move_x = move_x
        self.move_y = move_y
        self.timestamp = timestamp


class InjurySample:
    def __init__(self, timestamp, injury_id, player_id, new_hp_value):
        self.timestamp = timestamp
        self.player_id = player_id
        self.injury_id = injury_id
        self.new_hp_value = new_hp_value


class QuakeEventSample:
    def __init__(self, timestamp, event_id, player_id, injury_id, new_hp_value):
        self.timestamp = timestamp
        self.event_id = event_id
        self.player_id = player_id
        self.injury_id = injury_id
        self.new_hp_value = new_hp_value


class SendingImageData(canal_data_pb2_grpc.SendingImageDataServicer):
    def __init__(self, image_data_sample):
        self.imageDataSample = image_data_sample

    def sendImageData(self, request, context):
        self.imageDataSample.negative = request.negative
        self.imageDataSample.neutral = request.neutral
        self.imageDataSample.positive = request.positive
        self.imageDataSample.black_screen = request.black_screen
        self.imageDataSample.image_name = request.image_name

        print("[IMAGE - got image data]")
        print("[IMAGE DATA]: name: ", self.imageDataSample.image_name)
        print("[IMAGE DATA]: is negative? ", self.imageDataSample.negative)
        print("[IMAGE DATA]: is neutral? ", self.imageDataSample.neutral)
        print("[IMAGE DATA]: is positive? ", self.imageDataSample.positive)
        print("[IMAGE DATA]: is black? ", self.imageDataSample.black_screen)

        return canal_data_pb2.ServerConfirmation(confirm=b"1")


class SendingMouseData(canal_data_pb2_grpc.SendingMouseDataServicer):
    def __init__(self, mouse_data_sample):
        self.mouse_data_sample = mouse_data_sample

    def sendMouseData(self, request, context):
        self.mouse_data_sample.move_x = request.move_x
        self.mouse_data_sample.move_y = request.move_y
        self.mouse_data_sample.timestamp = request.timestamp
        print("[MOUSE - got data]")
        print("[MOUSE DATA]: timestamp: ", self.mouse_data_sample.timestamp)
        print("[MOUSE DATA]: x: ", self.mouse_data_sample.move_x)
        print("[MOUSE DATA]: y: ", self.mouse_data_sample.move_y)

        return canal_data_pb2.ServerConfirmation(confirm=b"1")


class SendingQuakeEvent(canal_data_pb2_grpc.SendingQuakeEventServicer):
    def __init__(self, quake_event_sample):
        self.quake_event_sample = quake_event_sample

    def sendQuakeEventData(self, request, context):
        self.quake_event_sample.timestamp = request.timestamp
        self.quake_event_sample.event_id = request.event_id
        self.quake_event_sample.player_id = request.player_id
        print("[QUAKE EVENT - got data]")
        print("[QUAKE DATA]: timestamp: ", self.quake_event_sample.timestamp)
        print("[QUAKE DATA]: event_id: ", self.quake_event_sample.event_id)
        print("[QUAKE DATA]: player_id: ", self.quake_event_sample.player_id)

        return canal_data_pb2.ServerConfirmation(confirm=b"1")

    def sendInjuryData(self, request, context):
        self.quake_event_sample.timestamp = request.timestamp
        self.quake_event_sample.injury_id = request.injury_id
        self.quake_event_sample.player_id = request.player_id
        self.quake_event_sample.new_hp_value = request.new_hp_value
        print("[INJURY - got data]")
        print("[INJURY DATA]: timestamp: ", self.quake_event_sample.timestamp)
        print("[INJURY DATA]: injury_id: ", self.quake_event_sample.injury_id)
        print("[INJURY DATA]: player_id: ", self.quake_event_sample.player_id)
        print("[INJURY DATA]: new_hp_value: ", self.quake_event_sample.new_hp_value)

        return canal_data_pb2.ServerConfirmation(confirm=b"1")



def server():
    image_sample = ImageDataSample(False, False, False, False, "noName")
    mouse_sample = MouseDataSample(0, 0, 0)
    quake_sample = QuakeEventSample(100, 1, 0, 2, 60)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    canal_data_pb2_grpc.add_SendingImageDataServicer_to_server(SendingImageData(image_sample), server)
    canal_data_pb2_grpc.add_SendingMouseDataServicer_to_server(SendingMouseData(mouse_sample), server)
    canal_data_pb2_grpc.add_SendingQuakeEventServicer_to_server(SendingQuakeEvent(quake_sample), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    server()

