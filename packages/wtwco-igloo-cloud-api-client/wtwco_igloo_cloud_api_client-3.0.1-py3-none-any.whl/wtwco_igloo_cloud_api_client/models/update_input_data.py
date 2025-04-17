from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_input_data_table_updates import UpdateInputDataTableUpdates


T = TypeVar("T", bound="UpdateInputData")


@_attrs_define
class UpdateInputData:
    """
    Attributes:
        table_updates (UpdateInputDataTableUpdates): A dictionary of table names with the data changes to make to that
            table.
            The data changes to make to the table are in the form of a dictionary of column names with an associated list of
            values.
            Different columns for the same table must have lists of the same length.

            List tables must have exactly one column name supplied called "Value". The values in the list for this
            column will be used to add new rows to the List table. If a value in the data is already in the list table
            then it is silently ignored so as to support idempotency if the API call is replayed.
            If ReplaceListTables is true then the list table is cleared before the new values are added, allowing old values
            to be removed.
            It is not possible to rename values in list tables using the UpdateInputData API call.

            For other input tables, you must include all of the dimension columns for that table and some of the
            non-dimension columns.
            The values in the dimension columns are used to locate the row to update and the values in the other
            columns are used to update the values there. If a data column is not supplied then the values in that location
            are left unchanged.

            The UpdateInputData API can be called as many times as you like, so you can split up the updates
            by table, by columns or by rows if necessary.

            Note: If the table belongs to a data group that is not owned by this run then the system will automatically
            make a new data group version to contain the modifications to the table. Example: {'TableName1': {'ColumnName1':
            ['Value1', 'Value2', '...', 'ValueK'], 'ColumnName2': ['Value1', 'Value2', '...', 'ValueK']}, 'TableName2':
            {'ColumnName1': ['Value1', 'Value2', '...', 'ValueL'], 'ColumnName2': ['Value1', 'Value2', '...', 'ValueL'],
            'ColumnName3': ['Value1', 'Value2', '...', 'ValueL']}, 'TableName3': {'ColumnName1': ['Value1', 'Value2', '...',
            'ValueM']}}.
        replace_list_tables (Union[Unset, bool]): If true then any old values in list tables that are not in the new
            list supplied will be removed.
    """

    table_updates: "UpdateInputDataTableUpdates"
    replace_list_tables: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        table_updates = self.table_updates.to_dict()

        replace_list_tables = self.replace_list_tables

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "tableUpdates": table_updates,
            }
        )
        if replace_list_tables is not UNSET:
            field_dict["replaceListTables"] = replace_list_tables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.update_input_data_table_updates import UpdateInputDataTableUpdates

        d = src_dict.copy()
        table_updates = UpdateInputDataTableUpdates.from_dict(d.pop("tableUpdates"))

        replace_list_tables = d.pop("replaceListTables", UNSET)

        update_input_data = cls(
            table_updates=table_updates,
            replace_list_tables=replace_list_tables,
        )

        return update_input_data
