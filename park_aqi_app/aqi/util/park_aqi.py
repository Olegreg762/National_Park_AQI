import requests
import os
from regions import regions
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    def park_data(state_code):
        np_api_key = os.getenv("np_api_key")
        epa_api = os.getenv("epa_api")
        epa_api1 = os.getenv("epa_api1")
        try:
            nps_url = f"https://developer.nps.gov/api/v1/parks?stateCode={state_code}&api_key={np_api_key}"
            nps_response = requests.get(nps_url)
            nps_response.raise_for_status()
            nps_data = nps_response.json()
            i = 0
            while i < len(nps_data['data']):
                if nps_data["data"][i]["designation"] == "National Historic Trail":
                    del nps_data["data"][i]
                else:
                    epa_url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={nps_data['data'][i]['latitude']}&longitude={nps_data['data'][i]['longitude']}&distance=50&API_KEY={epa_api}"
                    epa_response = requests.get(epa_url)
                    epa_response.raise_for_status()

                    if epa_response.status_code != 200:
                        epa_url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={nps_data['data'][i]['latitude']}&longitude={nps_data['data'][i]['longitude']}&distance=50&API_KEY={epa_api1}"
                        print('epakey2')
                        epa_response = requests.get(epa_url)
                        epa_response.raise_for_status()
                    epa_data = epa_response.json()

                    if epa_data == []:
                        aqi_data = {
                        "aqi": "NO DATA AVALIABLE",
                        "quality_name": "NO DATA"
                        }
                        
                    else:   
                        aqi_data = {
                        "aqi": epa_data[0]["AQI"],
                        "quality_name": epa_data[0]["Category"]["Name"]
                        }
                    nps_data["data"][i]["EPA_AQI"] = aqi_data
                    i += 1

        except requests.exceptions.RequestException as e:
            nps_data = {'error': str(e)}

        return nps_data




