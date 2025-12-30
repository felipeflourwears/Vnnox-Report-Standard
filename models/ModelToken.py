import json
import requests
import time

from .ModelConfig import ModelConfig

class ModelToken:
    @classmethod
    def getTokenDB(cls):
        url = "https://retailmibeex.net/apiVnnox/getTokenVnnox.php"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "token" in data:
                print("Token obtenido:", data["token"])
                return data["token"]
            else:
                print("Error: No se encontró el token en la respuesta")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el token: {e}")
            return None
