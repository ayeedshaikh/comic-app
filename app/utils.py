import requests
from datetime import datetime
import models as model
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import NoCredentialsError
from connexion import ProblemException
from models import update_views, write_to_comic
from io import BytesIO
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, ENDPOINT_URL
"""
    This Function will fetch the metadata of the comic once the comic number is provided.    
"""

# Configure S3 client
s3_client = boto3.client(
    's3',
    endpoint_url = ENDPOINT_URL,
    aws_access_key_id= AWS_ACCESS_KEY_ID,
    aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
    region_name= REGION_NAME
)
bucket_name = 's3-bucket-name'

def fetch_metadata(comic_number):
    comic_url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(comic_url)
    if response.status_code == 200:
        comic_metadata = response.json()

        title = comic_metadata["title"]
        image_url = comic_metadata["img"]
        num = comic_metadata["num"]

        year = int(comic_metadata["year"])
        month = int(comic_metadata["month"])
        day = int(comic_metadata["day"])
        comic_date = datetime(year, month, day)
        formatted_date = comic_date.strftime("%d%m%Y")

        image_response = requests.get(image_url)
        filename = f"{num}.png"

        try:
            s3_client.upload_fileobj(BytesIO(image_response.content), bucket_name, filename)
        except NoCredentialsError:
            raise ProblemException(status=500, title='Error',
                                   detail='S3 credentials not found. Unable to upload image.')

        s3_image_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        write_to_comic(num, title, s3_image_url, formatted_date)
        update_views(comic_number)
        read_db = model.read_from_comic(comic_number)
        if 'Item' in read_db:
            return {
                "title": read_db['Item']['title'],
                "image_url": read_db['Item']['image_url']
            }
    return {"error": "Failed to retrieve comic metadata."}


"""
    Second approach as the publishing data is not consistent, 
    and with this approach we can fetch the data of any date 
    from 01-01-2006 onwards.
"""

archive_links = []

def fetch_archive_links():
    if archive_links:
        return archive_links

    url = "https://xkcd.com/archive/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links_container = soup.find('div', {'id': 'middleContainer', 'class': 'box'})

        archive_links.extend([
            {'id': int(link['href'].strip('/')), 'date': link['title']}
            for link in links_container.find_all('a')
        ])

    return archive_links