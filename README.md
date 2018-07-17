# grpc_server_python

###Run:
$ pip install grpcio-tools


$ pip install googleapis-common-protos


python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. canal_data.proto

$ python server
