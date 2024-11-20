# Third-party imports
from django.urls import path

# Local imports
from .views import (
    UpdateChampions,
    UpdateSummoner
)

urlpatterns = [
    path('update/champions', UpdateChampions.as_view(), name='update_champions'),
    path('update/summoner', UpdateSummoner.as_view(), name='update_summoner')    
]