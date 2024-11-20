# Third-party imports
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Local imports
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
