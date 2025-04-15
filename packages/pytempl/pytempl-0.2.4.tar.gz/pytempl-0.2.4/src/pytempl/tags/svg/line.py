from typing import Literal, Self

from pydantic import ValidationError as PydanticValidationError

from pytempl.errors import ValidationError
from pytempl.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseSVGAttributes, BaseSVGElement

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class LineAttributes(BaseSVGAttributes):
    x1: str
    x2: str
    y1: str
    y2: str
    pathLength: str | Literal["none"]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)

    @classmethod
    def set_defaults(cls) -> dict:
        return {"x1": 0, "x2": 0, "y1": 0, "y2": 0, "pathLength": "none"}


class Line(BaseSVGElement):
    tag_name = "line"
    have_children = False

    def __init__(self, **attributes: Unpack[LineAttributes]):
        try:
            validated_attributes = LineAttributes.validate(
                attributes, LineAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
