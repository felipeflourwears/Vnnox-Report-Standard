import requests
import time
import platform

from .ModelConfig import ModelConfig


import requests

class ModelVnnox():
    def get_screen_player(self, token, player_ids):
        print("Getting Screenshot from Players")
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/control/screenshot'
        received = 'https://retailmibeex.net/apiVnnox/recibe.php'

        if platform.system() == "Windows":
             username = ModelConfig.username_auth()
        else:
            username = 'popatelier'
        new_url = f"https://{api_host}{new_api_endpoint}"
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'
        }

        # Función para dividir la lista de IDs en lotes
        def chunk_list(data, chunk_size):
            for i in range(0, len(data), chunk_size):
                yield data[i:i + chunk_size]

        chunks = list(chunk_list(player_ids, 100))
        responses = []

        for chunk in chunks:
            request_parameters = {
                "playerIds": chunk,
                "noticeUrl": received
            }

            response = requests.post(new_url, headers=headers, json=request_parameters)
            responses.append(response)

            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
            else:
                print(f"Success: {response.status_code}")
    
        time.sleep(5)
        return responses
    
    def request_data_info_analytics(self, data_players: list):
        total_players = len(data_players)
        online_count = 0
        offline_count = 0

        for player in data_players:
            status = player.get("onlineStatus")

            if status == 1:
                online_count += 1
            elif status == 0:
                offline_count += 1

        return total_players, online_count, offline_count
    

    def get_solution(self, token: str, sn: str):
        API_HOST = 'openapi-us.vnnox.com'
        API_ENDPOINT = '/v1/cloud/lite/player-list'

        url = (
            f"https://{API_HOST}{API_ENDPOINT}"
            f"?count=10&start=0&keyword={sn}"
        )

        headers = {
            "username": "popatelier",
            "token": token
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                return "No Solution"

            data = response.json()

            return (
                data
                .get("data", {})
                .get("rows", [{}])[0]
                .get("programInfo", {})
                .get("programName", "No Solution")
            )

        except Exception as e:
            print("Error get_solution:", e)
            return "No Solution"
        
   

    def get_players_data(
        self,
        token: str,
        names: list,
        START_PARAMETER: int = 0,
        COUNT_PARAMETER: int = 1
    ):
        API_HOST = 'openapi-us.vnnox.com'
        ENDPOINT = '/v1/player/getPlayerList'

        username = 'popatelier'
        password = 'Beex2024%.'

        # 1. Autenticación
        auth_url = f"https://{API_HOST}/v1/oauth/token"
        auth_payload = {
            'username': username,
            'password': password,
            'grant_type': 'password'
        }

        auth_response = requests.post(auth_url, data=auth_payload)

        if auth_response.status_code != 200:
            raise Exception(f"Error en autenticación: {auth_response.status_code}")

        # ARRAY ALL INFORMATION OF PLAYERS
        players_data = []

        # ARRAY ALL PLAYERS IDs
        players_ids = []

        # 3. Iterar nombres de tiendas
        for name in names:
            url = (
                f"https://{API_HOST}{ENDPOINT}"
                f"?count={COUNT_PARAMETER}&start={START_PARAMETER}&name={name}"
            )

            headers = {
                'username': username,
                'token': token
            }

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"Error obteniendo datos de {name}: {response.status_code}")
                continue

            data = response.json()
            rows = data.get('data', {}).get('rows', [])

            if not rows:
                continue

            player = rows[0]  # solo uno porque count=1

            players_data.append({
                "playerId": player.get("playerId"),
                "name": player.get("name"),
                "sn": player.get("sn"),
                "onlineStatus": player.get("onlineStatus"),
                "lastOnlineTime": player.get("lastOnlineTime"),
            })
            players_ids.append(player.get("playerId"))

        return players_data, players_ids