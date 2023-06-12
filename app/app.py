import connexion

from utils import fetch_archive_links
from models import create_table_comic

def create_app():
    global archive_links
    app = connexion.App(__name__, specification_dir='../')
    app.add_api('swagger.yml')

    flask_app = app.app
    flask_app.config['SECRET_KEY'] = 'your-secret-key'
    create_table_comic()
    #used while fetching data from xkcd archive using beautifulsoup. archive_links is a accessable throughout the app
    fetch_archive_links()
    return flask_app


app = create_app()


def lambda_handler(event, context):
    app = create_app()
    response = app(event, context)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
