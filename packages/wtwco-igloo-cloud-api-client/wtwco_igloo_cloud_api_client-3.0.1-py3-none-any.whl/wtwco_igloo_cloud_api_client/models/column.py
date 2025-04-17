from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.data_type import DataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.links import Links


T = TypeVar("T", bound="Column")


@_attrs_define
class Column:
    """
    Attributes:
        name (Union[None, Unset, str]): The name of the column, this can be used to refer to this column in other API
            calls such as UpdateInputData
        display_name (Union[None, Unset, str]): The user-friendly display name for this column.
        description (Union[None, Unset, str]): A description, supplied by the model developer, to describe the purpose
            of this column.
        data_type (Union[Unset, DataType]): The data type of the column. This can be one of the following values:
             * Id - A 64-bit integer which is used to identify a row in a list tables. For instance dimension columns in
            input tables use this data type to identify the dimension value in the list table associated with the dimension
            column.
             * Position - A 32-bit integer which is used to specify the order for displaying values in a list table. This
            data type will only be found in list tables.
             * Integer - A 32-bit integer.
             * Real - A 64-bit floating point number.
             * String - A string of characters containing at most MaxLength characters.
             * Boolean - A boolean value.
             * Date - A date and time value.
             * File - A reference to an uploaded file. The value will be the id of an uploaded file represented as a string.
             * RunArtifact - A reference to an artifact produced by another run. The value will be the id of a run
            represented as a string.
        max_length (Union[None, Unset, int]): Set to the maximum length of string values for this column if applicable
            for the data type.
        file_type_specifier (Union[None, Unset, str]): Set to the file extension of the file type required by this
            column if the data type is File.
        links (Union[Unset, Links]): Provides the URL to use to fetch the values of the list table if this column is of
            type Id.
        model_name (Union[None, Unset, str]): The name of the model that can provide run artifacts for this column if
            the data type is RunArtifact.
        minimum_version (Union[None, Unset, str]): The minimum version of the model that can provide run artifacts for
            this column if the data type is RunArtifact.
        values (Union[None, Unset, list[Any]]): If supplied, provides the full set of values of a dimension column, in
            the order that they should be displayed.
            Use DataType to determine the type of the values.
            Links.Self and Values will not both be present in the dto, however it is possible that neither will be present
            in which case the dimension values should be deduced from the data in the table.
    """

    name: Union[None, Unset, str] = UNSET
    display_name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    data_type: Union[Unset, DataType] = UNSET
    max_length: Union[None, Unset, int] = UNSET
    file_type_specifier: Union[None, Unset, str] = UNSET
    links: Union[Unset, "Links"] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    minimum_version: Union[None, Unset, str] = UNSET
    values: Union[None, Unset, list[Any]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        display_name: Union[None, Unset, str]
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        data_type: Union[Unset, str] = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = self.data_type.value

        max_length: Union[None, Unset, int]
        if isinstance(self.max_length, Unset):
            max_length = UNSET
        else:
            max_length = self.max_length

        file_type_specifier: Union[None, Unset, str]
        if isinstance(self.file_type_specifier, Unset):
            file_type_specifier = UNSET
        else:
            file_type_specifier = self.file_type_specifier

        links: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        model_name: Union[None, Unset, str]
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        minimum_version: Union[None, Unset, str]
        if isinstance(self.minimum_version, Unset):
            minimum_version = UNSET
        else:
            minimum_version = self.minimum_version

        values: Union[None, Unset, list[Any]]
        if isinstance(self.values, Unset):
            values = UNSET
        elif isinstance(self.values, list):
            values = self.values

        else:
            values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if max_length is not UNSET:
            field_dict["maxLength"] = max_length
        if file_type_specifier is not UNSET:
            field_dict["fileTypeSpecifier"] = file_type_specifier
        if links is not UNSET:
            field_dict["links"] = links
        if model_name is not UNSET:
            field_dict["modelName"] = model_name
        if minimum_version is not UNSET:
            field_dict["minimumVersion"] = minimum_version
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.links import Links

        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_display_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        display_name = _parse_display_name(d.pop("displayName", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _data_type = d.pop("dataType", UNSET)
        data_type: Union[Unset, DataType]
        if isinstance(_data_type, Unset):
            data_type = UNSET
        else:
            data_type = DataType(_data_type)

        def _parse_max_length(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_length = _parse_max_length(d.pop("maxLength", UNSET))

        def _parse_file_type_specifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        file_type_specifier = _parse_file_type_specifier(d.pop("fileTypeSpecifier", UNSET))

        _links = d.pop("links", UNSET)
        links: Union[Unset, Links]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = Links.from_dict(_links)

        def _parse_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_name = _parse_model_name(d.pop("modelName", UNSET))

        def _parse_minimum_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        minimum_version = _parse_minimum_version(d.pop("minimumVersion", UNSET))

        def _parse_values(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                values_type_0 = cast(list[Any], data)

                return values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        values = _parse_values(d.pop("values", UNSET))

        column = cls(
            name=name,
            display_name=display_name,
            description=description,
            data_type=data_type,
            max_length=max_length,
            file_type_specifier=file_type_specifier,
            links=links,
            model_name=model_name,
            minimum_version=minimum_version,
            values=values,
        )

        return column
