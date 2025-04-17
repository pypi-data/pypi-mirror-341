from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_workspace import CreateWorkspace
from ...models.response_wrapper import ResponseWrapper
from ...models.workspace_response import WorkspaceResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CreateWorkspace,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v3/workspaces",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseWrapper, WorkspaceResponse]]:
    if response.status_code == 406:
        response_406 = ResponseWrapper.from_dict(response.json())

        return response_406
    if response.status_code == 415:
        response_415 = ResponseWrapper.from_dict(response.json())

        return response_415
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 201:
        response_201 = WorkspaceResponse.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ResponseWrapper.from_dict(response.json())
        return response_400
    if response.status_code == 409:
        response_409 = ResponseWrapper.from_dict(response.json())
        return response_409
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ResponseWrapper, WorkspaceResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkspace,
) -> Response[Union[Any, ResponseWrapper, WorkspaceResponse]]:
    """Create a new workspace to manage projects and files.

    Args:
        body (CreateWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper, WorkspaceResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkspace,
) -> Optional[Union[Any, ResponseWrapper, WorkspaceResponse]]:
    """Create a new workspace to manage projects and files.

    Args:
        body (CreateWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper, WorkspaceResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkspace,
) -> Response[Union[Any, ResponseWrapper, WorkspaceResponse]]:
    """Create a new workspace to manage projects and files.

    Args:
        body (CreateWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper, WorkspaceResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkspace,
) -> Optional[Union[Any, ResponseWrapper, WorkspaceResponse]]:
    """Create a new workspace to manage projects and files.

    Args:
        body (CreateWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper, WorkspaceResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
