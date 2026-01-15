# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(Create_Order) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import json
import azure.functions as func
import logging
import azure.durable_functions as df
from datetime import datetime
import time

Create_Order = df.Blueprint()

# An HTTP-Triggered Function with a Durable Functions Client binding
@Create_Order.route(route="orchestrators/{functionName}/{orderid}")
@Create_Order.durable_client_input(client_name="client")
async def hello_orchestration_starter(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    order_id = req.route_params.get('orderid') # Get our OrderId
    instance_id = await client.start_new(function_name, None, {"orderid": order_id}) # Passing OrderId to the Orchestrator
    response = client.create_check_status_response(req, instance_id)
    return response

# Orchestrator
@Create_Order.orchestration_trigger(context_name="context")
def hello_orchestration_orchestrator(context):

    input_data = context.get_input()
    order_id = input_data.get("orderid")

    result1 = yield context.call_activity("activity_accept_order", order_id)
    context.set_custom_status(result1)

    result2 = yield context.call_activity("activity_pick_order", order_id)
    context.set_custom_status(result2)

    result3 = yield context.call_activity("activity_despatch_order", order_id)
    context.set_custom_status(result3)

    return result3["trackingref"]

# Activity
@Create_Order.activity_trigger(input_name="orderid")
def activity_accept_order(orderid: str):
    # ORDER VALIDATION
    time.sleep(15)
    return {"status": "ACCEPTED", "orderid":f"{orderid}"}

@Create_Order.activity_trigger(input_name="orderid")
def activity_pick_order(orderid: str):
    # ORDER PICKING PROCESS
    time.sleep(15)
    return {"status": "PICKED", "orderid":f"{orderid}"}

@Create_Order.activity_trigger(input_name="orderid")
def activity_despatch_order(orderid: str):
    # ORDER DESPATCH PROCESS
    time.sleep(15)
    return {"status": "DESPATCHED", "orderid":f"{orderid}","trackingref": "FEDEX-3450-2323231"}