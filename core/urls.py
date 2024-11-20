# Third-party imports
from django.urls import path

# Local imports
from .views import UpdateChampions

urlpatterns = [
    path('update/champions', UpdateChampions.as_view(), name='update_champions'),
]