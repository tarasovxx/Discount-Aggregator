import requests
import xml.etree.ElementTree as ET

url = 'https://www.boardgamegeek.com/xmlapi2/hot?type=boardgame&discount=1'

response = requests.get(url)

if response.ok:
    root = ET.fromstring(response.text)
    games = root.findall('.//item')
    for game in games:
        name = game.find('name').attrib['value']
        year_published = game.find('yearpublished').attrib['value']
        print(f'Игра: {name}, Год выпуска: {year_published}')
else:
    print('Ошибка запроса')