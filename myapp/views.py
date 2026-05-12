import json

import sentry_sdk
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inventory
from .serializers import InventorySerializer

InventoryData = [{"name": "wrench", "count": 1},
                 {"name": "nails", "count": 1},
                 {"name": "hammer", "count": 1}]


def find_in_inventory(itemId):
    for item in InventoryData:
        if item['name'] == itemId:
            return item
    raise Exception("Item : " + itemId + " not in inventory ")


def process_order(cart):
    global InventoryData
    tempInventory = InventoryData
    for item in cart:
        itemID = item['id']
        inventoryItem = find_in_inventory(itemID)
        if inventoryItem['count'] <= 0:
            raise Exception("Not enough inventory for " + itemID)
        else:
            inventoryItem['count'] -= 1
            print('Success: ' + itemID + ' was purchased, remaining stock is ' + str(inventoryItem['count']))
    InventoryData = tempInventory


class SentryContextMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.body:
            body_unicode = request.body.decode('utf-8')
            order = json.loads(body_unicode)
            sentry_sdk.set_user({"email": order["email"]})

        transactionId = request.headers.get('X-Transaction-ID')
        sessionId = request.headers.get('X-Session-ID')

        if transactionId:
            sentry_sdk.set_tag("transaction_id", transactionId)
        if sessionId:
            sentry_sdk.set_tag("session-id", sessionId)
        if Inventory:
            sentry_sdk.set_extra("inventory", InventoryData)

        return super().dispatch(request, *args, **kwargs)


class InventoreyView(SentryContextMixin, APIView):

    def get(self, request):
        results = InventorySerializer(InventoryData, many=True).data
        return Response(results)

    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        order = json.loads(body_unicode)
        cart = order['cart']
        process_order(cart)
        return Response(InventoryData)


class HandledErrorView(APIView):
    def get(self, request):
        try:
            '2' + 2
        except Exception as err:
            sentry_sdk.capture_exception(err)
        return Response()


class UnHandledErrorView(APIView):
    def get(self, request):
        obj = {}
        obj['keyDoesntExist']
        return Response()
