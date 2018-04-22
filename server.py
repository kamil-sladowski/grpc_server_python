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
    def __init__(self, pos_x, pos_y, delta, active):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.delta = delta
        self.active = active


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
        self.mouse_data_sample.pos_x = request.pos_x
        self.mouse_data_sample.pos_y = request.pos_y
        self.mouse_data_sample.delta = request.delta
        self.mouse_data_sample.active = request.active
        print("[MOUSE - got data]")

        return canal_data_pb2.ServerConfirmation(confirm=b"1")


def serve():
    image_sample = ImageDataSample(False, False, False, False, "noName")
    mouse_sample = MouseDataSample(0, 0, 0, 0)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    canal_data_pb2_grpc.add_SendingImageDataServicer_to_server(SendingImageData(image_sample), server)
    canal_data_pb2_grpc.add_SendingMouseDataServicer_to_server(SendingMouseData(mouse_sample), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
