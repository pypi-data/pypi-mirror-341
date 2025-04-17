from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.output_data_status import OutputDataStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.output_data_output_tables_type_0 import OutputDataOutputTablesType0


T = TypeVar("T", bound="OutputData")


@_attrs_define
class OutputData:
    """
    Attributes:
        run_status (Union[Unset, OutputDataStatus]): Indicates the state of the Run containing the output data, this may
            be one of:
              * Calculating - The run is currently being calculated.
              * ModelError - The model calculation terminated early due to an error.
              * Done - The run has been calculated for the latest input data changes and the results are ready to be viewed.
        model_error (Union[None, Unset, str]): Set to the error message from the model if RunStatus equals ModelError.
        output_tables (Union['OutputDataOutputTablesType0', None, Unset]): Set only if the RunStatus equals Done. Will
            contain all of the output data for that run, or a single table if requested, in the format: Example:
            {'TableName1': {'ColumnName1': ['Value1', 'Value2', '...', 'ValueK'], 'ColumnName2': ['Value1', 'Value2', '...',
            'ValueK']}, 'TableName2': {'ColumnName1': ['Value1', 'Value2', '...', 'ValueL'], 'ColumnName2': ['Value1',
            'Value2', '...', 'ValueL'], 'ColumnName3': ['Value1', 'Value2', '...', 'ValueL']}, 'TableName3': {'ColumnName1':
            ['Value1', 'Value2', '...', 'ValueM']}}.
    """

    run_status: Union[Unset, OutputDataStatus] = UNSET
    model_error: Union[None, Unset, str] = UNSET
    output_tables: Union["OutputDataOutputTablesType0", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.output_data_output_tables_type_0 import OutputDataOutputTablesType0

        run_status: Union[Unset, str] = UNSET
        if not isinstance(self.run_status, Unset):
            run_status = self.run_status.value

        model_error: Union[None, Unset, str]
        if isinstance(self.model_error, Unset):
            model_error = UNSET
        else:
            model_error = self.model_error

        output_tables: Union[None, Unset, dict[str, Any]]
        if isinstance(self.output_tables, Unset):
            output_tables = UNSET
        elif isinstance(self.output_tables, OutputDataOutputTablesType0):
            output_tables = self.output_tables.to_dict()
        else:
            output_tables = self.output_tables

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if run_status is not UNSET:
            field_dict["runStatus"] = run_status
        if model_error is not UNSET:
            field_dict["modelError"] = model_error
        if output_tables is not UNSET:
            field_dict["outputTables"] = output_tables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.output_data_output_tables_type_0 import OutputDataOutputTablesType0

        d = src_dict.copy()
        _run_status = d.pop("runStatus", UNSET)
        run_status: Union[Unset, OutputDataStatus]
        if isinstance(_run_status, Unset):
            run_status = UNSET
        else:
            run_status = OutputDataStatus(_run_status)

        def _parse_model_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_error = _parse_model_error(d.pop("modelError", UNSET))

        def _parse_output_tables(data: object) -> Union["OutputDataOutputTablesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_tables_type_0 = OutputDataOutputTablesType0.from_dict(data)

                return output_tables_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OutputDataOutputTablesType0", None, Unset], data)

        output_tables = _parse_output_tables(d.pop("outputTables", UNSET))

        output_data = cls(
            run_status=run_status,
            model_error=model_error,
            output_tables=output_tables,
        )

        return output_data
