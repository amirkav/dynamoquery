"""
Usage examples for `DynamoQuery` class.
"""

import boto3

from dynamo_query.data_table import DataTable
from dynamo_query.dynamo_query_main import DynamoQuery
from dynamo_query.expressions import ConditionExpression


def main() -> None:
    table = boto3.resource("dynamodb").Table("test_dq_users_table")
    users_table = DataTable.create().add_record(
        {
            "pk": "john_student@gmail.com",
            "sk": "IBM",
            "email": "john_student@gmail.com",
            "company": "IBM",
            "name": "John",
            "age": 34,
        },
        {
            "pk": "mary@gmail.com",
            "sk": "CiscoSystems",
            "email": "mary@gmail.com",
            "company": "CiscoSystems",
            "name": "Mary",
            "age": 34,
        },
    )
    DynamoQuery.build_batch_update_item().table(table, table_keys={"pk", "sk"}).execute(users_table)

    print("Get all records:")
    for record in (
        DynamoQuery.build_scan()
        .table(table, table_keys={"pk", "sk"})
        .execute_dict({})
        .get_records()
    ):
        print(record)

    print("Get John's record:")
    print(
        DynamoQuery.build_get_item()
        .table(table, table_keys={"pk", "sk"})
        .execute_dict({"pk": "john_student@gmail.com", "sk": "IBM",})
    )

    print("Query by a specific index:")
    for record in (
        DynamoQuery.build_query(
            index_name="gsi_name_age", key_condition_expression=ConditionExpression("name")
        )
        .table(table, table_keys={"pk", "sk"})
        .execute_dict({"name": "Mary", "age": 34})
        .get_records()
    ):
        print(record)


if __name__ == "__main__":
    main()
