# Jira MCP Server

A Model Context Protocol (MCP) server for Jira integration. This server provides tools for interacting with Jira, including creating, reading, and updating issues.

## Features

- **Issue Management**: Create, read, update, and transition issues
- **Search**: Use JQL to search for issues
- **Comments**: Add comments to issues
- **Resources**: Access metadata about projects, issue types, and priorities
- **Prompts**: Templates for common Jira workflows

## Installation

```bash
pip install -e .
```

## Configuration

Set the following environment variables:

```bash
export JIRA_BASE_URL="https://your-instance.atlassian.net"
export JIRA_USERNAME="your_email@example.com"
export JIRA_API_TOKEN="your_api_token"
```

You can get an API token from: https://id.atlassian.com/manage-profile/security/api-tokens

## Usage

Start the server:

```bash
mcp-jira
```

## Available Tools

- **get_issue**: Get details of a specific Jira issue
- **search_issues**: Search for Jira issues using JQL
- **create_issue**: Create a new Jira issue
- **update_issue**: Update an existing Jira issue
- **add_comment**: Add a comment to a Jira issue
- **transition_issue**: Change the status of a Jira issue

## Available Resources

- **jira://projects**: List of all Jira projects
- **jira://issuetypes**: List of all issue types
- **jira://priorities**: List of all priorities

## Available Prompts

- **create_bug**: Template for creating a bug report
- **jql_search**: Template for creating JQL search queries

## Version

0.0.1
