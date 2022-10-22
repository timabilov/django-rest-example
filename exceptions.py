from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response


def custom_drf_exception_handler(exc, context):
    print (exc, context)
    response = exception_handler(exc, context)
    if response:
        return response
    else:
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
