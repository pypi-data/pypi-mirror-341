from collections import deque
from copy import deepcopy
from dataclasses import fields, is_dataclass
from functools import reduce
from inspect import isclass, unwrap
from typing import Any, Dict, List, Literal, Protocol, Tuple, Type, TypeVar, Union

from catalystwan.core.exceptions import (
    CatalystwanModelInputException,
    CatalystwanModelValidationError,
)
from catalystwan.core.types import MODEL_TYPES, AliasPath, DataclassInstance
from typing_extensions import Annotated, get_args, get_origin, get_type_hints

T = TypeVar("T", bound=DataclassInstance)


class ValueExtractorCallable(Protocol):
    def __call__(self, field_value: Any) -> Any: ...


class ModelDeserializer:
    def __init__(self, model: Type[T]) -> None:
        self.model = model
        try:
            self.model_type: MODEL_TYPES = model._catalystwan_model_type  # type: ignore[attr-defined]
        except AttributeError:
            self.model_type = "base"
        self._exceptions: List[
            Union[CatalystwanModelInputException, CatalystwanModelValidationError]
        ] = []
        # different models wrap their values in different ways, hence
        # the need for multiple extractors
        self.VALUE_EXTRACTORS: Dict[MODEL_TYPES, ValueExtractorCallable] = {
            "base": self.__value_extractor_base,
            "feature_template": self.__value_extractor_ft,
            "parcel": self.__value_extractor_parcel,
        }

    def deserialize(self, *args, **kwargs) -> Tuple[List[Any], Dict[str, Any]]:
        new_args, new_kwargs = self.__transform_model_input(
            self.model, self.__value_extractor, *args, **kwargs
        )
        # Input errors are aggregated and thrown out as a bundle
        self.__check_errors()
        return new_args, new_kwargs

    def __check_errors(self):
        if self._exceptions:
            print(self._exceptions)
            # Put exceptions from current model first
            self._exceptions.sort(key=lambda x: isinstance(x, CatalystwanModelValidationError))
            current_model_errors = sum(
                isinstance(x, CatalystwanModelInputException) for x in self._exceptions
            )
            message = f"{current_model_errors} validation errors for {self.model.__name__}\n"
            for exc in self._exceptions:
                message += f"{exc}\n"
            raise CatalystwanModelValidationError(message)

    def __is_optional(self, t: Any) -> bool:
        if get_origin(t) is Union and type(None) in get_args(t):
            return True
        return False

    def __extract_type(self, field_type: Any, field_value: Any, field_name: str) -> Any:
        origin = get_origin(field_type)
        # check for simple types and classes
        if origin is None:
            if field_type is Any:
                return field_value
            if isinstance(field_value, field_type):
                return field_value
            elif is_dataclass(field_type):
                assert isinstance(field_type, type)
                return deserialize(field_type, **field_value)
            elif isclass(unwrap(field_type)):
                if isinstance(field_value, dict):
                    return field_type(**field_value)
                else:
                    try:
                        return field_type(field_value)
                    except ValueError:
                        raise CatalystwanModelInputException(
                            f"Unable to match or cast input value for {field_name} [expected_type={unwrap(field_type)}, input={field_value}, input_type={type(field_value)}]"
                        )
        elif origin is list:
            if isinstance(field_value, list):
                return [
                    self.__extract_type(get_args(field_type)[0], value, field_name)
                    for value in field_value
                ]
        elif self.__is_optional(field_type):
            if field_value is None:
                return None
            else:
                try:
                    return self.__extract_type(get_args(field_type)[0], field_value, field_name)
                except CatalystwanModelInputException as e:
                    if not field_value:
                        return None
                    raise e
        elif origin is Literal:
            for arg in get_args(field_type):
                try:
                    if type(arg)(field_value) == arg:
                        return type(arg)(field_value)
                except Exception:
                    continue
        elif origin is Annotated:
            validator, caster = field_type.__metadata__
            if validator(field_value):
                return field_value
            return caster(field_value)
        # TODO: Currently, casting is done left-to-right. Searching deeper for a better match may be the way to go.
        elif origin is Union:
            for arg in get_args(field_type):
                try:
                    return self.__extract_type(arg, field_value, field_name)
                except Exception:
                    continue
        # Correct type not found, add exception
        raise CatalystwanModelInputException(
            f"Unable to match or cast input value for {field_name} [expected_type={unwrap(field_type)}, input={field_value}, input_type={type(field_value)}]"
        )

    def __transform_model_input(
        self, cls: Type[T], value_extractor: ValueExtractorCallable, *args, **kwargs
    ):
        args_copy = deque(deepcopy(args))
        kwargs_copy = deepcopy(kwargs)
        new_args = []
        new_kwargs = {}
        field_types = get_type_hints(cls)
        for field in fields(cls):
            if not field.init:
                continue
            field_type = field_types[field.name]
            # check args first
            if len(args_copy) > 0:
                field_value = args_copy.popleft()
                try:
                    new_args.append(
                        self.__extract_type(field_type, value_extractor(field_value), field.name)
                    )
                except (
                    CatalystwanModelInputException,
                    CatalystwanModelValidationError,
                ) as e:
                    self._exceptions.append(e)
                continue

            alias = field.metadata.get("alias", None)
            alias_path = alias if isinstance(alias, AliasPath) else [alias]
            try:
                # get value from given dict path
                field_value = reduce(dict.get, alias_path, kwargs_copy)  # type: ignore[arg-type]
            except TypeError:
                field_value = None
            if field_value is None:
                if field.name in kwargs_copy:
                    field_value = kwargs_copy[field.name]
                else:
                    continue
            try:
                new_kwargs[field.name] = self.__extract_type(
                    field_type, value_extractor(field_value), field.name
                )
            except (
                CatalystwanModelInputException,
                CatalystwanModelValidationError,
            ) as e:
                self._exceptions.append(e)
        return new_args, new_kwargs

    @property
    def __value_extractor(self) -> ValueExtractorCallable:
        return self.VALUE_EXTRACTORS[self.model_type]

    def __value_extractor_base(self, field_value: Any) -> Any:
        return field_value

    def __value_extractor_ft(self, field_value: Any) -> Any:
        if isinstance(field_value, dict):
            if "vipType" in field_value and field_value["vipType"] == "ignore":
                return None
            if "vipValue" in field_value:
                return field_value["vipValue"]
        return field_value

    def __value_extractor_parcel(self, field_value: Any) -> Any:
        if (
            isinstance(field_value, dict)
            and "option_type" in field_value
            and "value" in field_value
        ):
            return field_value["value"]
        return field_value


def deserialize(catalystwan_model: Type[T], *args, **kwargs) -> T:
    new_args, new_kwargs = ModelDeserializer(catalystwan_model).deserialize(*args, **kwargs)

    return catalystwan_model(*new_args, **new_kwargs)
