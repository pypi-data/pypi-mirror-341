from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.job_state import JobState
from ..types import UNSET, Unset

T = TypeVar("T", bound="JobStatus")


@_attrs_define
class JobStatus:
    """
    Attributes:
        error_message (Union[None, Unset, str]): If non-null then provides a warning or error message that was raised by
            Igloo Cloud when the run was calculated.
        link (Union[None, Unset, str]): Provides a Url to use to view the job on Igloo Cloud.
        state (Union[Unset, JobState]): The state of a Job. This can be one of the following values:
             * InProgress - The job is currently being calculated.
             * Completed - The job has finished calculating and the results are ready to be viewed.
             * Warned - The job has finished calculating and the results are ready to be viewed, however the model emitted a
            warning message.
             * Error - The job has finished calculating, however the model calculation terminated early due to an error.
    """

    error_message: Union[None, Unset, str] = UNSET
    link: Union[None, Unset, str] = UNSET
    state: Union[Unset, JobState] = UNSET

    def to_dict(self) -> dict[str, Any]:
        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if link is not UNSET:
            field_dict["link"] = link
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("errorMessage", UNSET))

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, JobState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = JobState(_state)

        job_status = cls(
            error_message=error_message,
            link=link,
            state=state,
        )

        return job_status
