import unittest
from unittest.mock import patch, MagicMock
import os
from github_project_manager.project_manager import GitHubProjectManager


class TestGitHubProjectManager(unittest.TestCase):
    def setUp(self):
        # Set environment variables for testing
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_ORG"] = "test_org"

        # Create patcher for the API client
        self.api_patcher = patch(
            "github_project_manager.project_manager.GitHubAPIClient"
        )
        self.mock_api_class = self.api_patcher.start()
        self.mock_api = MagicMock()
        self.mock_api_class.return_value = self.mock_api

        # Initialize the project manager
        self.manager = GitHubProjectManager()

        # Set the project_id for testing
        self.manager.project_id = "test_project_id"
        self.manager.project_name = "Test Project"

    def tearDown(self):
        self.api_patcher.stop()

    def test_create_issue_with_add_to_project(self):
        """Test creating an issue with add_to_project=True"""
        # Mock API responses
        self.mock_api.rest_request.side_effect = [
            # First call - check if issue exists
            [],
            # Second call - create issue
            {"node_id": "test_issue_id", "title": "Test Issue"},
        ]

        # Mock GraphQL query for adding to project
        project_items_response = {"node": {"items": {"nodes": []}}}
        self.mock_api.graphql_query.side_effect = [
            project_items_response,  # First call - check if already in project
            {
                "addProjectV2ItemById": {"item": {"id": "new_item_id"}}
            },  # Second call - add to project
        ]

        # Test creating a new issue with add_to_project=True
        result = self.manager.create_issue(
            "test-repo", "Test Issue", "Test description", add_to_project=True
        )

        # Verify issue was created
        self.assertEqual(result, "test_issue_id")

        # Verify issue was added to project
        self.assertEqual(self.mock_api.graphql_query.call_count, 2)

        # Check second call (the mutation)
        mutation_call = self.mock_api.graphql_query.call_args_list[1]
        self.assertIn("addProjectV2ItemById", mutation_call[0][0])

        # Verify the variables were passed correctly
        variables = mutation_call[0][1]
        self.assertEqual(variables["projectId"], "test_project_id")
        self.assertEqual(variables["contentId"], "test_issue_id")

    def test_create_issue_update_description(self):
        """Test updating an issue's description when it changes"""
        # Mock API responses
        existing_issue = {
            "node_id": "test_issue_id",
            "title": "Test Issue",
            "body": "Old description",
            "number": 42,
        }

        self.mock_api.rest_request.side_effect = [
            # First call - check if issue exists
            [existing_issue],
            # Second call - update issue (add this mock response)
            {"node_id": "test_issue_id", "body": "New description"},
        ]

        # Test updating an existing issue's description
        result = self.manager.create_issue("test-repo", "Test Issue", "New description")

        # Verify correct issue ID is returned
        self.assertEqual(result, "test_issue_id")

        # Verify description was updated
        self.assertEqual(self.mock_api.rest_request.call_count, 2)
        patch_call_args = self.mock_api.rest_request.call_args_list[1]
        self.assertEqual(patch_call_args[0][0], "PATCH")
        self.assertEqual(patch_call_args[0][1], "/repos/test_org/test-repo/issues/42")
        self.assertEqual(patch_call_args[0][2], {"body": "New description"})

    def test_add_issue_to_project_already_exists(self):
        """Test adding an issue that's already in the project"""
        # Mock API responses for checking project items
        project_items_response = {
            "node": {
                "items": {
                    "nodes": [
                        {"content": {"id": "issue_1"}},
                        {"content": {"id": "test_issue_id"}},
                    ]
                }
            }
        }

        self.mock_api.graphql_query.return_value = project_items_response

        # Try to add an issue that's already in the project
        self.manager.add_issue_to_project("test_issue_id")

        # Verify the API wasn't called to add the issue
        self.assertEqual(self.mock_api.graphql_query.call_count, 1)

    def test_add_issue_to_project_new_issue(self):
        """Test adding an issue that's not already in the project"""
        # Mock API responses for checking project items
        project_items_response = {
            "node": {"items": {"nodes": [{"content": {"id": "issue_1"}}]}}
        }

        # First call returns existing items, second call is the mutation
        self.mock_api.graphql_query.side_effect = [
            project_items_response,
            {"addProjectV2ItemById": {"item": {"id": "new_item_id"}}},
        ]

        # Add a new issue to the project
        self.manager.add_issue_to_project("test_issue_id")

        # Verify the API was called to add the issue
        self.assertEqual(self.mock_api.graphql_query.call_count, 2)
        mutation_call = self.mock_api.graphql_query.call_args_list[1]

        # Check that a mutation with addProjectV2ItemById was called
        self.assertIn("addProjectV2ItemById", mutation_call[0][0])

        # Verify the variables were passed correctly
        variables = mutation_call[0][1]
        self.assertEqual(variables["projectId"], "test_project_id")
        self.assertEqual(variables["contentId"], "test_issue_id")


if __name__ == "__main__":
    unittest.main()
