from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.input_data_data_type_0 import InputDataDataType0


T = TypeVar("T", bound="InputData")


@_attrs_define
class InputData:
    """
    Attributes:
        data (Union['InputDataDataType0', None]): A dictionary of column names mapped to a list of values containing the
            data in the table associated with that column.
    """

    data: Union["InputDataDataType0", None]

    def to_dict(self) -> dict[str, Any]:
        from ..models.input_data_data_type_0 import InputDataDataType0

        data: Union[None, dict[str, Any]]
        if isinstance(self.data, InputDataDataType0):
            data = self.data.to_dict()
        else:
            data = self.data

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.input_data_data_type_0 import InputDataDataType0

        d = src_dict.copy()

        def _parse_data(data: object) -> Union["InputDataDataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = InputDataDataType0.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["InputDataDataType0", None], data)

        data = _parse_data(d.pop("data"))

        input_data = cls(
            data=data,
        )

        return input_data
