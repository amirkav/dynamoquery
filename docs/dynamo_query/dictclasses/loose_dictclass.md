# LooseDictClass

> Auto-generated documentation for [dynamoquery.dictclasses.loose_dictclass](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dictclasses/loose_dictclass.py) module.

- [dynamo-query](../../README.md#dynamoquery) / [Modules](../../MODULES.md#dynamo-query-modules) / [Dynamo Query](../index.md#dynamo-query) / [Dictclasses](index.md#dictclasses) / LooseDictClass
  - [LooseDictClass](#loosedictclass)
    - [LooseDictClass().update](#loosedictclassupdate)

## LooseDictClass

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dictclasses/loose_dictclass.py#L8)

```python
class LooseDictClass(DynamoDictClass):
```

DictClass that allows any keys.

#### See also

- [DynamoDictClass](dynamo_dictclass.md#dynamodictclass)

### LooseDictClass().update

[[find in source code]](https://github.com/altitudenetworks/dynamoquery/blob/master/dynamoquery/dictclasses/loose_dictclass.py#L32)

```python
def update(*args: Dict[(str, Any)], **kwargs: ignore) -> None:
```

Override of original `dict.update` method to apply `_set_item` rules.
