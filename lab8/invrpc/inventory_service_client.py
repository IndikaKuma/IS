from __future__ import print_function
import logging

import grpc

import inventory_service_pb2
import inventory_service_pb2_grpc


def generate_product_list():
    yield inventory_service_pb2.ProductType(type="Laptop")
    yield inventory_service_pb2.ProductType(type="Phone")


def run():
    channel = grpc.insecure_channel('localhost:5005')
    stub = inventory_service_pb2_grpc.InventoryServiceStub(channel)
    response = stub.GetProductQuantity(inventory_service_pb2.ProductType(type="Laptop"))
    logging.info("Quantity for Product Type Laptop : " + str(response.amount))

    product_list = generate_product_list()
    response = stub.GetStockSummary(product_list)
    logging.info("Quantity for Product Type Laptop : " + str(response.productStocks["Laptop"].amount))
    logging.info("Quantity for Product Type Phone : " + str(response.productStocks["Phone"].amount))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()
