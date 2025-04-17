from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreateJob")


@_attrs_define
class CreateJob:
    """
    Attributes:
        project_id (int): The id of the project that contains the run you wish to calculate.
        run_id (int): The id of the run that you wish to calculate.
        pool (str): The name of the pool you wish to use to calculate the model.
    """

    project_id: int
    run_id: int
    pool: str

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        run_id = self.run_id

        pool = self.pool

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "projectId": project_id,
                "runId": run_id,
                "pool": pool,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId")

        run_id = d.pop("runId")

        pool = d.pop("pool")

        create_job = cls(
            project_id=project_id,
            run_id=run_id,
            pool=pool,
        )

        return create_job
