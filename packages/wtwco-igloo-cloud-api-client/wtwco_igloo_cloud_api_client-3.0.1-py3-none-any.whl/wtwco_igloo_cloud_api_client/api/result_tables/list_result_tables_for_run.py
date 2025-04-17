from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_wrapper import ResponseWrapper
from ...models.result_table_node_array_response import ResultTableNodeArrayResponse
from ...types import Response


def _get_kwargs(
    workspace_id: int,
    project_id: int,
    run_id: int,
    run_result_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v3/workspaces/{workspace_id}/projects/{project_id}/runs/{run_id}/run-results/{run_result_name}/tables",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]:
    if response.status_code == 406:
        response_406 = ResponseWrapper.from_dict(response.json())

        return response_406
    if response.status_code == 415:
        response_415 = ResponseWrapper.from_dict(response.json())

        return response_415
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 200:
        response_200 = ResultTableNodeArrayResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ResponseWrapper.from_dict(response.json())
        return response_404
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]:
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
    run_result_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]:
    """Lists the collection of result tables in a run result.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        run_result_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        project_id=project_id,
        run_id=run_id,
        run_result_name=run_result_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: int,
    project_id: int,
    run_id: int,
    run_result_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]:
    """Lists the collection of result tables in a run result.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        run_result_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        project_id=project_id,
        run_id=run_id,
        run_result_name=run_result_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    project_id: int,
    run_id: int,
    run_result_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]:
    """Lists the collection of result tables in a run result.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        run_result_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        project_id=project_id,
        run_id=run_id,
        run_result_name=run_result_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    project_id: int,
    run_id: int,
    run_result_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]]:
    """Lists the collection of result tables in a run result.

    Args:
        workspace_id (int):
        project_id (int):
        run_id (int):
        run_result_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResponseWrapper, ResultTableNodeArrayResponse]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            project_id=project_id,
            run_id=run_id,
            run_result_name=run_result_name,
            client=client,
        )
    ).parsed
