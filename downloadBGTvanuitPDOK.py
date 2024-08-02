import requests
import json
import os
import time

# Dit Python-script downloadt (alle) Basisregistratie Grootschalige Topografie (BGT)-gegevens van PDOK voor een bepaald gebied gedefinieerd door een polygoon.
# Zowel de coördinaten voor de polygoon als het formaat van de output ('citygml', 'gml', 'json') kunnen worden aangepast.
# Het script zorgt ervoor dat de lijst met op te vragen features altijd actueel is door eerst een lijst van de beschikbare gegevens op te halen.
# Het script doorloopt de volgende drie stappen:
# 1. Creëer een downloadverzoek en ontvang een 'download request ID'.
# 2. Controleer de status van het downloadverzoek totdat het voltooid is.
# 3. Downloadt het bestand naar de opgegeven locatie (voor nu 'C:/temp/downloaded_file.zip').

# Basis-URL voor de API
base_url = 'https://api.pdok.nl/lv/bgt/download/v1_0/full/custom'

# Haal de beschikbare featuretypes op van de PDOK BGT API 
def get_featuretypes():
    dataset_url = "https://api.pdok.nl/lv/bgt/download/v1_0/dataset"
    response = requests.get(dataset_url)
    
    if response.status_code == 200:
        data = response.json()
        featuretypes = [item['featuretype'] for item in data['timeliness']]
        return featuretypes
    else:
        print(f"Fout bij het ophalen van featuretypes: {response.status_code}")
        return []

# Stap 1: Verstuur een POST-aanroep om een downloadverzoek aan te maken (aanmaken 'download request id')
def create_download_request():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Haal dynamisch de lijst met featuretypes op
    featuretypes = get_featuretypes()

    payload = {
        "featuretypes": featuretypes,
        # qua format kun je 'citygml' vervangen door 'gml' en 'json'. Heb ik overigens niet op getest.
        "format": "citygml",
        # onderstaande coordinaten tonen een polygoon. Merk op dat de polygoon gesloten is (het laatste coordinaat is gelijk aan het eerste)
        "geofilter": "POLYGON((229109.0 570764.5, 231744.308 569600.046, 231671.36 575662.81, 224312.8 574798.8, 229109.0 570764.5))"
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 202:
        response_data = response.json()
        download_request_id = response_data.get('downloadRequestId')
        print(f"Download Request ID: {download_request_id}")
        return download_request_id
    else:
        print(f"Fout bij verzoek: {response.status_code}")
        print(response.text)
        return None

# Stap 2: Controleer de status van het downloadverzoek
def check_status(download_request_id):
    status_url = f'{base_url}/{download_request_id}/status'

    while True:
        response = requests.get(status_url)
        
        if response.status_code == 200:
            response_data = response.json()
            progress = response_data.get('progress')
            status = response_data.get('status')
            print(f"Progress: {progress}%")
            print(f"Status: {status}")
            
            if status == 'COMPLETED':
                download_link = response_data['_links']['download']['href']
                return download_link
            elif status == 'FAILED':
                print("Downloadaanvraag mislukt.")
                return None
            
        elif response.status_code == 201:
            response_data = response.json()
            download_link = response_data['_links']['download']['href']
            return download_link
        
        elif response.status_code == 404:
            print("DownloadRequestId niet gevonden.")
            return None
        elif response.status_code == 429:
            print("Te veel verzoeken. Probeer het later opnieuw.")
            time.sleep(60)  # Wacht een minuut en probeer het opnieuw
        elif response.status_code == 500:
            print("Interne serverfout. Probeer het later opnieuw.")
            return None
        else:
            print(f"Onverwachte fout: {response.status_code}")
            print(response.text)
            return None

# Stap 3: Download het bestand
def download_file(download_link):
    download_url = f'https://api.pdok.nl{download_link}'
    download_path = 'C:/temp/downloaded_file.zip'

    # Zorg ervoor dat de map bestaat
    try:
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
    except Exception as e:
        print(f"Fout bij het maken van de map: {e}")
        return

    try:
        response = requests.get(download_url, stream=True)
        
        if response.status_code == 200:
            with open(download_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Bestand succesvol gedownload naar {download_path}!")
        else:
            print(f"Fout bij downloaden: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"Netwerkfout bij het downloaden van het bestand: {e}")
    except Exception as e:
        print(f"Onverwachte fout: {e}")

# Hoofdscript
if __name__ == "__main__":
    download_request_id = create_download_request()
    if download_request_id:
        download_link = check_status(download_request_id)
        if download_link:
            download_file(download_link)
