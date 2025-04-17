import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.run_state import RunState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.owned_data_group import OwnedDataGroup


T = TypeVar("T", bound="Run")


@_attrs_define
class Run:
    """
    Attributes:
        job_id (Union[None, int]): The Job id of the job that calculated this run, or null if the run is not calculated
            or being calculated.
        id (Union[Unset, int]): The id value of this run.
        project_id (Union[Unset, int]): The id of the project.
        workspace_id (Union[Unset, int]): The id of the workspace.
        name (Union[None, Unset, str]): The name for this run.
        parent_id (Union[None, Unset, int]): The id of our parent run, or null if we are the base run in the project.
        description (Union[None, Unset, str]): The description of this run.
        auto_deletion_time (Union[None, Unset, datetime.datetime]): If this value is non-null then it specified the date
            and time after which the run may be automatically deleted.
        state (Union[Unset, RunState]): The state of a Run. This can be one of the following values:
             * Processing - The input data is not ready to be viewed, this may be because the run is being initialised or
            some processing is happening as the result of a recent input data change.
             * Uncalculated - The run has not been calculated since the input data was last modified.
             * InProgress - The run is currently being calculated.
             * Completed - The run has been calculated for the latest input data changes and the results are ready to be
            viewed.
             * Warned - The run has been calculated for the latest input data changes and the results are ready to be
            viewed, however the model emitted a warning message.
             * Error - The run failed to calculate with the latest input data changes.
        owned_data_groups (Union[None, Unset, list['OwnedDataGroup']]): A list of data groups whose data has been
            modified by this run.
        job_link (Union[None, Unset, str]): If non-null then provides a Url to use to view the job on Igloo Cloud which
            calculated this run.
        job_error (Union[None, Unset, str]): If non-null then provides a warning or error message that was raised by
            Igloo Cloud when the run was calculated.
    """

    job_id: Union[None, int]
    id: Union[Unset, int] = UNSET
    project_id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    parent_id: Union[None, Unset, int] = UNSET
    description: Union[None, Unset, str] = UNSET
    auto_deletion_time: Union[None, Unset, datetime.datetime] = UNSET
    state: Union[Unset, RunState] = UNSET
    owned_data_groups: Union[None, Unset, list["OwnedDataGroup"]] = UNSET
    job_link: Union[None, Unset, str] = UNSET
    job_error: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        job_id: Union[None, int]
        job_id = self.job_id

        id = self.id

        project_id = self.project_id

        workspace_id = self.workspace_id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        parent_id: Union[None, Unset, int]
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        auto_deletion_time: Union[None, Unset, str]
        if isinstance(self.auto_deletion_time, Unset):
            auto_deletion_time = UNSET
        elif isinstance(self.auto_deletion_time, datetime.datetime):
            auto_deletion_time = self.auto_deletion_time.isoformat()
        else:
            auto_deletion_time = self.auto_deletion_time

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        owned_data_groups: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.owned_data_groups, Unset):
            owned_data_groups = UNSET
        elif isinstance(self.owned_data_groups, list):
            owned_data_groups = []
            for owned_data_groups_type_0_item_data in self.owned_data_groups:
                owned_data_groups_type_0_item = owned_data_groups_type_0_item_data.to_dict()
                owned_data_groups.append(owned_data_groups_type_0_item)

        else:
            owned_data_groups = self.owned_data_groups

        job_link: Union[None, Unset, str]
        if isinstance(self.job_link, Unset):
            job_link = UNSET
        else:
            job_link = self.job_link

        job_error: Union[None, Unset, str]
        if isinstance(self.job_error, Unset):
            job_error = UNSET
        else:
            job_error = self.job_error

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "jobId": job_id,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id
        if name is not UNSET:
            field_dict["name"] = name
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if description is not UNSET:
            field_dict["description"] = description
        if auto_deletion_time is not UNSET:
            field_dict["autoDeletionTime"] = auto_deletion_time
        if state is not UNSET:
            field_dict["state"] = state
        if owned_data_groups is not UNSET:
            field_dict["ownedDataGroups"] = owned_data_groups
        if job_link is not UNSET:
            field_dict["jobLink"] = job_link
        if job_error is not UNSET:
            field_dict["jobError"] = job_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.owned_data_group import OwnedDataGroup

        d = src_dict.copy()

        def _parse_job_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        job_id = _parse_job_id(d.pop("jobId"))

        id = d.pop("id", UNSET)

        project_id = d.pop("projectId", UNSET)

        workspace_id = d.pop("workspaceId", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_parent_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        parent_id = _parse_parent_id(d.pop("parentId", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_auto_deletion_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                auto_deletion_time_type_0 = isoparse(data)

                return auto_deletion_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        auto_deletion_time = _parse_auto_deletion_time(d.pop("autoDeletionTime", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, RunState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = RunState(_state)

        def _parse_owned_data_groups(data: object) -> Union[None, Unset, list["OwnedDataGroup"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                owned_data_groups_type_0 = []
                _owned_data_groups_type_0 = data
                for owned_data_groups_type_0_item_data in _owned_data_groups_type_0:
                    owned_data_groups_type_0_item = OwnedDataGroup.from_dict(owned_data_groups_type_0_item_data)

                    owned_data_groups_type_0.append(owned_data_groups_type_0_item)

                return owned_data_groups_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["OwnedDataGroup"]], data)

        owned_data_groups = _parse_owned_data_groups(d.pop("ownedDataGroups", UNSET))

        def _parse_job_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        job_link = _parse_job_link(d.pop("jobLink", UNSET))

        def _parse_job_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        job_error = _parse_job_error(d.pop("jobError", UNSET))

        run = cls(
            job_id=job_id,
            id=id,
            project_id=project_id,
            workspace_id=workspace_id,
            name=name,
            parent_id=parent_id,
            description=description,
            auto_deletion_time=auto_deletion_time,
            state=state,
            owned_data_groups=owned_data_groups,
            job_link=job_link,
            job_error=job_error,
        )

        return run
