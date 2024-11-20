# Third-party imports
from django.urls import path

# Local imports
from .views import UserCreateView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
]