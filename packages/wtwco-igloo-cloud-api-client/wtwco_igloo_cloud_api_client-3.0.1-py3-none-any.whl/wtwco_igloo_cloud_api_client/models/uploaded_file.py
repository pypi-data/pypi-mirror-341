import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadedFile")


@_attrs_define
class UploadedFile:
    """
    Attributes:
        id (Union[Unset, int]): The id value of this uploaded file.
        workspace_id (Union[Unset, int]): The id of the workspace containing this file.
        name (Union[None, Unset, str]): The name of this uploaded file.
        extension (Union[None, Unset, str]): The file extension of the uploaded file.
        description (Union[None, Unset, str]): The description of the uploaded file.
        upload_status (Union[None, Unset, str]): Indicates the upload status of this file. One of UploadNotStarted,
            Uploading, UploadCompleting, Uploaded or UploadFailedOrCancelled.
        uploaded_by (Union[None, Unset, str]): The name of the user who uploaded the content of this file.
        upload_start_time (Union[None, Unset, datetime.datetime]): The date and time when the file upload process was
            initiated.
        upload_percent (Union[Unset, int]): How much of the content has been uploaded to Azure blob storage.
        size_in_bytes (Union[None, Unset, int]): The total size of the file content.
        run_count (Union[Unset, int]): The number of runs whose input data reference this file.
        file_upload_identifier (Union[None, Unset, str]): The upload identifier to use in calls to UpdateProgress or
            CancelUpload.
    """

    id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    extension: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    upload_status: Union[None, Unset, str] = UNSET
    uploaded_by: Union[None, Unset, str] = UNSET
    upload_start_time: Union[None, Unset, datetime.datetime] = UNSET
    upload_percent: Union[Unset, int] = UNSET
    size_in_bytes: Union[None, Unset, int] = UNSET
    run_count: Union[Unset, int] = UNSET
    file_upload_identifier: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        workspace_id = self.workspace_id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        extension: Union[None, Unset, str]
        if isinstance(self.extension, Unset):
            extension = UNSET
        else:
            extension = self.extension

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        upload_status: Union[None, Unset, str]
        if isinstance(self.upload_status, Unset):
            upload_status = UNSET
        else:
            upload_status = self.upload_status

        uploaded_by: Union[None, Unset, str]
        if isinstance(self.uploaded_by, Unset):
            uploaded_by = UNSET
        else:
            uploaded_by = self.uploaded_by

        upload_start_time: Union[None, Unset, str]
        if isinstance(self.upload_start_time, Unset):
            upload_start_time = UNSET
        elif isinstance(self.upload_start_time, datetime.datetime):
            upload_start_time = self.upload_start_time.isoformat()
        else:
            upload_start_time = self.upload_start_time

        upload_percent = self.upload_percent

        size_in_bytes: Union[None, Unset, int]
        if isinstance(self.size_in_bytes, Unset):
            size_in_bytes = UNSET
        else:
            size_in_bytes = self.size_in_bytes

        run_count = self.run_count

        file_upload_identifier: Union[None, Unset, str]
        if isinstance(self.file_upload_identifier, Unset):
            file_upload_identifier = UNSET
        else:
            file_upload_identifier = self.file_upload_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id
        if name is not UNSET:
            field_dict["name"] = name
        if extension is not UNSET:
            field_dict["extension"] = extension
        if description is not UNSET:
            field_dict["description"] = description
        if upload_status is not UNSET:
            field_dict["uploadStatus"] = upload_status
        if uploaded_by is not UNSET:
            field_dict["uploadedBy"] = uploaded_by
        if upload_start_time is not UNSET:
            field_dict["uploadStartTime"] = upload_start_time
        if upload_percent is not UNSET:
            field_dict["uploadPercent"] = upload_percent
        if size_in_bytes is not UNSET:
            field_dict["sizeInBytes"] = size_in_bytes
        if run_count is not UNSET:
            field_dict["runCount"] = run_count
        if file_upload_identifier is not UNSET:
            field_dict["fileUploadIdentifier"] = file_upload_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        workspace_id = d.pop("workspaceId", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_extension(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extension = _parse_extension(d.pop("extension", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_upload_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        upload_status = _parse_upload_status(d.pop("uploadStatus", UNSET))

        def _parse_uploaded_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        uploaded_by = _parse_uploaded_by(d.pop("uploadedBy", UNSET))

        def _parse_upload_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                upload_start_time_type_0 = isoparse(data)

                return upload_start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        upload_start_time = _parse_upload_start_time(d.pop("uploadStartTime", UNSET))

        upload_percent = d.pop("uploadPercent", UNSET)

        def _parse_size_in_bytes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        size_in_bytes = _parse_size_in_bytes(d.pop("sizeInBytes", UNSET))

        run_count = d.pop("runCount", UNSET)

        def _parse_file_upload_identifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        file_upload_identifier = _parse_file_upload_identifier(d.pop("fileUploadIdentifier", UNSET))

        uploaded_file = cls(
            id=id,
            workspace_id=workspace_id,
            name=name,
            extension=extension,
            description=description,
            upload_status=upload_status,
            uploaded_by=uploaded_by,
            upload_start_time=upload_start_time,
            upload_percent=upload_percent,
            size_in_bytes=size_in_bytes,
            run_count=run_count,
            file_upload_identifier=file_upload_identifier,
        )

        return uploaded_file
