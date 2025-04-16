"""Issue tools implementation for the PyGithub MCP Server.

This module implements MCP tools for GitHub issues, including creation, listing,
updating, comments, and labels.
"""

import json
import logging
import traceback
from typing import List, Callable

from mcp.server.fastmcp import FastMCP

from pygithub_mcp_server.client import GitHubClient
from pygithub_mcp_server.schemas.issues import (
    ListIssuesParams,
    CreateIssueParams,
    GetIssueParams,
    UpdateIssueParams,
    IssueCommentParams,
    ListIssueCommentsParams,
    UpdateIssueCommentParams,
    DeleteIssueCommentParams,
    AddIssueLabelsParams,
    RemoveIssueLabelParams,
)
from pygithub_mcp_server.errors import GitHubError, format_github_error
from pygithub_mcp_server.operations import issues
from pygithub_mcp_server.tools import tool

# Get logger
logger = logging.getLogger(__name__)

@tool()
def create_issue(params_dict: dict) -> dict:
    """Create a new issue in a GitHub repository.
    
    Args:
        params_dict: Parameters for creating an issue including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - title: Issue title
            - body: Issue description (optional)
            - assignees: List of usernames to assign
            - labels: List of labels to add
            - milestone: Milestone number (optional)
    
    Returns:
        Created issue details from GitHub API
    """
    try:
        # First validate the input params
        try:
            params = CreateIssueParams(**params_dict)
            logger.debug(f"create_issue called with validated params: {params}")
        except Exception as e:
            logger.error(f"Failed to convert dict to CreateIssueParams: {e}")
            return {
                "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
                "is_error": True
            }

        # Pass the Pydantic model directly to the operation
        result = issues.create_issue(params)
        logger.debug(f"Got result: {result}")
        response = {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        logger.debug(f"Returning response: {response}")
        return response
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }

@tool()
def list_issues(params: ListIssuesParams) -> dict:
    """List issues from a GitHub repository.
    
    Args:
        params: Parameters for listing issues including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - state: Issue state (open, closed, all)
            - labels: Filter by labels
            - sort: Sort field (created, updated, comments)
            - direction: Sort direction (asc, desc)
            - since: Filter by date
            - page: Page number for pagination
            - per_page: Number of results per page (max 100)
    
    Returns:
        List of issues from GitHub API
    """
    try:
        logger.debug(f"list_issues called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.list_issues(params)
        logger.debug(f"Got result: {result}")
        response = {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        logger.debug(f"Returning response: {response}")
        return response
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def get_issue(params: GetIssueParams) -> dict:
    """Get details about a specific issue.
    
    Args:
        params: Parameters for getting an issue including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number to retrieve
    
    Returns:
        Issue details from GitHub API
    """
    try:
        logger.debug(f"get_issue called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.get_issue(params)
        logger.debug(f"Got result: {result}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def update_issue(params: UpdateIssueParams) -> dict:
    """Update an existing issue.
    
    Args:
        params: Parameters for updating an issue including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number to update
            - title: New title (optional)
            - body: New description (optional)
            - state: New state (optional)
            - labels: New labels (optional)
            - assignees: New assignees (optional)
            - milestone: New milestone number (optional)
    
    Returns:
        Updated issue details from GitHub API
    """
    try:
        logger.debug(f"update_issue called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.update_issue(params)
        logger.debug(f"Got result: {result}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def add_issue_comment(params: IssueCommentParams) -> dict:
    """Add a comment to an issue.
    
    Args:
        params: Parameters for adding a comment including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number to comment on
            - body: Comment text
    
    Returns:
        Created comment details from GitHub API
    """
    try:
        logger.debug(f"add_issue_comment called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.add_issue_comment(params)
        logger.debug(f"Got result: {result}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def list_issue_comments(params: ListIssueCommentsParams) -> dict:
    """List comments on an issue.
    
    Args:
        params: Parameters for listing comments including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number
            - since: Filter by date (optional)
            - page: Page number (optional)
            - per_page: Results per page (optional)
    
    Returns:
        List of comments from GitHub API
    """
    try:
        logger.debug(f"list_issue_comments called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.list_issue_comments(params)
        logger.debug(f"Got result: {result}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def update_issue_comment(params: UpdateIssueCommentParams) -> dict:
    """Update an issue comment.
    
    Args:
        params: Parameters for updating a comment including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number containing the comment
            - comment_id: Comment ID to update
            - body: New comment text
    
    Returns:
        Updated comment details from GitHub API
    """
    try:
        logger.debug(f"update_issue_comment called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.update_issue_comment(params)
        logger.debug(f"Got result: {result}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def delete_issue_comment(params: DeleteIssueCommentParams) -> dict:
    """Delete an issue comment.
    
    Args:
        params: Parameters for deleting a comment including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number containing the comment
            - comment_id: Comment ID to delete
    
    Returns:
        Empty response on success
    """
    try:
        logger.debug(f"delete_issue_comment called with params: {params}")
        # Pass the Pydantic model directly to the operation
        issues.delete_issue_comment(params)
        logger.debug("Comment deleted successfully")
        return {"content": [{"type": "text", "text": "Comment deleted successfully"}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def add_issue_labels(params: AddIssueLabelsParams) -> dict:
    """Add labels to an issue.
    
    Args:
        params: Parameters for adding labels including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number
            - labels: Labels to add
    
    Returns:
        Updated list of labels from GitHub API
    """
    try:
        logger.debug(f"add_issue_labels called with params: {params}")
        # Pass the Pydantic model directly to the operation
        result = issues.add_issue_labels(params)
        logger.debug(f"Got result: {result}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }


@tool()
def remove_issue_label(params: RemoveIssueLabelParams) -> dict:
    """Remove a label from an issue.
    
    Args:
        params: Parameters for removing a label including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - issue_number: Issue number
            - label: Label to remove
    
    Returns:
        Empty response on success or error if label doesn't exist
    """
    try:
        logger.debug(f"remove_issue_label called with params: {params}")
        
        # First check if the issue exists and has the label
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        
        # Get current labels
        label_names = [label.name for label in issue.labels]
        
        if params.label not in label_names:
            # Label doesn't exist on this issue, return an error
            error_msg = f"Label '{params.label}' does not exist on issue #{params.issue_number}"
            logger.warning(error_msg)
            return {
                "content": [{"type": "error", "text": error_msg}],
                "is_error": True
            }
        
        # Now try to remove the label
        issues.remove_issue_label(params)
        logger.debug("Label removed successfully")
        return {"content": [{"type": "text", "text": "Label removed successfully"}]}
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }

def register(mcp: FastMCP) -> None:
    """Register all issue tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
    """
    from pygithub_mcp_server.tools import register_tools
    
    # List of all issue tools to register
    issue_tools = [
        create_issue,
        list_issues,
        get_issue,
        update_issue,
        add_issue_comment,
        list_issue_comments,
        update_issue_comment,
        delete_issue_comment,
        add_issue_labels,
        remove_issue_label,
    ]
    
    register_tools(mcp, issue_tools)
    logger.debug(f"Registered {len(issue_tools)} issue tools")
