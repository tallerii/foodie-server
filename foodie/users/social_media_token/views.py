from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .serializers import FacebookTokenSerializer

from rest_framework.response import Response
 
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def facebookLoginView(request):
    serializer = FacebookTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = serializer.validated_data.get('token')

    strategy = load_strategy(request)
    backend = load_backend(strategy=strategy, name='facebook', redirect_uri=None)

    try:
        user = backend.do_auth(token)
        print(user)
        authenticated_user = backend.do_auth(token, user=user)
    except AuthForbidden as error:
        return Response({
            "error": "Invalid token",
            "details": str(error)
        }, status=status.HTTP_400_BAD_REQUEST)

    if authenticated_user and authenticated_user.is_active:
        response = {
            "token": authenticated_user.auth_token.key
        }
        return Response(status=status.HTTP_200_OK, data=response)
