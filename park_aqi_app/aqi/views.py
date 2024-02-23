from django.shortcuts import render
import os
import requests
from regions import regions
from dotenv import load_dotenv
load_dotenv()
np_api_key = os.getenv("np_api_key")
epa_api = os.getenv("epa_api")
epa_api1 = os.getenv("epa_api2")


def aqi(request):
    state_code = request.GET.get('state_code', '')
    nps_url = f'https://developer.nps.gov/api/v1/parks?stateCode=${state_code}&api_key=${np_api_key}'

    try:
        response = requests.get(nps_url)
        response.raise_fro_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {'error': str(e)}

    return data