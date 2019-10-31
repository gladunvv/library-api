from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from users.serializers import CreateUserSerializer


class UserAuthToken(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user is not None:
                refresh = RefreshToken.for_user(user=user)
                response = serializer.data
                response['access'] = str(refresh.access_token)
                response['refresh'] = str(refresh)
            return Response(response, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogIn(ObtainAuthToken):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user=user)
        response = {
            'user_id': user.pk,
            'access': str(refresh.access_token),
            'refresh:': str(refresh),
        }
        return Response(response, status.HTTP_200_OK)


class UserDelete(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user = request.user
        request.user.delete()
        message = {
            'message': 'User {user} deleted successfully'.format(
                user=user.username,
            ),
        }
        return Response(message, status=status.HTTP_200_OK)
