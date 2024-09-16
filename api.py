import requests

API_KEY = 'f049a2441fa5d88249abfc0dc9d21593'
BASE_URL = 'https://v3.football.api-sports.io/'

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

def get_fixtures(league_id, season):
    url = f"{BASE_URL}fixtures?league={league_id}&season={season}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_results(league_id, season):
    url = f"{BASE_URL}fixtures?league={league_id}&season={season}&status=FT"
    response = requests.get(url, headers=headers)
    return response.json()

def get_live_status():
    url = f"{BASE_URL}fixtures?live=all"
    response = requests.get(url, headers=headers)
    return response.json()

def get_euro_2024_fixtures():
    url = f"{BASE_URL}fixtures?league=4&season=2024"  # Пример ID лиги для Евро 2024
    response = requests.get(url, headers=headers)
    return response.json()

def get_champions_league_2024_2025_fixtures():
    url = f"{BASE_URL}fixtures?league=2&season=2024"  # Пример ID лиги для Лиги Чемпионов 2024/2025
    response = requests.get(url, headers=headers)
    return response.json()
