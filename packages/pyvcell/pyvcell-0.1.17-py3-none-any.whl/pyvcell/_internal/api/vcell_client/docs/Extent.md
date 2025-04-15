# Extent

## Properties

| Name  | Type      | Description | Notes      |
| ----- | --------- | ----------- | ---------- |
| **x** | **float** |             | [optional] |
| **y** | **float** |             | [optional] |
| **z** | **float** |             | [optional] |

## Example

```python
from pyvcell._internal.api.vcell_client.models.extent import Extent

# TODO update the JSON string below
json = "{}"
# create an instance of Extent from a JSON string
extent_instance = Extent.from_json(json)
# print the JSON string representation of the object
print(Extent.to_json())

# convert the object into a dict
extent_dict = extent_instance.to_dict()
# create an instance of Extent from a dict
extent_from_dict = Extent.from_dict(extent_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
