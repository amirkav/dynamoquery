"""
Main import point for DynamoQuery.
"""
from dynamoquery.data_table import DataTable
from dynamoquery.dictclasses.dynamo_dictclass import DynamoDictClass
from dynamoquery.dictclasses.loose_dictclass import LooseDictClass
from dynamoquery.dynamoquery_main import DynamoQuery, DynamoQueryError
from dynamoquery.dynamo_table import DynamoTable
from dynamoquery.enums import Operator
from dynamoquery.expressions import ConditionExpression

DynamoRecord = DynamoDictClass

__all__ = (
    "DynamoQuery",
    "DynamoQueryError",
    "ConditionExpression",
    "Operator",
    "DataTable",
    "DynamoDictClass",
    "LooseDictClass",
    "DynamoRecord",
    "DynamoTable",
)
