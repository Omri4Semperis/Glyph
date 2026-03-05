"""
Azure DevOps integration tools for Glyph MCP.

Provides tools to fetch and query work items (PBIs, Tasks, Bugs, etc.)
from an Azure DevOps project using a Personal Access Token (PAT).
"""

import base64
import json
import urllib.request
import urllib.error
from typing import Any

from mcp_object import mcp
from response import GlyphMCPResponse

_ADO_API_VERSION = "7.0"

# Fields to expand when fetching work items
_EXPAND_FIELDS = [
    "System.Id",
    "System.Title",
    "System.WorkItemType",
    "System.State",
    "System.Description",
    "System.AssignedTo",
    "System.AreaPath",
    "System.IterationPath",
    "System.Tags",
    "System.CreatedBy",
    "System.ChangedDate",
    "Microsoft.VSTS.Common.AcceptanceCriteria",
    "Microsoft.VSTS.Common.Priority",
    "Microsoft.VSTS.Scheduling.StoryPoints",
    "Microsoft.VSTS.Scheduling.Effort",
    "Microsoft.VSTS.Scheduling.RemainingWork",
]


def _build_auth_header(pat: str) -> str:
    """Build the Basic Authorization header value for a PAT."""
    encoded = base64.b64encode(f":{pat}".encode()).decode()
    return f"Basic {encoded}"


def _make_ado_request(
    url: str,
    pat: str,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Perform an authenticated HTTP request against the Azure DevOps REST API.

    Args:
        url: The full API endpoint URL.
        pat: Personal Access Token for authentication.
        method: HTTP method (GET or POST).
        body: Optional JSON body for POST requests.

    Returns:
        Parsed JSON response as a dictionary.

    Raises:
        urllib.error.HTTPError: On non-2xx HTTP responses.
        urllib.error.URLError: On network/connection errors.
        ValueError: If the response body cannot be parsed as JSON.
    """
    headers = {
        "Authorization": _build_auth_header(pat),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _extract_display_name(field_value: Any) -> str:
    """Extract a display name string from an identity-reference field."""
    if isinstance(field_value, dict):
        return field_value.get("displayName", "")
    if isinstance(field_value, str):
        return field_value
    return ""


def _parse_work_item(raw_item: dict[str, Any]) -> dict[str, Any]:
    """
    Convert a raw Azure DevOps work-item API object into a clean dict.

    Args:
        raw_item: Raw work item object from the ADO REST API.

    Returns:
        Cleaned dictionary with the most relevant fields.
    """
    fields = raw_item.get("fields", {})

    parent_id: int | None = None
    child_ids: list[int] = []
    related_items: list[dict[str, Any]] = []

    for rel in raw_item.get("relations", []):
        rel_type = rel.get("rel", "")
        url = rel.get("url", "")
        try:
            rel_id = int(url.rstrip("/").split("/")[-1])
        except (ValueError, IndexError):
            continue

        if rel_type == "System.LinkTypes.Hierarchy-Reverse":
            parent_id = rel_id
        elif rel_type == "System.LinkTypes.Hierarchy-Forward":
            child_ids.append(rel_id)
        else:
            related_items.append({"type": rel_type, "id": rel_id})

    return {
        "id": raw_item.get("id"),
        "url": raw_item.get("url", ""),
        "title": fields.get("System.Title", ""),
        "type": fields.get("System.WorkItemType", ""),
        "state": fields.get("System.State", ""),
        "description": fields.get("System.Description") or "",
        "acceptance_criteria": fields.get("Microsoft.VSTS.Common.AcceptanceCriteria") or "",
        "assigned_to": _extract_display_name(fields.get("System.AssignedTo")),
        "created_by": _extract_display_name(fields.get("System.CreatedBy")),
        "priority": fields.get("Microsoft.VSTS.Common.Priority"),
        "story_points": fields.get("Microsoft.VSTS.Scheduling.StoryPoints"),
        "effort": fields.get("Microsoft.VSTS.Scheduling.Effort"),
        "remaining_work": fields.get("Microsoft.VSTS.Scheduling.RemainingWork"),
        "tags": fields.get("System.Tags") or "",
        "area_path": fields.get("System.AreaPath", ""),
        "iteration_path": fields.get("System.IterationPath", ""),
        "changed_date": fields.get("System.ChangedDate", ""),
        "parent_id": parent_id,
        "child_ids": child_ids,
        "related_items": related_items,
    }


def _fetch_work_items_by_ids(
    org_url: str,
    project: str,
    pat: str,
    ids: list[int],
) -> list[dict[str, Any]]:
    """
    Batch-fetch work items by their IDs, including all relations.

    Args:
        org_url: Azure DevOps organization URL (e.g. https://dev.azure.com/myorg).
        project: Project name.
        pat: Personal Access Token.
        ids: List of work item IDs.

    Returns:
        List of parsed work item dicts.
    """
    ids_param = ",".join(str(i) for i in ids)
    url = (
        f"{org_url.rstrip('/')}/{project}/_apis/wit/workitems"
        f"?ids={ids_param}&$expand=all&api-version={_ADO_API_VERSION}"
    )
    data = _make_ado_request(url, pat)
    return [_parse_work_item(item) for item in data.get("value", [])]


# =============================================================================
# MCP Tools
# =============================================================================

@mcp.tool()
def fetch_ado_work_item(
    organization_url: str,
    project: str,
    personal_access_token: str,
    work_item_id: int,
) -> GlyphMCPResponse[dict]:
    """
    Fetch a single Azure DevOps work item by its ID.

    Retrieves the full detail of a work item (PBI, Task, Bug, Feature, Epic,
    etc.) including its description, acceptance criteria, relations, and
    scheduling fields.

    The Personal Access Token must have at least **Work Items (Read)** scope
    for the target organization.

    Args:
        organization_url: Azure DevOps organization URL.
                          Example: "https://dev.azure.com/my-org"
        project: The name (or ID) of the Azure DevOps project.
                 Example: "MyProject"
        personal_access_token: A Personal Access Token (PAT) with
                               Work Items read permission.
        work_item_id: Numeric ID of the work item to fetch.

    Returns:
        GlyphMCPResponse whose `result` field contains a dict with:
          - id, url, title, type, state
          - description, acceptance_criteria
          - assigned_to, created_by
          - priority, story_points, effort, remaining_work
          - tags, area_path, iteration_path, changed_date
          - parent_id, child_ids, related_items
    """
    response = GlyphMCPResponse[dict]()
    try:
        url = (
            f"{organization_url.rstrip('/')}/{project}/_apis/wit/workitems"
            f"/{work_item_id}?$expand=all&api-version={_ADO_API_VERSION}"
        )
        raw = _make_ado_request(url, personal_access_token)
        response.result = _parse_work_item(raw)
        response.success = True
        response.add_context(
            f"Successfully fetched work item #{work_item_id}: "
            f"[{response.result['type']}] {response.result['title']}"
        )
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()
        except Exception:
            pass
        response.add_context(
            f"Azure DevOps API error {e.code} for work item #{work_item_id}: "
            f"{e.reason}. {body}"
        )
    except urllib.error.URLError as e:
        response.add_context(
            f"Failed to connect to Azure DevOps at '{organization_url}': {e.reason}"
        )
    except Exception as e:
        response.add_context(f"Unexpected error fetching work item #{work_item_id}: {e}")
    return response


@mcp.tool()
def query_ado_work_items(
    organization_url: str,
    project: str,
    personal_access_token: str,
    wiql: str,
    max_results: int = 50,
) -> GlyphMCPResponse[list]:
    """
    Query Azure DevOps work items using a WIQL (Work Item Query Language) statement.

    The query is executed against the given project, and the matching work items
    are returned with their full details (same fields as `fetch_ado_work_item`).

    The Personal Access Token must have at least **Work Items (Read)** scope
    for the target organization.

    ## Example WIQL queries

    All active PBIs in the current sprint:
    ```sql
    SELECT [System.Id] FROM WorkItems
    WHERE [System.TeamProject] = @project
      AND [System.WorkItemType] = 'Product Backlog Item'
      AND [System.State] NOT IN ('Closed', 'Removed')
      AND [System.IterationPath] = @currentIteration('[MyTeam]\\MyProject')
    ORDER BY [Microsoft.VSTS.Common.Priority] ASC
    ```

    All open tasks assigned to a specific user:
    ```sql
    SELECT [System.Id] FROM WorkItems
    WHERE [System.TeamProject] = @project
      AND [System.WorkItemType] = 'Task'
      AND [System.State] NOT IN ('Done', 'Closed')
      AND [System.AssignedTo] = 'John Smith <john@example.com>'
    ORDER BY [System.ChangedDate] DESC
    ```

    Args:
        organization_url: Azure DevOps organization URL.
                          Example: "https://dev.azure.com/my-org"
        project: The name (or ID) of the Azure DevOps project.
                 Example: "MyProject"
        personal_access_token: A Personal Access Token (PAT) with
                               Work Items read permission.
        wiql: A valid WIQL SELECT statement. The SELECT clause need only
              contain `[System.Id]`; all other fields are fetched automatically.
        max_results: Maximum number of work items to return (default 50, max 200).

    Returns:
        GlyphMCPResponse whose `result` field is a list of dicts, each
        containing the same fields as `fetch_ado_work_item`.
    """
    response = GlyphMCPResponse[list]()
    max_results = max(1, min(max_results, 200))

    try:
        # Step 1: execute the WIQL to get matching IDs
        wiql_url = (
            f"{organization_url.rstrip('/')}/{project}"
            f"/_apis/wit/wiql?api-version={_ADO_API_VERSION}"
        )
        wiql_response = _make_ado_request(
            wiql_url,
            personal_access_token,
            method="POST",
            body={"query": wiql},
        )

        work_item_refs = wiql_response.get("workItems", [])
        ids = [ref["id"] for ref in work_item_refs[:max_results]]

        if not ids:
            response.success = True
            response.result = []
            response.add_context("Query returned no work items.")
            return response

        # Step 2: batch-fetch full work item details
        response.result = _fetch_work_items_by_ids(
            organization_url, project, personal_access_token, ids
        )
        response.success = True
        response.add_context(
            f"Query returned {len(response.result)} work item(s) "
            f"(limited to {max_results})."
        )

    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()
        except Exception:
            pass
        response.add_context(
            f"Azure DevOps API error {e.code}: {e.reason}. {body}"
        )
    except urllib.error.URLError as e:
        response.add_context(
            f"Failed to connect to Azure DevOps at '{organization_url}': {e.reason}"
        )
    except Exception as e:
        response.add_context(f"Unexpected error querying work items: {e}")

    return response
