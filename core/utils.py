# Standard library imports
import pandas as pd

# Third-party imports
from .models import (
    APILog,
    Champion
)

def save_api_logs(endpoint, data=None, err="", code=None):
    APILog.objects.create(
        endpoint=endpoint,
        request_data=data,
        error_message=str(err),
        status_code=getattr(code, 'status_code', None)
    )


def save_champion(champs, version):
    champions_list_data = []
    for _, info in champs.items():
        core_data = {
            'key': int(info['key']),
            'alias': info['id'].capitalize(),
            'name': info['name'].capitalize(), # ?
            'title': info['title'].title(),
            'blurb': info['blurb'],
            'atk': info['info']['attack'],
            'def': info['info']['defense'],
            'mag': info['info']['magic'],
            'dif': info['info']['difficulty'],
            'load_img': f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{info['id']}_0.jpg",
            'spar_img': f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{info['id']}_0.jpg",
            'bbox_img': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{info['id']}.png",
            'tag_1': info['tags'][0] if len(info.get('tags', [])) > 0 else "",
            'tag_2': info['tags'][1] if len(info.get('tags', [])) > 1 else "",
            'partype': info['partype']
        }
        champions_list_data.append(core_data)
    
    df = pd.DataFrame(champions_list_data).sort_values(by='key', ascending=True)
    for _, row in df.iterrows():
        Champion.objects.update_or_create(
            key=row['key'],  
            defaults={
                'alias': row['alias'],
                'name': row['name'],
                'title': row['title'],
                'blurb': row['blurb'],
                'atk': row['atk'],
                'defense': row['def'],
                'magic': row['mag'],
                'difficulty': row['dif'],
                'load_img': row['load_img'],
                'spar_img': row['spar_img'],
                'bbox_img': row['bbox_img'],
                'tag_1': row['tag_1'],
                'tag_2': row['tag_2'],
                'partype': row['partype']
            }
        )

