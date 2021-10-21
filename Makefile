default: proto fmt

env-setup:
	pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: proto
proto:
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/app.proto

.PHONY: fmt
fmt:
	black client protos server

.PHONY: client
client:
	python client.py

.PHONY: server
server:
	python server.py
