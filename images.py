from PIL import Image
from os import path
from pathlib import PurePath
import Apikeys
import requests
import re
 

def do_things(query, options) -> bool:
    res = query_gis(query, options)
    if res:
        img_type, img_url = handle_gis_response(res)
        
        r = requests.get(img_url)
        
        file_name = PurePath('images/' + generate_emoji_name(query) + "." + generate_file_extension(img_type))
        open(file_name, 'wb').write(r.content)
        process_image(file_name, options)
        
        return True
            
        
def generate_file_extension(text) -> str:
    text = text.split('/')[1]
    return text

def generate_emoji_name(text) -> str:
    text = re.sub('[\W_]', '', text)
    return text

def process_image(image_name, options) -> None:
    base_image = Image.open(str(image_name))
    base_image.thumbnail((200,200))
    base_image.save('emoji/' + image_name.with_suffix('.png').name)

def query_gis(query, options=None) -> dict:
    try:   
        r = requests.get('https://customsearch.googleapis.com/customsearch/v1', params={
            'q': query,
            'num': 1,
            'start': 1,
            'imgSize': 'medium',
            'searchType': 'image',
            'key': Apikeys.key,
            'cx': Apikeys.cx,
        }, timeout=5)
    except requests.exceptions.HTTPError as e:
        print (e)
    response = r.json()
    return response

def handle_gis_response(req) -> tuple:
    #return (req['items'][0]['fileFormat'], req['items'][0]['image']['thumbnailLink'])
    return (req['items'][0]['fileFormat'], req['items'][0]['link'])
    
do_things('cat', None)