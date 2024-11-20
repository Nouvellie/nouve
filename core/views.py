# Standard library imports
import re
import requests as url_req
import traceback

# Third-party imports
from decouple import config
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import (
    save_api_logs,
    save_champion
)


class UpdateChampions(APIView):

    CHAMPIONS_URL = f"https://ddragon.leagueoflegends.com/cdn/"
    VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

    def get(self, request, format=None):
        try:
            version_response = url_req.get(self.VERSIONS_URL)
            if version_response.status_code == 200:
                version = version_response.json()[0]
            else:
                return Response({'err': 'DDragon website problems. (code 1)', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
            champions_response = url_req.get(f"{self.CHAMPIONS_URL}{version}/data/en_US/champion.json")
            if champions_response.status_code == 200:
                champions_list = champions_response.json()
            else:
                return Response({'err': 'DDragon website problems. (code 2)', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

            save_champion(champs=champions_list['data'], version=version)
            return Response({'status': True, 'err': ''}, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())
            print(full_traceback)
            save_api_logs(endpoint="http://127.0.0.1:8000/api/riot/update/champions", err=full_traceback, code=400)
            return Response({'err': 'Champion update failed.', 'status': False}, status=status.HTTP_400_BAD_REQUEST)


class UpdateSummoner(APIView):

    RIOT_KEY = config('RIOT_KEY', default='unsafe-secret-key')

    def post(self, request, format=None):
        try:
            summoner_name = request.data.get('summoner_name').replace('#', '/')
            region = request.data.get('region'
            )
            data1 = url_req.get(f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}?api_key={self.RIOT_KEY}").json()
            return Response(data1,status=status.HTTP_200_OK)
        except:
            # pass
            return Response(status=status.HTTP_400_BAD_REQUEST)