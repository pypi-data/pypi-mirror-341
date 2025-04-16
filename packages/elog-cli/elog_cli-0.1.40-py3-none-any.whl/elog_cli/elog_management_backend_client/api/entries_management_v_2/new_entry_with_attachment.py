from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_string import ApiResultResponseString
from ...models.new_entry_with_attachment_body import NewEntryWithAttachmentBody
from ...types import Response


def _get_kwargs(
    *,
    body: NewEntryWithAttachmentBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/entries",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseString]:
    if response.status_code == 201:
        response_201 = ApiResultResponseString.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ApiResultResponseString.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ApiResultResponseString.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ApiResultResponseString.from_dict(response.json())

        return response_403
    if response.status_code == 500:
        response_500 = ApiResultResponseString.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseString]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEntryWithAttachmentBody,
) -> Response[ApiResultResponseString]:
    """Create new entry with attachments

     Creates a new electronic log entry along with optional file attachments. This API endpoint accepts
    multipart/form-data requests. The 'entry' part must contain a valid JSON payload corresponding to
    the NewEntryDTO schema, which defines the log entry details. The 'files' part is optional and may
    include one or more attachments. The operation requires the user to be authenticated and authorized
    to create an entry.

    Args:
        body (NewEntryWithAttachmentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
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
    body: NewEntryWithAttachmentBody,
) -> Optional[ApiResultResponseString]:
    """Create new entry with attachments

     Creates a new electronic log entry along with optional file attachments. This API endpoint accepts
    multipart/form-data requests. The 'entry' part must contain a valid JSON payload corresponding to
    the NewEntryDTO schema, which defines the log entry details. The 'files' part is optional and may
    include one or more attachments. The operation requires the user to be authenticated and authorized
    to create an entry.

    Args:
        body (NewEntryWithAttachmentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEntryWithAttachmentBody,
) -> Response[ApiResultResponseString]:
    """Create new entry with attachments

     Creates a new electronic log entry along with optional file attachments. This API endpoint accepts
    multipart/form-data requests. The 'entry' part must contain a valid JSON payload corresponding to
    the NewEntryDTO schema, which defines the log entry details. The 'files' part is optional and may
    include one or more attachments. The operation requires the user to be authenticated and authorized
    to create an entry.

    Args:
        body (NewEntryWithAttachmentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEntryWithAttachmentBody,
) -> Optional[ApiResultResponseString]:
    """Create new entry with attachments

     Creates a new electronic log entry along with optional file attachments. This API endpoint accepts
    multipart/form-data requests. The 'entry' part must contain a valid JSON payload corresponding to
    the NewEntryDTO schema, which defines the log entry details. The 'files' part is optional and may
    include one or more attachments. The operation requires the user to be authenticated and authorized
    to create an entry.

    Args:
        body (NewEntryWithAttachmentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
