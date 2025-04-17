from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """
    Attributes:
        id (Union[Unset, int]): The id value of this project.
        workspace_id (Union[Unset, int]): The id of the workspace containing this project.
        base_run_id (Union[Unset, int]): The id of the base run for this project.
        name (Union[None, Unset, str]): The name for this project.
        description (Union[None, Unset, str]): The description of the project.
        run_count (Union[Unset, int]): The number of runs of this project.
        model_version_id (Union[Unset, int]): The id of the model version used by the project.
        default_pool (Union[None, Unset, str]): The default pool for the project.
    """

    id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, int] = UNSET
    base_run_id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    run_count: Union[Unset, int] = UNSET
    model_version_id: Union[Unset, int] = UNSET
    default_pool: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        workspace_id = self.workspace_id

        base_run_id = self.base_run_id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        run_count = self.run_count

        model_version_id = self.model_version_id

        default_pool: Union[None, Unset, str]
        if isinstance(self.default_pool, Unset):
            default_pool = UNSET
        else:
            default_pool = self.default_pool

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id
        if base_run_id is not UNSET:
            field_dict["baseRunId"] = base_run_id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if run_count is not UNSET:
            field_dict["runCount"] = run_count
        if model_version_id is not UNSET:
            field_dict["modelVersionId"] = model_version_id
        if default_pool is not UNSET:
            field_dict["defaultPool"] = default_pool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        workspace_id = d.pop("workspaceId", UNSET)

        base_run_id = d.pop("baseRunId", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        run_count = d.pop("runCount", UNSET)

        model_version_id = d.pop("modelVersionId", UNSET)

        def _parse_default_pool(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_pool = _parse_default_pool(d.pop("defaultPool", UNSET))

        project = cls(
            id=id,
            workspace_id=workspace_id,
            base_run_id=base_run_id,
            name=name,
            description=description,
            run_count=run_count,
            model_version_id=model_version_id,
            default_pool=default_pool,
        )

        return project
