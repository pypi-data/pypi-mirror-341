from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateProject")


@_attrs_define
class CreateProject:
    """
    Attributes:
        name (str): The name to give to the new project, this must be unique.
        model_version_id (int): The id value of the model version to use in this project. Call GetModels for the list of
            model versions available.
        description (Union[None, Unset, str]): The description for the new project.
        source_run_id (Union[None, Unset, int]): (optional) The id value of an existing run. If specified the new
            project will create a base run
            containing a copy of the data from this run.
        source_project_id (Union[None, Unset, int]): (optional) The id value of an existing project. If specified the
            new project will create a project with a clone of
            all the runs from the source project.
        default_pool (Union[None, Unset, str]): The default pool for the project.
    """

    name: str
    model_version_id: int
    description: Union[None, Unset, str] = UNSET
    source_run_id: Union[None, Unset, int] = UNSET
    source_project_id: Union[None, Unset, int] = UNSET
    default_pool: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        model_version_id = self.model_version_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        source_run_id: Union[None, Unset, int]
        if isinstance(self.source_run_id, Unset):
            source_run_id = UNSET
        else:
            source_run_id = self.source_run_id

        source_project_id: Union[None, Unset, int]
        if isinstance(self.source_project_id, Unset):
            source_project_id = UNSET
        else:
            source_project_id = self.source_project_id

        default_pool: Union[None, Unset, str]
        if isinstance(self.default_pool, Unset):
            default_pool = UNSET
        else:
            default_pool = self.default_pool

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "modelVersionId": model_version_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if source_run_id is not UNSET:
            field_dict["sourceRunId"] = source_run_id
        if source_project_id is not UNSET:
            field_dict["sourceProjectId"] = source_project_id
        if default_pool is not UNSET:
            field_dict["defaultPool"] = default_pool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        model_version_id = d.pop("modelVersionId")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_source_run_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        source_run_id = _parse_source_run_id(d.pop("sourceRunId", UNSET))

        def _parse_source_project_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        source_project_id = _parse_source_project_id(d.pop("sourceProjectId", UNSET))

        def _parse_default_pool(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_pool = _parse_default_pool(d.pop("defaultPool", UNSET))

        create_project = cls(
            name=name,
            model_version_id=model_version_id,
            description=description,
            source_run_id=source_run_id,
            source_project_id=source_project_id,
            default_pool=default_pool,
        )

        return create_project
