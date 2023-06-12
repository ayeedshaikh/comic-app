from dotenv import load_dotenv

load_dotenv()
import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')