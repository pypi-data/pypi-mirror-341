"""
This library will interact with a Mongo
database by to be able to persist 
information on it.

Module to easily connect to a Mongo
database instance.
"""
from yta_mongo.validation import validate_mongo_database_name, validate_mongo_document, validate_mongo_field, validate_mongo_id, validate_mongo_table_name, validate_mongo_host
from yta_mongo.clients import MongoDBClient
from yta_general_utils.programming.validator import PythonValidator
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Union


class MongoDatabaseHandler:
    """
    Class to handle an specific Mongo
    database.
    """

    def __init__(
        self,
        host: str,
        database_name: str,
        client_type: MongoDBClient
    ):  
        validate_mongo_host(host)
        validate_mongo_database_name(database_name)
        client_type = MongoDBClient.to_enum(client_type)

        self._host = host
        self._database_name = database_name
        self._client_type = client_type
        
        # Try and validate connection or raise exception
        self.client

    @property
    def client(self) -> MongoClient:
        """
        The client that is connected to the MongoDB Compass
        instance and can interact with it.

        This method will raise an Exception if the database
        doesn't exist.
        """
        if not hasattr(self, '_client'):
            self._client = self._client_type.get_client(self._host, self._database_name)

        return self._client

    # TODO: I don't know the real type
    @property
    def database(self) -> 'Database':
        """
        The connection with the database that allows us
        interacting with the tables and items.
        """
        return self._client[self._database_name]

    def _get_table(
        self,
        table_name: str
    ) -> 'Collection':
        """
        The connection with the provided 'table_name' 
        database table that allows us interacting with
        all the items inside.
        """
        validate_mongo_table_name(table_name)

        return self.database[table_name]

    # TODO: I don't know the real type
    def find_one_by_id(
        self,
        table_name: str,
        id: Union[ObjectId, str]
    ) -> Union[dict, None]:
        """
        Find the element with the given 'id' in the table
        with the 'table_name' given name.

        This method returns the result if found or None if
        not.
        """
        validate_mongo_table_name(table_name)
        validate_mongo_id(id)

        id = (
            ObjectId(id)
            if PythonValidator.is_string(id) else
            id
        )

        return self.find_one(
            table_name,
            { '_id': id }
        )
        
    # TODO: I don't know the real type
    def find_one_by_field(
        self,
        table_name: str,
        field_name: str,
        value: any
    ) -> Union[dict, None]:
        """
        Find the element with the given 'value' for its
        'field_name' field in the table with the 'table_name'
        provided name.

        This method returns the result if found or None if
        not.
        """
        validate_mongo_table_name(table_name)
        validate_mongo_field(field_name)

        return self.find_one(
            table_name,
            { field_name: value }
        )
        
    # TODO: I don't know the real type
    def find_one(
        self,
        table_name: str,
        find_condition: dict
    ) -> Union[dict, None]:
        """
        Look for the first document with the given
        'find_condition' in the provided 'table_name'.

        The 'find_condition' must be a dict adapted to
        the mongo way of handling it. One example is
        { 'status': { '$ne': 'finished' } } to look
        for the documents which status is not equal to
        'finished' string value. You can use hierarchy
        in the fields by using dots.

        This method will return a single result (the
        first one found) or None if no results found.
        """
        validate_mongo_table_name(table_name)

        return self._get_table(table_name).find_one(
            find_condition
        )
    
    def find_by_field(
        self,
        table_name: str,
        field_name: str,
        value: any
    ) -> list[dict]:
        """
        TODO: Write doc
        """
        return self.find(
            table_name,
            { field_name: value }
        )
    
    # TODO: I don't know the real type
    def find(
        self,
        table_name: str,
        find_condition: dict
    ) -> list[dict]:
        """
        Look for the documents with the given
        'find_condition' in the provided 'table_name'.

        The 'find_condition' must be a dict adapted to
        the mongo way of handling it. One example is
        { 'status': { '$ne': 'finished' } } to look
        for the documents which status is not equal to
        'finished' string value. You can use hierarchy
        in the fields by using dots.

        This method will return all the results found
        or an empty list if no results founds.
        """
        validate_mongo_table_name(table_name)

        return self._get_table(table_name).find(
            find_condition
        )

    # TODO: I don't know the real type
    def insert_one(
        self,
        table_name: str,
        document: dict
    ) -> Union[dict, None]:
        """
        Insert the given 'document' in the table with the
        'table_name' provided name.

        This method returns the whole document that has
        been inserted doing a 'find_by_id' search if it
        was correctly inserted, or will raise an Exception
        if something went wrong.
        """
        validate_mongo_table_name(table_name)
        validate_mongo_document(document)

        return self.find_one_by_id(
            table_name,
            self._get_table(table_name).insert_one(document).inserted_id
        )

    def update_one(
        self,
        table_name: str,
        id: Union[ObjectId, str],
        field: str,
        value: any
    ) -> Union[dict, None]:
        """
        Update the given 'field' of the document that has
        the provided 'id' and set the new provided 'value'.

        The 'field' can be a field name with hierarchy by
        using dots. For example, if you use the field value
        'segments.0.enhancements.1.name' you will be 
        updating the 'name' field for the second enhancement
        of the first segment.
        """
        validate_mongo_table_name(table_name)
        validate_mongo_id(id)
        validate_mongo_field(field)
        # TODO: Can I validate 'value' in some way (?)

        document = self.find_one_by_id(table_name, id)

        if document is None:
            raise Exception(f'No document foudn with the given id "{str(id)}".')
        
        self._get_table(table_name).update_one(
            { '_id': id },
            { "$set": { field: value } }
        )

        return self.find_one_by_id(table_name, id)
