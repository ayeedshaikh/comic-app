from boto3 import resource
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, ENDPOINT_URL

resource = resource(
    'dynamodb',
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)


def create_table_comic():
    table_name = 'Comic'
    existing_tables = resource.meta.client.list_tables()['TableNames']
    if table_name in existing_tables:
        print(f"Table '{table_name}' already exists. Skipping creation.")
        return None
    try:
        table = resource.create_table(
            TableName='Comic',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table
    except Exception as e:
        print(f"Error creating table '{table_name}'.")
        print(e)
        return None


ComicTable = resource.Table('Comic')


def write_to_comic(pk, title, image_url, date):
    response = ComicTable.put_item(
        Item={
            'id': pk,
            'title': title,
            'image_url': image_url,
            'date': date,
            'views': 0
        }
    )
    return response


def read_from_comic(pk):
    response = ComicTable.get_item(
        Key={
            'id': pk
        },
        AttributesToGet=[
            'id', 'title', 'date', 'views', 'image_url'
        ]
    )
    return response


def update_views(pk):
    response = ComicTable.update_item(
        Key={
            'id': pk
        },
        AttributeUpdates={
            'views': {
                'Value': 1,
                'Action': 'ADD'
            }
        },
        ReturnValues="UPDATED_NEW"
    )
    response['Attributes']['views'] = int(response['Attributes']['views'])
    return response


table = resource.Table("User")


def create_user(username, password):
    table.put_item(
        Item={
            "username": username,
            "password": password,
        }
    )


def get_user(username):
    response = table.get_item(Key={"username": username})
    user = response.get("Item")
    return user
