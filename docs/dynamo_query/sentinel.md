# Sentinel

> Auto-generated documentation for [dynamoquery.sentinel](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/sentinel.py) module.

Sentinel value than can be used as a placeholder.

- [dynamo-query](../README.md#dynamoquery) / [Modules](../MODULES.md#dynamo-query-modules) / [Dynamo Query](index.md#dynamo-query) / Sentinel
  - [SentinelValue](#sentinelvalue)

## SentinelValue

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/sentinel.py#L6)

```python
class SentinelValue():
    def __init__(name: str = 'DEFAULT') -> None:
```

Sentinel value than can be used as a placeholder.
Doc generation friendly.

```python
NOT_SET = SentinelValue('NOT_SET')

def check_value(name=NOT_SET):
    if name is NOT_SET:
        return 'This is a NOT_SET value'

    return 'This is something else'

repr(NOT_SET) # 'NOT_SET'
```

#### Arguments

- `name` - String used as a representation of the object.
