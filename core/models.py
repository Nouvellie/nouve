# Third-party imports
from django.db import models
from django.utils.timezone import now


class Champion(models.Model):
    key = models.IntegerField(primary_key=True) 
    alias = models.CharField(max_length=100)  
    name = models.CharField(max_length=100)  
    title = models.CharField(max_length=200)
    blurb = models.TextField()
    atk = models.IntegerField()
    defense = models.IntegerField()
    magic = models.IntegerField()
    difficulty = models.IntegerField()
    load_img = models.URLField()  
    spar_img = models.URLField()  
    bbox_img = models.URLField()  
    tag_1 = models.CharField(max_length=50, blank=True)  
    tag_2 = models.CharField(max_length=50, blank=True)  
    partype = models.CharField(max_length=50)  

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'champion'
        managed = True


class APILog(models.Model):
    timestamp = models.DateTimeField(default=now)
    endpoint = models.CharField(max_length=255)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    error_message = models.TextField()
    status_code = models.IntegerField(blank=True, null=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.timestamp} - {self.endpoint} - {self.error_message[:50]}"

    class Meta:
        db_table = 'apilog'
        managed = True


class SummonerChart(models.Model):
    puuid
    gameName
    tagLine
    summonerid https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    accoundid https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    mastery_level https://la2.api.riotgames.com/lol/champion-mastery/v4/scores/by-puuid/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    high_champ_mastery https://la2.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q/top?count=3&api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    challenges_point https://la2.api.riotgames.com/lol/challenges/v1/player-data/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    accountdata https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    soloQ data https://la2.api.riotgames.com/lol/league/v4/entries/by-summoner/0EKlJo3T6T116BfaJudnTD6iRoeAWTmUKTYvx5f9fozd?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    profile icon https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/kzsMmNAH4GCNjPnprQ4pK5uuqHtVeiLXwPMtNxg_vgRvPeCmClTGZNBfDve1ginEnR_TccRqDE1o1Q?api_key=RGAPI-0cf603aa-48be-45dd-8a29-db889de48139
    class Meta:
        db_table = 'summonerchart'
        managed = True

