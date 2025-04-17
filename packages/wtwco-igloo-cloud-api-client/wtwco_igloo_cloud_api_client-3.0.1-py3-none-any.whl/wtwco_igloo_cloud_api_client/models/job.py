import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.id_and_name import IdAndName
    from ..models.job_status import JobStatus


T = TypeVar("T", bound="Job")


@_attrs_define
class Job:
    """
    Attributes:
        id (Union[Unset, int]): The id value of this job.
        workspace_id (Union[Unset, int]): The id of the workspace.
        project (Union[Unset, IdAndName]):
        run (Union[Unset, IdAndName]):
        status (Union[Unset, JobStatus]):
        start_time (Union[None, Unset, datetime.datetime]): The date and time when this job was submitted.
        finish_time (Union[None, Unset, datetime.datetime]): If non-null, supplies the date and time this job finished.
        user_name (Union[None, Unset, str]): The name of the user that submitted the job.
        pool (Union[None, Unset, str]): The name of the pool used to calculate the job.
    """

    id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, int] = UNSET
    project: Union[Unset, "IdAndName"] = UNSET
    run: Union[Unset, "IdAndName"] = UNSET
    status: Union[Unset, "JobStatus"] = UNSET
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    finish_time: Union[None, Unset, datetime.datetime] = UNSET
    user_name: Union[None, Unset, str] = UNSET
    pool: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        workspace_id = self.workspace_id

        project: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.project, Unset):
            project = self.project.to_dict()

        run: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.run, Unset):
            run = self.run.to_dict()

        status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        finish_time: Union[None, Unset, str]
        if isinstance(self.finish_time, Unset):
            finish_time = UNSET
        elif isinstance(self.finish_time, datetime.datetime):
            finish_time = self.finish_time.isoformat()
        else:
            finish_time = self.finish_time

        user_name: Union[None, Unset, str]
        if isinstance(self.user_name, Unset):
            user_name = UNSET
        else:
            user_name = self.user_name

        pool: Union[None, Unset, str]
        if isinstance(self.pool, Unset):
            pool = UNSET
        else:
            pool = self.pool

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id
        if project is not UNSET:
            field_dict["project"] = project
        if run is not UNSET:
            field_dict["run"] = run
        if status is not UNSET:
            field_dict["status"] = status
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if finish_time is not UNSET:
            field_dict["finishTime"] = finish_time
        if user_name is not UNSET:
            field_dict["userName"] = user_name
        if pool is not UNSET:
            field_dict["pool"] = pool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.id_and_name import IdAndName
        from ..models.job_status import JobStatus

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        workspace_id = d.pop("workspaceId", UNSET)

        _project = d.pop("project", UNSET)
        project: Union[Unset, IdAndName]
        if isinstance(_project, Unset):
            project = UNSET
        else:
            project = IdAndName.from_dict(_project)

        _run = d.pop("run", UNSET)
        run: Union[Unset, IdAndName]
        if isinstance(_run, Unset):
            run = UNSET
        else:
            run = IdAndName.from_dict(_run)

        _status = d.pop("status", UNSET)
        status: Union[Unset, JobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = JobStatus.from_dict(_status)

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("startTime", UNSET))

        def _parse_finish_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finish_time_type_0 = isoparse(data)

                return finish_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        finish_time = _parse_finish_time(d.pop("finishTime", UNSET))

        def _parse_user_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_name = _parse_user_name(d.pop("userName", UNSET))

        def _parse_pool(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pool = _parse_pool(d.pop("pool", UNSET))

        job = cls(
            id=id,
            workspace_id=workspace_id,
            project=project,
            run=run,
            status=status,
            start_time=start_time,
            finish_time=finish_time,
            user_name=user_name,
            pool=pool,
        )

        return job
