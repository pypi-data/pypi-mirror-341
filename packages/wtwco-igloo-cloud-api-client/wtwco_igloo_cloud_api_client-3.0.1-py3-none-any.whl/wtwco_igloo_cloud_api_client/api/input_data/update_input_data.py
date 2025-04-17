from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_wrapper import ResponseWrapper
from ...models.update_input_data import UpdateInputData
from ...types import Response


def _get_kwargs(
    workspace_id: int,
    project_id: int,
    run_id: int,
    *,
    body: UpdateInputData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/v3/workspaces/{workspace_id}/projects/{project_id}/runs/{run_id}/input-data",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseWrapper]]:
    if response.status_code == 406:
        response_406 = ResponseWrapper.from_dict(response.json())

        return response_406
    if response.status_code == 415:
        response_415 = ResponseWrapper.from_dict(response.json())

        return response_415
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = ResponseWrapper.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = ResponseWrapper.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = ResponseWrapper.from_dict(response.json())
        return response_409
    if response.status_code == 410:
        response_410 = ResponseWrapper.from_dict(response.json())
        return response_410
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ResponseWrapper]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: int,
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInputData,
) -> Response[Union[Any, ResponseWrapper]]:
    """Update the input data in a table for a run.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        project_id=project_id,
        run_id=run_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: int,
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInputData,
) -> Optional[Union[Any, ResponseWrapper]]:
    """Update the input data in a table for a run.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        project_id=project_id,
        run_id=run_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInputData,
) -> Response[Union[Any, ResponseWrapper]]:
    """Update the input data in a table for a run.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        project_id=project_id,
        run_id=run_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    project_id: int,
    run_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInputData,
) -> Optional[Union[Any, ResponseWrapper]]:
    """Update the input data in a table for a run.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        body (UpdateInputData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            project_id=project_id,
            run_id=run_id,
            client=client,
            body=body,
        )
    ).parsed
