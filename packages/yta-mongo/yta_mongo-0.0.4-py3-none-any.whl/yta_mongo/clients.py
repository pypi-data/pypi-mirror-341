from yta_general_utils.programming.enum import YTAEnum as Enum
from pymongo import MongoClient


__all__ = [
    'MongoDBClient'
]

class MongoDBClient(Enum):
    """
    Enum class to include different Mongo client
    providers to simplify the way to obtain a 
    client connection.
    """

    LOCAL_MONGODB_COMPASS = 'local_mongodb_compass'
    """
    A local instance connected to the MongoDB
    Compass app.
    """

    def get_client(
        self,
        host: str,
        database_name: str
    ) -> MongoClient:
        """
        Obtain a pymongo MongoClient instance connected 
        to the database with the provided 'database_name'
        within the also given 'host'.
        """
        # host = 'localhost:27017'
        # TODO: This must be an if condition according to self.name
        return MongoClient(f'mongodb://{host}/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false/{database_name}')

    