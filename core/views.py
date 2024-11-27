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

    def get(self, request, format=None):
        try:
            summoner_name_ = request.data.get('summoner_name').strip().replace('#', '/')
            region_ = request.data.get('region').strip()
            old_region_ = "la2"
            summoner_core_data = url_req.get(f"https://{region_}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name_}?api_key={self.RIOT_KEY}").json()

            puuid_ = summoner_core_data['puuid']
            game_name_ = summoner_core_data['gameName']
            tag_line_ = summoner_core_data['tagLine']

            summoner_core_full_data = url_req.get(f"https://{old_region_}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid_}?api_key={self.RIOT_KEY}").json()
            summoner_id_ = summoner_core_full_data['id']
            account_id_ = summoner_core_full_data['accountId']
            profile_icon_id_ = summoner_core_full_data['profileIconId']
            revision_date_ = summoner_core_full_data['revisionDate']
            summoner_level_ = summoner_core_full_data['summonerLevel']

            summoner_mastery_level = url_req.get(f"https://{old_region_}.api.riotgames.com/lol/champion-mastery/v4/scores/by-puuid/{puuid_}?api_key={self.RIOT_KEY}").json()

            summoner_challenges_data = url_req.get(f"https://{old_region_}.api.riotgames.com/lol/challenges/v1/player-data/{puuid_}?api_key={self.RIOT_KEY}").json()

            summoner_challenges_total = {
                'points': f"{summoner_challenges_data['totalPoints']['current']}/{summoner_challenges_data['totalPoints']['max']}",
                'rank': summoner_challenges_data['totalPoints']['level']
            }
            summoner_challenges_detail = {
                "VETERANCY": {
                    "points": f"{summoner_challenges_data['categoryPoints']['VETERANCY']['current']}/{summoner_challenges_data['categoryPoints']['VETERANCY']['max']}",
                    "rank": summoner_challenges_data['categoryPoints']['VETERANCY']['level'],
                },
                "IMAGINATION": {
                    "points": f"{summoner_challenges_data['categoryPoints']['IMAGINATION']['current']}/{summoner_challenges_data['categoryPoints']['IMAGINATION']['max']}",
                    "rank": summoner_challenges_data['categoryPoints']['IMAGINATION']['level'],
                },
                "EXPERTISE": {
                    "points": f"{summoner_challenges_data['categoryPoints']['EXPERTISE']['current']}/{summoner_challenges_data['categoryPoints']['EXPERTISE']['max']}",
                    "rank": summoner_challenges_data['categoryPoints']['EXPERTISE']['level'],
                },
                "COLLECTION": {
                    "points": f"{summoner_challenges_data['categoryPoints']['COLLECTION']['current']}/{summoner_challenges_data['categoryPoints']['COLLECTION']['max']}",
                    "rank": summoner_challenges_data['categoryPoints']['COLLECTION']['level'],
                },
                "TEAMWORK": {
                    "points": f"{summoner_challenges_data['categoryPoints']['TEAMWORK']['current']}/{summoner_challenges_data['categoryPoints']['TEAMWORK']['max']}",
                    "rank": summoner_challenges_data['categoryPoints']['TEAMWORK']['level'],
                }
            }

            summoner_high_mastery_data = url_req.get(f"https://{old_region_}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid_}/top?count=3&api_key={self.RIOT_KEY}").json()

            summoner_top_champs = {
                '1': {
                    'champId': summoner_high_mastery_data[0]['championId'],
                    'champLevel': summoner_high_mastery_data[0]['championLevel'],
                    'champPoints': summoner_high_mastery_data[0]['championPoints']
                },
                '2': {
                    'champId': summoner_high_mastery_data[1]['championId'],
                    'champLevel': summoner_high_mastery_data[1]['championLevel'],
                    'champPoints': summoner_high_mastery_data[1]['championPoints']
                },
                '3': {
                    'champId': summoner_high_mastery_data[2]['championId'],
                    'champLevel': summoner_high_mastery_data[2]['championLevel'],
                    'champPoints': summoner_high_mastery_data[2]['championPoints']
                }   
            }

            summoner_soloqueue_data = url_req.get(f"https://{old_region_}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id_}?api_key={self.RIOT_KEY}").json()[0]

            summoner_ranked = {
                'soloq': {
                    'rank': f"{summoner_soloqueue_data['tier']} {summoner_soloqueue_data['rank']}",
                    'points': summoner_soloqueue_data['leaguePoints'],
                    'wr': f"{int(round((summoner_soloqueue_data['wins']*100)/(summoner_soloqueue_data['wins']+summoner_soloqueue_data['losses']), 0))}%",
                    'wins': summoner_soloqueue_data['wins'],
                    'losses': summoner_soloqueue_data['losses'],
                    'veteran': summoner_soloqueue_data['veteran'],
                    'freshBlood': summoner_soloqueue_data['freshBlood'],
                    'hotStreak': summoner_soloqueue_data['hotStreak']
                },
                'flex': {
                    'rank': None,
                    'points': None,
                    'wr': None,
                    'wins': None,
                    'losses': None,
                    'veteran': None,
                    'freshBlood': None,
                    'hotStreak': None
                }
            }

            final_dict = {
                'puuid': puuid_,
                'nickname': f"{game_name_}#{tag_line_}",
                'region': region_,
                'summonerId': summoner_id_,
                'accountId': account_id_,
                'iconId': profile_icon_id_,
                'level': summoner_level_,
                'revisionDate': revision_date_,
                'elo': summoner_ranked,
                'challenges': summoner_challenges_total,
                'champions': summoner_top_champs
            }


            return Response(final_dict,status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())
            print(full_traceback)
            return Response(status=status.HTTP_400_BAD_REQUEST)