"""
Azure DevOps integration test scenarios.

These scenarios exercise the ADO tool helpers using offline/mock data so that
no real Azure DevOps credentials are required.  They also demonstrate graceful
error handling when the API is unreachable.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.azure_devops import (
    _parse_work_item,
    _extract_display_name,
    fetch_ado_work_item,
    query_ado_work_items,
)
from test_runner.scenarios.base import BaseScenario


# ---------------------------------------------------------------------------
# Minimal fake ADO API responses used across scenarios
# ---------------------------------------------------------------------------

_FAKE_PBI = {
    "id": 42,
    "url": "https://dev.azure.com/myorg/myproject/_apis/wit/workItems/42",
    "fields": {
        "System.Id": 42,
        "System.Title": "Implement Azure DevOps integration",
        "System.WorkItemType": "Product Backlog Item",
        "System.State": "Active",
        "System.Description": "<p>As a developer, I want Glyph to fetch ADO work items.</p>",
        "Microsoft.VSTS.Common.AcceptanceCriteria": "<p>Given credentials are valid, items are returned.</p>",
        "System.AssignedTo": {"displayName": "Jane Dev", "uniqueName": "jane@example.com"},
        "System.CreatedBy": {"displayName": "John PM"},
        "Microsoft.VSTS.Common.Priority": 2,
        "Microsoft.VSTS.Scheduling.StoryPoints": 5.0,
        "Microsoft.VSTS.Scheduling.Effort": None,
        "Microsoft.VSTS.Scheduling.RemainingWork": None,
        "System.Tags": "ado; integration",
        "System.AreaPath": "MyProject\\Backend",
        "System.IterationPath": "MyProject\\Sprint 3",
        "System.ChangedDate": "2024-06-01T12:00:00Z",
    },
    "relations": [
        {
            "rel": "System.LinkTypes.Hierarchy-Reverse",
            "url": "https://dev.azure.com/myorg/myproject/_apis/wit/workItems/10",
        },
        {
            "rel": "System.LinkTypes.Hierarchy-Forward",
            "url": "https://dev.azure.com/myorg/myproject/_apis/wit/workItems/43",
        },
        {
            "rel": "System.LinkTypes.Hierarchy-Forward",
            "url": "https://dev.azure.com/myorg/myproject/_apis/wit/workItems/44",
        },
        {
            "rel": "System.LinkTypes.Related",
            "url": "https://dev.azure.com/myorg/myproject/_apis/wit/workItems/99",
        },
    ],
}

_FAKE_TASK = {
    "id": 43,
    "url": "https://dev.azure.com/myorg/myproject/_apis/wit/workItems/43",
    "fields": {
        "System.Id": 43,
        "System.Title": "Write unit tests for ADO tool",
        "System.WorkItemType": "Task",
        "System.State": "New",
        "System.Description": None,
        "Microsoft.VSTS.Common.AcceptanceCriteria": None,
        "System.AssignedTo": "Jane Dev <jane@example.com>",
        "System.CreatedBy": {"displayName": "Jane Dev"},
        "Microsoft.VSTS.Common.Priority": 1,
        "Microsoft.VSTS.Scheduling.StoryPoints": None,
        "Microsoft.VSTS.Scheduling.Effort": 3.0,
        "Microsoft.VSTS.Scheduling.RemainingWork": 2.0,
        "System.Tags": "",
        "System.AreaPath": "MyProject\\Backend",
        "System.IterationPath": "MyProject\\Sprint 3",
        "System.ChangedDate": "2024-06-02T09:00:00Z",
    },
    "relations": [],
}


class ParseWorkItemScenario(BaseScenario):
    """Scenario 30: Parse raw ADO work-item API response (offline)."""

    def run(self):
        self.print_header(
            30,
            "Parse ADO Work Item - Offline",
            "Converts a raw ADO API response dict into a clean Glyph dict.",
        )

        print("\nInput: fake PBI API response (no network call)")
        result = _parse_work_item(_FAKE_PBI)
        self.print_result("Parsed PBI", str(result))

        # Basic assertions
        assert result["id"] == 42, "ID mismatch"
        assert result["type"] == "Product Backlog Item", "Type mismatch"
        assert result["assigned_to"] == "Jane Dev", "AssignedTo mismatch"
        assert result["parent_id"] == 10, "Parent ID mismatch"
        assert result["child_ids"] == [43, 44], "Child IDs mismatch"
        assert result["related_items"] == [{"type": "System.LinkTypes.Related", "id": 99}]
        print("\n✓ All assertions passed.")

        print("\nInput: fake Task API response (no network call)")
        result_task = _parse_work_item(_FAKE_TASK)
        self.print_result("Parsed Task", str(result_task))

        assert result_task["id"] == 43
        assert result_task["type"] == "Task"
        assert result_task["description"] == ""   # None converted to ""
        assert result_task["child_ids"] == []
        assert result_task["parent_id"] is None
        # String AssignedTo field
        assert result_task["assigned_to"] == "Jane Dev <jane@example.com>"
        print("✓ All assertions passed.")


class ExtractDisplayNameScenario(BaseScenario):
    """Scenario 31: _extract_display_name helper (offline)."""

    def run(self):
        self.print_header(
            31,
            "Extract Display Name Helper - Offline",
            "Tests the identity-field extraction helper with various input shapes.",
        )

        cases = [
            ({"displayName": "Alice", "uniqueName": "alice@example.com"}, "Alice"),
            ("Bob <bob@example.com>", "Bob <bob@example.com>"),
            (None, ""),
            ({}, ""),
            (123, ""),
        ]

        for value, expected in cases:
            actual = _extract_display_name(value)
            status = "✓" if actual == expected else "✗"
            print(f"  {status} Input: {value!r:45s}  → {actual!r}  (expected {expected!r})")
            assert actual == expected, f"Mismatch for input {value!r}: got {actual!r}"

        print("\n✓ All display-name cases passed.")


class FetchAdoWorkItemInvalidCredentialsScenario(BaseScenario):
    """Scenario 32: fetch_ado_work_item with invalid credentials returns error gracefully."""

    def run(self):
        self.print_header(
            32,
            "Fetch ADO Work Item - Invalid Credentials",
            "Demonstrates graceful failure when the PAT or URL is wrong.",
        )

        print("\nCalling: fetch_ado_work_item with a non-existent org URL")
        response = fetch_ado_work_item(
            organization_url="https://dev.azure.com/nonexistent-org-12345",
            project="FakeProject",
            personal_access_token="fake-pat",
            work_item_id=1,
        )
        self.print_result("Response", str(response.model_dump()))

        assert not response.success, "Expected failure, got success"
        assert len(response.context) > 0, "Expected at least one context message"
        print("\n✓ Tool failed gracefully with an error context message.")


class QueryAdoWorkItemsInvalidCredentialsScenario(BaseScenario):
    """Scenario 33: query_ado_work_items with invalid credentials returns error gracefully."""

    def run(self):
        self.print_header(
            33,
            "Query ADO Work Items - Invalid Credentials",
            "Demonstrates graceful failure when the PAT or URL is wrong.",
        )

        wiql = (
            "SELECT [System.Id] FROM WorkItems "
            "WHERE [System.TeamProject] = @project "
            "AND [System.WorkItemType] = 'Product Backlog Item' "
            "AND [System.State] != 'Closed' "
            "ORDER BY [System.ChangedDate] DESC"
        )

        print("\nCalling: query_ado_work_items with a non-existent org URL")
        response = query_ado_work_items(
            organization_url="https://dev.azure.com/nonexistent-org-12345",
            project="FakeProject",
            personal_access_token="fake-pat",
            wiql=wiql,
        )
        self.print_result("Response", str(response.model_dump()))

        assert not response.success, "Expected failure, got success"
        assert len(response.context) > 0, "Expected at least one context message"
        print("\n✓ Tool failed gracefully with an error context message.")
