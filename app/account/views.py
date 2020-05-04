from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LogInSerializer, UserSerializer


class SignUpView(generics.CreateAPIView):
    """ Create a new user """

    authentication_classes = ()
    permission_classes = ()

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    """Create a new auth token for user"""

    authentication_classes = ()
    permission_classes = ()

    serializer_class = LogInSerializer
