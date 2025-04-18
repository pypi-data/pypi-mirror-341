import inspect
from typing import List, Optional, Type

from pydantic import BaseModel

from pait import _pydanitc_adapter, field
from pait.util import get_pydantic_annotation


def get_parameter_list_from_pydantic_basemodel(
    pait_model: Type[BaseModel],
    default_field_class: Optional[Type[field.BaseRequestResourceField]] = None,
) -> List["inspect.Parameter"]:
    """get class parameter list by attributes, if attributes not default value, it will be set `Undefined`"""
    parameter_list = []
    for key, model_field in _pydanitc_adapter.model_fields(pait_model).items():
        pydantic_field = _pydanitc_adapter.get_field_info(model_field)
        if not field.is_pait_field(pydantic_field):
            if not default_field_class:
                raise TypeError(  # pragma: no cover
                    f"{pydantic_field.__class__} must instance {field.BaseRequestResourceField} or"
                    f" {field.Depends} by model {pait_model}"
                )
            pydantic_field = default_field_class.from_pydantic_field(pydantic_field)
            pydantic_field.set_request_key(key)
        parameter = inspect.Parameter(
            key,
            inspect.Parameter.POSITIONAL_ONLY,
            default=pydantic_field,
            annotation=get_pydantic_annotation(key, pait_model),
        )
        parameter_list.append(parameter)
    return parameter_list
