from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.helpers import error_response, success_response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)
from .serializers import CreateCredentialsSerailzier, GetCredentials
# Create your views here.


class CreateGetCredentialViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create_credential(self, request, **kwargs):
        serializer = CreateCredentialsSerailzier(
            data=request.data, context={'request': request, 'kwargs': kwargs})
        if not serializer.is_valid():
            if serializer.errors.get('password', None):
                error = serializer.errors.get('password')[0]
            elif serializer.errors.get('website', None):
                error = serializer.errors.get('website')[0]
            elif serializer.errors.get('password1', None):
                error = serializer.errors.get('password1')[0]
            elif serializer.errors.get('password2', None):
                error = serializer.errors.get('password2')[0]
            elif serializer.errors.get('credential', None):
                error = serializer.errors.get('credential')[0]
            else:
                error = serializer.errors

            return error_response(status=HTTP_400_BAD_REQUEST, msg="error occured", data=error)
        else:
            CreateCredentialsSerailzier.create(self, serializer.validated_data)
            return success_response(status=HTTP_200_OK,
                                    msg="API to save credentials",
                                    data=serializer.data)

    def get_credential(self, request, **kwargs):
        serializer = GetCredentials(
            data=request.query_params, context={'request': request, 'kwargs': kwargs})
        if not serializer.is_valid():

            return error_response(status=HTTP_400_BAD_REQUEST, msg="error occured", data=serializer.errors)
        else:
            return success_response(status=HTTP_200_OK,
                                    msg="API to get credentials",
                                    data=serializer.data)
