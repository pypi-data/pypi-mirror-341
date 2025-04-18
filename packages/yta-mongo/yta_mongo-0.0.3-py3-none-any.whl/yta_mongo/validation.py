"""
Functions to simplify the way we validate 
parameters.
"""
from yta_general_utils.programming.validator import PythonValidator
from bson.objectid import ObjectId
from typing import Union


def is_mongo_id(id: Union[ObjectId, str]):
    """
    Check if the given 'id' is a valid type of mongo
    id (string or ObjectId).
    """
    return (
        PythonValidator.is_string(id) or
        PythonValidator.is_instance(id, ObjectId)
    )

def validate_mongo_host(host: str):
    """
    Validate if the given 'host' is a string and
    raises an Exception if not.
    """
    _validate_string_parameter('host', host)

def validate_mongo_database_name(database_name: str):
    """
    Validate if the given 'database_name' is a string
    and raises an Exception if not.
    """
    _validate_string_parameter('database_name', database_name)

def validate_mongo_field(field: str):
    """
    Validate if the given 'field' is a string and
    raises an Exception if not.
    """
    _validate_string_parameter('field', field)

def validate_mongo_id(id: Union[ObjectId, str]):
    """
    Validate if the given 'id' is a valid type of
    mongo id (string or ObjectId) and raises an
    Exception if not.
    """
    if not is_mongo_id(id):
        raise Exception('The provided "id" is not a valid mongo id (string or ObjectId instance).')

def validate_mongo_table_name(table_name: str):
    """
    Validate if the given 'table_name' is a string
    and raises an Exception if not.
    """
    _validate_string_parameter('table_name', table_name)
    
def validate_mongo_document(document: dict):
    """
    Validate if the given 'document' is a dict and
    raises an Exception if not.
    """
    if not PythonValidator.is_dict(document):
        raise Exception('The given "document" is not a valid dict.')
    
def _validate_string_parameter(name: str, value: any):
    """
    Validate if the given 'value' is a string value
    or raises an Exception mentioning the given 'name'
    if not.
    """
    if not PythonValidator.is_string(value):
        raise Exception(f'The given "{name}" is not a valid string.')
