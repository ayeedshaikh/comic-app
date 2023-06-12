from datetime import datetime
from flask import abort
from utils import fetch_metadata, archive_links
from models import read_from_comic, update_views

"""
    When the user provides a date, the API will fetch the comic published on that date.
    As the publisher have not provided an interface for fetching the comic by date,
    the below logic will convert date to comic number as per the publishing schedule (Mondays, Wednesdays, and Fridays).
    But this approach will not work for dates before 2023 as the data is inconsistency.
    
    user input is date in DDMMYYYY format.
"""


def get_comic_by_date(date):
    target_date = datetime.strptime(date, "%d%m%Y")
    current_date = datetime.now()
    start_date = datetime(2023, 1, 2)

    if target_date > current_date:
        abort(404, "The target date is in the future. Please provide a valid date.")

    if target_date.weekday() not in [0, 2, 4]:
        abort(404, "Comics are published only on Mondays, Wednesdays, and Fridays as per xkcd.")

    days_start = (target_date - start_date).days

    if days_start < 0:
        abort(404, "Due to inconsistent publishing schedule, the API fetches data 2023 onwards.", )

    weeks = days_start // 7
    extra_days = days_start % 7
    comic_number = 2719 + weeks * 3

    if extra_days >= 1:
        comic_number += 1
    if extra_days >= 3:
        comic_number += 1
    if extra_days >= 5:
        comic_number += 1

    leap_years = (target_date.year - start_date.year + 1) // 4
    if target_date.year % 4 == 0 and target_date.month < 3:
        leap_years -= 1
    comic_number += leap_years

    fetch_meta = get_comic_by_id(comic_number)
    return fetch_meta


"""
    Fetching the comic metadata by comic number.
    user input is comic number.
"""


def get_comic_by_id(comic_id):
    # Check if the comic is already fetched and stored in DynamoDB.
    read_db = read_from_comic(comic_id)
    if 'Item' in read_db:
        update_views(comic_id)
        return {
            "title": read_db['Item']['title'],
            "image_url": read_db['Item']['image_url']
        }
    fetch_meta = fetch_metadata(comic_id)
    return fetch_meta


"""
    An alternative approach to fetch the comic by date using beautiful soup.
"""


def search_comic_by_date(date):
    date_obj = datetime.strptime(date, "%d%m%Y")
    formatted_date = date_obj.strftime("%Y-%-m-%-d")
    comic_id = [data for data in archive_links if data['date'] == formatted_date]
    fetch_meta = get_comic_by_id(comic_id[0]['id'])
    return fetch_meta


"""
    Fetching the comic statistics by comic number.
"""


def get_comic_statistics(comic_id):
    read_db = read_from_comic(comic_id)
    if 'Item' in read_db:
        return {
            "title": read_db['Item']['title'],
            "image_url": read_db['Item']['image_url'],
            "views": read_db['Item']['views']
        }
    return {"error": "No comic found with the given id."}
