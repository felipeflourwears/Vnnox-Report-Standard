from dotenv import load_dotenv
import os

#Cargar variables de ENV
load_dotenv()

class ModelConfig:
    @staticmethod
    def username_auth():
        username = os.getenv('VNNOX_USER')
        return username
     
    @staticmethod
    def token_auth():
        token = os.getenv('VNNOX_TOKEN')
        return token
     
    @staticmethod
    def pass_username():
        passw = os.getenv('VNNOX_PASSWORD')
        return passw