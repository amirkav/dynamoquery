# DynamoTable

> Auto-generated documentation for [dynamoquery.dynamo_table](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py) module.

- [dynamo-query](../README.md#dynamoquery) / [Modules](../MODULES.md#dynamo-query-modules) / [Dynamo Query](index.md#dynamo-query) / DynamoTable
  - [DynamoTable](#dynamotable)
    - [DynamoTable().batch_delete](#dynamotablebatch_delete)
    - [DynamoTable().batch_delete_records](#dynamotablebatch_delete_records)
    - [DynamoTable().batch_get](#dynamotablebatch_get)
    - [DynamoTable().batch_get_records](#dynamotablebatch_get_records)
    - [DynamoTable().batch_upsert](#dynamotablebatch_upsert)
    - [DynamoTable().batch_upsert_records](#dynamotablebatch_upsert_records)
    - [DynamoTable().cached_batch_get](#dynamotablecached_batch_get)
    - [DynamoTable().cached_get_record](#dynamotablecached_get_record)
    - [DynamoTable().clear_records](#dynamotableclear_records)
    - [DynamoTable().clear_table](#dynamotableclear_table)
    - [DynamoTable().client](#dynamotableclient)
    - [DynamoTable().create_table](#dynamotablecreate_table)
    - [DynamoTable().delete_record](#dynamotabledelete_record)
    - [DynamoTable().delete_table](#dynamotabledelete_table)
    - [DynamoTable().get_partition_key](#dynamotableget_partition_key)
    - [DynamoTable.get_primary_index](#dynamotableget_primary_index)
    - [DynamoTable().get_record](#dynamotableget_record)
    - [DynamoTable().get_sort_key](#dynamotableget_sort_key)
    - [DynamoTable().get_table_status](#dynamotableget_table_status)
    - [DynamoTable().invalidate_cache](#dynamotableinvalidate_cache)
    - [DynamoTable().max_batch_size](#dynamotablemax_batch_size)
    - [DynamoTable().normalize_record](#dynamotablenormalize_record)
    - [DynamoTable().primary_index](#dynamotableprimary_index)
    - [DynamoTable().query](#dynamotablequery)
    - [DynamoTable().scan](#dynamotablescan)
    - [DynamoTable().table](#dynamotabletable)
    - [DynamoTable().table_keys](#dynamotabletable_keys)
    - [DynamoTable().upsert_record](#dynamotableupsert_record)
    - [DynamoTable().validate_record_attributes](#dynamotablevalidate_record_attributes)
    - [DynamoTable().wait_until_exists](#dynamotablewait_until_exists)
    - [DynamoTable().wait_until_not_exists](#dynamotablewait_until_not_exists)
  - [DynamoTableError](#dynamotableerror)

## DynamoTable

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L63)

```python
class DynamoTable(Generic[_RecordType], LazyLogger, ABC):
    def __init__(logger: Optional[logging.Logger] = None) -> None:
```

DynamoDB table manager, uses `DynamoQuery` underneath.

#### Arguments

- `logger` - `logging.Logger` instance.

#### Examples

```python
from dynamoquery import DynamoTable, DynamoRecord
from typing import Optional

class UserRecord(DynamoRecord):
    pk: str
    email: str
    name: str
    points: Optional[int] = None

# Create your dynamo table manager with your record class
class UserTable(DynamoTable[UserRecord]):
    # provide a set of your table keys
    table_keys = {'pk'}

    # use this property to define your table name
    @property
    def table(self) -> str:
        return "my_table"

    # define how to get PK from a record
    def get_partition_key(self, record: UserRecord) -> str:
        return record.email

    # we do not have a sort key in our table
    def get_sort_key(self, record: UserRecord) -> None:
        return None

    # specify some GSIs
    global_secondary_indexes = [
        DynamoTableIndex("gsi_name", "name", None),
        DynamoTableIndex("gsi_email_age", "email", "age"),
    ]

# and now we can create our table in DynamoDB
user_table = UserTable()
user_table.create_table()
```

#### Attributes

- `NO_RECORD` - Sentinels: `SentinelValue('NO_RECORD')`

#### See also

- [LazyLogger](lazy_logger.md#lazylogger)

### DynamoTable().batch_delete

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L614)

```python
def batch_delete(
    data_table: DataTable[_RecordType],
) -> DataTable[_RecordType]:
```

Delete multuple records as a DataTable from DB.

`data_table` must have all columns to calculate table keys.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# we should provide table keys or fields to calculate them
# in our case, PK is calculated from `email` field.
users_table = DataTable[UserRecord]().add_record(
    {
        "email": "puppy@gmail.com",
    },
    {
        "email": "elon@gmail.com",
    },
)
deleted_records = user_table.batch_delete(users_table)

for deleted_record in deleted_records:
    # print deleted_record records
    # if record was not found - it will still be returned
    # but only with the data you provided
    print(deleted_record)
```

#### Arguments

- `data_table` - Request data table.

#### Returns

DataTable with deleted records.

### DynamoTable().batch_delete_records

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L774)

```python
def batch_delete_records(records: Iterable[_RecordType]) -> None:
```

Delete records from DB.

See [DynamoTable().batch_delete](#dynamotablebatch_delete).

#### Arguments

- `records` - Full or partial records to delete.

### DynamoTable().batch_get

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L504)

```python
def batch_get(data_table: DataTable[_RecordType]) -> DataTable[_RecordType]:
```

Get multuple records as a DataTable from DB.

`data_table` must have all columns to calculate table keys.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# we should provide table keys or fields to calculate them
# in our case, PK is calculated from `email` field.
users_table = DataTable[UserRecord]().add_record(
    {
        "email": "puppy@gmail.com",
    },
    {
        "email": "elon@gmail.com",
    },
)
user_records = user_table.batch_get(users_table)

for user_record in user_records:
    # print found records
    # if record was not found - it will still be returned
    # but only with the data you provided
    print(user_record)
```

#### Arguments

- `data_table` - Request data table.

#### Returns

DataTable with existing records.

### DynamoTable().batch_get_records

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L756)

```python
def batch_get_records(
    records: Iterable[_RecordType],
) -> Iterator[_RecordType]:
```

Get records as an iterator from DB.

See [DynamoTable().batch_get](#dynamotablebatch_get).

#### Arguments

- `records` - Full or partial records data.

#### Yields

Found or not found record data.

### DynamoTable().batch_upsert

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L668)

```python
def batch_upsert(
    data_table: DataTable[_RecordType],
    set_if_not_exists_keys: Iterable[str] = (),
) -> DataTable[_RecordType]:
```

Upsert multuple records as a DataTable to DB.

`data_table` must have all columns to calculate table keys.

Sets `dt_created` field equal to current UTC datetime if a record was created.
Sets `dt_modified` field equal to current UTC datetime.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# we should provide table keys or fields to calculate them
# in our case, PK is calculated from `email` field.
users_table = DataTable[UserRecord]().add_record(
    {
        "email": "puppy@gmail.com",
        "name": "Doge Barky",
        "age": 20,
    },
    {
        "email": "elon@gmail.com",
        "name": "Elon Musk",
        "age": 5289,
    },
)
upserted_records = user_table.batch_upsert(users_table)

for upserted_record in upserted_records:
    # print created and updated records
    print(upserted_record)
```

#### Arguments

- `data_table` - Request DataTable.
- `set_if_not_exists_keys` - List of keys to set only if they no do exist in DB.

#### Returns

A DataTable with upserted results.

### DynamoTable().batch_upsert_records

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L789)

```python
def batch_upsert_records(
    records: Iterable[_RecordType],
    set_if_not_exists_keys: Iterable[str] = (),
) -> None:
```

Upsert records to DB.

See [DynamoTable().batch_upsert](#dynamotablebatch_upsert).

#### Arguments

- `records` - Full or partial records data.
- `set_if_not_exists_keys` - List of keys to set only if they no do exist in DB.

### DynamoTable().cached_batch_get

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L574)

```python
def cached_batch_get(
    data_table: DataTable[_RecordType],
) -> DataTable[_RecordType]:
```

Get multuple records as a DataTable from DB with caching.

`data_table` must have all columns to calculate table keys.

Can be used instead of [DynamoTable().batch_get](#dynamotablebatch_get) method.

#### Arguments

- `data_table` - Request data table.

#### Returns

DataTable with existing records.

### DynamoTable().cached_get_record

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L858)

```python
def cached_get_record(record: _RecordType) -> Optional[_RecordType]:
```

Get Record from DB with caching.

Can be used instead of [DynamoTable().get_record](#dynamotableget_record) method.

#### Returns

A dict with record data or None.

### DynamoTable().clear_records

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L1178)

```python
def clear_records() -> None:
```

Delete all records managed by current table manager.

Deletes only records with sort key starting with `sort_key_prefix`.

### DynamoTable().clear_table

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L433)

```python
def clear_table(
    partition_key: Optional[str] = None,
    partition_key_prefix: Optional[str] = None,
    sort_key: Optional[str] = None,
    sort_key_prefix: Optional[str] = None,
    index: Optional[DynamoTableIndex] = None,
    filter_expression: Optional[ConditionExpressionType] = None,
    limit: Optional[int] = None,
) -> None:
```

Remove records from DB.

If `partition_key` and `partition_key_prefix` are None - deletes all records.

#### Arguments

- `partition_key` - Partition key value.
- `sort_key` - Sort key value.
- `partition_key_prefix` - Partition key prefix value.
- `sort_key_prefix` - Sort key prefix value.
- `index` - DynamoTableIndex instance, primary index is used if not provided.
- `filter_expression` - Query filter expression.
- `limit` - Max number of results.

### DynamoTable().client

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L161)

```python
@property
def client() -> DynamoDBClient:
```

#### See also

- [DynamoDBClient](dynamoquery_types.md#dynamodbclient)

### DynamoTable().create_table

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L281)

```python
def create_table() -> Optional[CreateTableOutputTypeDef]:
```

Create a table in DynamoDB.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# create a table with key schema and all indexes.
UserTable.create_table()
```

### DynamoTable().delete_record

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L958)

```python
def delete_record(
    record: _RecordType,
    condition_expression: Optional[ConditionExpression] = None,
) -> Optional[_RecordType]:
```

Delete Record from DB.

`record` must have all fields to calculate table keys.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# we should provide table keys or fields to calculate them
# in our case, PK is calculated from `email` field.
deleted_record = user_table.delete_record({
    "email": "cheater@gmail.com",
})

if deleted_record is None:
    # no record found, so nothing was deleted
else:
    # print deleted record
    print(user_record)
```

#### Arguments

- `record` - Record with required fields for sort and partition keys.
- `condition_expression` - Condition for delete.

#### Returns

A dict with record data or None.

### DynamoTable().delete_table

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L243)

```python
def delete_table() -> None:
```

Delete the table from DynamoDB.

If table is creating, wait until it is created, then deletes it.
If table is deleting or does not exist, does nothing.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# delete table
UserTable.delete_table()

# make sure that it is deleted
user_table.wait_until_not_exists()
```

### DynamoTable().get_partition_key

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L191)

```python
def get_partition_key(record: _RecordType) -> Any:
```

Override this method to get PK from a record.

### DynamoTable.get_primary_index

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L180)

```python
@classmethod
def get_primary_index() -> DynamoTableIndex:
```

Primary global index

#### See also

- [DynamoTableIndex](dynamo_table_index.md#dynamotableindex)

### DynamoTable().get_record

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L815)

```python
def get_record(record: _RecordType) -> Optional[_RecordType]:
```

Get Record from DB.

`record` must have all fields to calculate table keys.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# we should provide table keys or fields to calculate them
# in our case, PK is calculated from `email` field.
user_record = user_table.get_record({
    "email": "suspicious@gmail.com",
})

if user_record is None:
    # no record found
    pass
else:
    # print found record
    print(user_record)
```

#### Arguments

- `record` - Record with required fields for sort and partition keys.

#### Returns

A dict with record data or None.

### DynamoTable().get_sort_key

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L200)

```python
def get_sort_key(record: _RecordType) -> Any:
```

Override this method to get SK from a record.

### DynamoTable().get_table_status

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L229)

```python
def get_table_status() -> Optional[str]:
```

Get table status from Dynamo.

#### Returns

Status string or None.

### DynamoTable().invalidate_cache

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L568)

```python
def invalidate_cache() -> None:
```

Clear cache for [DynamoTable().cached_batch_get](#dynamotablecached_batch_get) and [DynamoTable().cached_get_record](#dynamotablecached_get_record)

### DynamoTable().max_batch_size

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L172)

```python
@property
def max_batch_size() -> int:
```

### DynamoTable().normalize_record

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L372)

```python
def normalize_record(record: _RecordType) -> _RecordType:
```

Modify record before upsert.

#### Arguments

- `record` - Record for upsert.

#### Returns

Normalized record.

### DynamoTable().primary_index

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L176)

```python
@property
def primary_index() -> DynamoTableIndex:
```

#### See also

- [DynamoTableIndex](dynamo_table_index.md#dynamotableindex)

### DynamoTable().query

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L1065)

```python
def query(
    partition_key: Any,
    index: Optional[DynamoTableIndex] = None,
    sort_key: Optional[Any] = None,
    sort_key_prefix: Optional[str] = None,
    filter_expression: Optional[ConditionExpressionType] = None,
    scan_index_forward: bool = True,
    projection: Iterable[str] = tuple(),
    data: Optional[Dict[(str, Any)]] = None,
    limit: Optional[int] = None,
) -> Iterator[_RecordType]:
```

Query table records by index.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

user_records = user_table.query(
    # query by our PK
    partition_key="new_users",

    # and SK starting with `email_`
    sort_key_prefix="email_",

    # get only users older than ...
    # we will provide values in data
    filter_expression=ConditionExpression("age", "<="),

    # get only first 5 results
    limit=5,

    # get only name and email fields
    projection=("name", "email"),

    # ...older than 45 years
    data= {"age": 45}

    # start with the newest records
    scan_index_forward=False,
)

for user_record in user_records:
    print(user_record)
```

#### Arguments

- `partition_key` - Partition key value.
- `index` - DynamoTableIndex instance, primary index is used if not provided.
- `sort_key` - Sort key value.
- `sort_key_prefix` - Sort key prefix value.
- `filter_expression` - Query filter expression.
- `scan_index_forward` - Whether to scan index from the beginning.
- `projection` - Record fields to return, by default returns all fields.
- `limit` - Max number of results.

#### Yields

Matching record.

### DynamoTable().scan

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L1007)

```python
def scan(
    filter_expression: Optional[ConditionExpressionType] = None,
    projection: Iterable[str] = tuple(),
    data: Optional[Dict[(str, Any)]] = None,
    limit: Optional[int] = None,
) -> Iterator[_RecordType]:
```

List table records.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

user_records = user_table.scan(
    # get only users older than ...
    # we will provide values in data
    filter_expression=ConditionExpression("age", "<="),

    # get only first 5 results
    limit=5,

    # get only name and email fields
    projection=("name", "email"),

    # ...older than 45 years
    data= {"age": 45}
)

for user_record in user_records:
    print(user_record)
```

#### Arguments

- `filter_expression` - Query filter expression.
- `scan_index_forward` - Whether to scan index from the beginning.
- `projection` - Record fields to return, by default returns all fields.
- `limit` - Max number of results.

### DynamoTable().table

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L154)

```python
@property
@abstractmethod
def table() -> Table:
```

Override this method to get DynamoDB Table resource.

#### See also

- [Table](dynamoquery_types.md#table)

### DynamoTable().table_keys

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L165)

```python
@property
def table_keys() -> Set[str]:
```

### DynamoTable().upsert_record

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L880)

```python
def upsert_record(
    record: _RecordType,
    condition_expression: Optional[ConditionExpression] = None,
    set_if_not_exists_keys: Iterable[str] = (),
    extra_data: Dict[(str, Any)] = None,
) -> _RecordType:
```

Upsert Record to DB.

`record` must have all fields to calculate table keys.

Sets `dt_created` field equal to current UTC datetime if a record was created.
Sets `dt_modified` field equal to current UTC datetime.

#### Examples

```python
# UserTable is a subclass of a DynamoTable
user_table = UserTable()

# we should provide table keys or fields to calculate them
# in our case, PK is calculated from `email` field.
user_record = user_table.upsert_record(
    {
        "email": "newuser@gmail.com",
        "name": "Somebody Oncetoldme"
        "age": 23,
    },
    set_if_not_exists_keys=["age"], # set age if it does not exist in DB yet.
)

# print upserted record
print(user_record)
```

#### Arguments

- `record` - Record to insert/update.
- `condition_expression` - Condition for update.
- `set_if_not_exists_keys` - List of keys to set only if they no do exist in DB.
- `extra_data` - Data for query.

#### Returns

A dict with updated record data.

### DynamoTable().validate_record_attributes

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L384)

```python
def validate_record_attributes(record: _RecordType) -> None:
```

Check that all index keys are set correctly in record.

#### Arguments

- `record` - Record for upsert.

#### Raises

- `DynamoTableError` - If index key is missing.

### DynamoTable().wait_until_exists

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L1166)

```python
def wait_until_exists() -> None:
```

Proxy method for `resource.Table.wait_until_exists`.

### DynamoTable().wait_until_not_exists

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L1172)

```python
def wait_until_not_exists() -> None:
```

Proxy method for `resource.Table.wait_until_not_exists`.

## DynamoTableError

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dynamo_table.py#L43)

```python
class DynamoTableError(BaseException):
    def __init__(message: str, data: Any = None) -> None:
```

Main error for [DynamoTable](#dynamotable) class.

#### Arguments

- `message` - Error message.
- `data` - Addition JSON-serializeable data.
