from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.table_read_only_reason_v2 import TableReadOnlyReasonV2
from ..models.table_type import TableType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column import Column


T = TypeVar("T", bound="TableData")


@_attrs_define
class TableData:
    """
    Attributes:
        self_ (Union[None, str]): This provides a self link to the table including the version and revision of data that
            is currently being used for this run.
        help_ (Union[None, Unset, str]): A link to the help document for this data table. This will be null if there is
            no help document available.
        is_read_only (Union[None, Unset, bool]): Indicates whether the data in this table is editable. If it is read-
            only then the ReadOnlyReason supplies more information as to why.
        read_only_reason (Union[Unset, TableReadOnlyReasonV2]): Indicates the reason why the table is read-only. This
            can be one of the following values:
             * None - The table is not read-only.
             * NotCalculated - The table is read-only because some of the dimension values have changed and the table has
            not yet been updated in response.
             * Result - The table is read-only because it contains the results of a model calculation.
        table_type (Union[Unset, TableType]): The type of table. The value can be one of
             * InputList - Indicates that the table contains a dynamic list of values which can be added, updated or deleted
            from.
             * InputTable - Indicates the table contains a fixed number of rows, one for each set of values in the dimension
            columns. The values in the rows can be updated.
             * ResultTable - Indicates the table contains results from calculating the model. The values cannot be modified.
             * ComparisonInputList - Indicates that the table represents a comparison of input lists. The values cannot be
            modified.
             * ComparisonInputTable - Indicates that the table represents a comparison of input tables. Unlike a normal
            input table, there is no guarantee that all dimension values are present. The values cannot be modified.
             * ComparisonResultTable - Indicates that the table represents a comparison of result tables. The values cannot
            be modified.
        dimensions (Union[None, Unset, list['Column']]): If the table is of type InputTable or ResultTable then this
            will contain the list of columns that are used to define the dimensions of the table.
            If this is an input table and there are no dimension columns then this table will contain just a single row.
        values (Union[None, Unset, list['Column']]): This field contains all of the other columns in the table that are
            not dimension columns.
        data (Union[None, Unset, list[list[Any]]]): This field contains the data in the table. The data is represented
            as a list of rows and each row contains a list of values with one value per column
            in the table in the order that the columns are defined in the dimension and value fields.
            Use the DataType value in the Column definition to determine the type of each value.
    """

    self_: Union[None, str]
    help_: Union[None, Unset, str] = UNSET
    is_read_only: Union[None, Unset, bool] = UNSET
    read_only_reason: Union[Unset, TableReadOnlyReasonV2] = UNSET
    table_type: Union[Unset, TableType] = UNSET
    dimensions: Union[None, Unset, list["Column"]] = UNSET
    values: Union[None, Unset, list["Column"]] = UNSET
    data: Union[None, Unset, list[list[Any]]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        self_: Union[None, str]
        self_ = self.self_

        help_: Union[None, Unset, str]
        if isinstance(self.help_, Unset):
            help_ = UNSET
        else:
            help_ = self.help_

        is_read_only: Union[None, Unset, bool]
        if isinstance(self.is_read_only, Unset):
            is_read_only = UNSET
        else:
            is_read_only = self.is_read_only

        read_only_reason: Union[Unset, str] = UNSET
        if not isinstance(self.read_only_reason, Unset):
            read_only_reason = self.read_only_reason.value

        table_type: Union[Unset, str] = UNSET
        if not isinstance(self.table_type, Unset):
            table_type = self.table_type.value

        dimensions: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.dimensions, Unset):
            dimensions = UNSET
        elif isinstance(self.dimensions, list):
            dimensions = []
            for dimensions_type_0_item_data in self.dimensions:
                dimensions_type_0_item = dimensions_type_0_item_data.to_dict()
                dimensions.append(dimensions_type_0_item)

        else:
            dimensions = self.dimensions

        values: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.values, Unset):
            values = UNSET
        elif isinstance(self.values, list):
            values = []
            for values_type_0_item_data in self.values:
                values_type_0_item = values_type_0_item_data.to_dict()
                values.append(values_type_0_item)

        else:
            values = self.values

        data: Union[None, Unset, list[list[Any]]]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, list):
            data = []
            for data_type_0_item_data in self.data:
                data_type_0_item = data_type_0_item_data

                data.append(data_type_0_item)

        else:
            data = self.data

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "self": self_,
            }
        )
        if help_ is not UNSET:
            field_dict["help"] = help_
        if is_read_only is not UNSET:
            field_dict["isReadOnly"] = is_read_only
        if read_only_reason is not UNSET:
            field_dict["readOnlyReason"] = read_only_reason
        if table_type is not UNSET:
            field_dict["tableType"] = table_type
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if values is not UNSET:
            field_dict["values"] = values
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.column import Column

        d = src_dict.copy()

        def _parse_self_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        self_ = _parse_self_(d.pop("self"))

        def _parse_help_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        help_ = _parse_help_(d.pop("help", UNSET))

        def _parse_is_read_only(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_read_only = _parse_is_read_only(d.pop("isReadOnly", UNSET))

        _read_only_reason = d.pop("readOnlyReason", UNSET)
        read_only_reason: Union[Unset, TableReadOnlyReasonV2]
        if isinstance(_read_only_reason, Unset):
            read_only_reason = UNSET
        else:
            read_only_reason = TableReadOnlyReasonV2(_read_only_reason)

        _table_type = d.pop("tableType", UNSET)
        table_type: Union[Unset, TableType]
        if isinstance(_table_type, Unset):
            table_type = UNSET
        else:
            table_type = TableType(_table_type)

        def _parse_dimensions(data: object) -> Union[None, Unset, list["Column"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                dimensions_type_0 = []
                _dimensions_type_0 = data
                for dimensions_type_0_item_data in _dimensions_type_0:
                    dimensions_type_0_item = Column.from_dict(dimensions_type_0_item_data)

                    dimensions_type_0.append(dimensions_type_0_item)

                return dimensions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Column"]], data)

        dimensions = _parse_dimensions(d.pop("dimensions", UNSET))

        def _parse_values(data: object) -> Union[None, Unset, list["Column"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                values_type_0 = []
                _values_type_0 = data
                for values_type_0_item_data in _values_type_0:
                    values_type_0_item = Column.from_dict(values_type_0_item_data)

                    values_type_0.append(values_type_0_item)

                return values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Column"]], data)

        values = _parse_values(d.pop("values", UNSET))

        def _parse_data(data: object) -> Union[None, Unset, list[list[Any]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_type_0 = []
                _data_type_0 = data
                for data_type_0_item_data in _data_type_0:
                    data_type_0_item = cast(list[Any], data_type_0_item_data)

                    data_type_0.append(data_type_0_item)

                return data_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[list[Any]]], data)

        data = _parse_data(d.pop("data", UNSET))

        table_data = cls(
            self_=self_,
            help_=help_,
            is_read_only=is_read_only,
            read_only_reason=read_only_reason,
            table_type=table_type,
            dimensions=dimensions,
            values=values,
            data=data,
        )

        return table_data
