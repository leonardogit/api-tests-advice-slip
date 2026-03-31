#!/usr/bin/env python3
"""
QA Specialist & PR Reviewer

This script integrates with GitHub to review pull request diffs and uses
OpenAI GPT-4 to generate QA analysis including:
- Potential test cases to be created
- Types of tests recommended (unit, integration, e2e, etc.)
- Code areas most affected by the changes

Usage:
    python qa_reviewer.py

Environment variables required:
    OPENAI_API_KEY  - OpenAI API key for GPT-4
    GITHUB_TOKEN    - GitHub token for API access
    GITHUB_REPOSITORY - Repository in owner/repo format
    PR_NUMBER       - Pull request number to analyze
"""

import os
import sys
import textwrap
from typing import Optional

import openai
import requests


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENAI_MODEL = "gpt-4"
MAX_DIFF_CHARS = 12000  # Truncate very large diffs to stay within token limits

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a senior QA specialist and code reviewer. Your job is to analyze
    pull request diffs and produce a comprehensive QA analysis written in
    clear, professional English.

    For every PR diff you receive, you MUST produce a report with the
    following sections:

    ## 1. Summary of Changes
    A brief, plain-language description of what the PR changes.

    ## 2. Affected Areas
    List the parts of the codebase most impacted by these changes.
    Mention files, classes, methods, and endpoints where relevant.

    ## 3. Risk Assessment
    Identify the riskiest parts of the change — things most likely to
    introduce bugs or regressions.

    ## 4. Recommended Test Cases
    Provide a numbered list of concrete test cases that should be created
    or updated to cover these changes. Each test case should include:
    - **Title**: short name
    - **Type**: unit / integration / e2e / contract / performance
    - **Description**: what it validates
    - **Priority**: high / medium / low

    ## 5. Recommended Test Types
    Summarize which *categories* of testing are most important for this PR
    and explain why.

    ## 6. Suggestions for Improvement
    Any code-quality, design, or testing suggestions for the PR author.

    Be specific, actionable, and concise. Use markdown formatting.
""")


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------

def get_github_headers(token: str) -> dict:
    """Return authorization headers for the GitHub API."""
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def fetch_pr_diff(repo: str, pr_number: int, token: str) -> str:
    """Fetch the unified diff of a pull request from GitHub."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = get_github_headers(token)
    headers["Accept"] = "application/vnd.github.v3.diff"

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def fetch_pr_metadata(repo: str, pr_number: int, token: str) -> dict:
    """Fetch PR metadata (title, body, changed files, etc.)."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = get_github_headers(token)

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_pr_files(repo: str, pr_number: int, token: str) -> list:
    """Fetch the list of changed files in a pull request."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = get_github_headers(token)

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def post_pr_comment(repo: str, pr_number: int, token: str, body: str) -> None:
    """Post a comment on a pull request."""
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = get_github_headers(token)

    response = requests.post(url, headers=headers, json={"body": body}, timeout=30)
    response.raise_for_status()
    print(f"Comment posted successfully on PR #{pr_number}")


# ---------------------------------------------------------------------------
# OpenAI helpers
# ---------------------------------------------------------------------------

def analyze_diff_with_gpt4(
    diff: str,
    pr_title: str,
    pr_body: Optional[str],
    changed_files: list,
    api_key: str,
) -> str:
    """Send the PR diff to GPT-4 and return the QA analysis."""
    client = openai.OpenAI(api_key=api_key)

    # Build context message
    files_summary = "\n".join(
        f"- `{f['filename']}` ({f['status']}, +{f['additions']}/-{f['deletions']})"
        for f in changed_files
    )

    # Truncate diff if too large
    truncated = False
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS]
        truncated = True

    user_message = f"""\
Pull Request: **{pr_title}**

Description:
{pr_body or '(no description)'}

### Changed Files
{files_summary}

### Diff
```diff
{diff}
```
{"(diff truncated due to size)" if truncated else ""}

Please provide your full QA analysis report.
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=3000,
    )

    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_comment(analysis: str) -> str:
    """Wrap the analysis in a nice PR comment body."""
    return (
        "## :mag: QA Analysis — Automated Review\n\n"
        f"{analysis}\n\n"
        "---\n"
        "*Generated automatically by the QA Reviewer (GPT-4)*"
    )


def main() -> None:
    # Read required environment variables
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number_str = os.environ.get("PR_NUMBER")

    missing = []
    if not openai_api_key:
        missing.append("OPENAI_API_KEY")
    if not github_token:
        missing.append("GITHUB_TOKEN")
    if not repo:
        missing.append("GITHUB_REPOSITORY")
    if not pr_number_str:
        missing.append("PR_NUMBER")

    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    pr_number = int(pr_number_str)

    print(f"Analyzing PR #{pr_number} in {repo}...")

    # 1. Fetch PR data from GitHub
    print("Fetching PR metadata...")
    pr_meta = fetch_pr_metadata(repo, pr_number, github_token)
    pr_title = pr_meta.get("title", "")
    pr_body = pr_meta.get("body", "")

    print("Fetching PR diff...")
    diff = fetch_pr_diff(repo, pr_number, github_token)

    print("Fetching changed files...")
    changed_files = fetch_pr_files(repo, pr_number, github_token)

    print(f"PR '{pr_title}' — {len(changed_files)} file(s) changed")

    # 2. Analyze with GPT-4
    print("Sending diff to GPT-4 for QA analysis...")
    analysis = analyze_diff_with_gpt4(
        diff=diff,
        pr_title=pr_title,
        pr_body=pr_body,
        changed_files=changed_files,
        api_key=openai_api_key,
    )

    # 3. Post comment on the PR
    comment_body = build_comment(analysis)
    print("Posting analysis as PR comment...")
    post_pr_comment(repo, pr_number, github_token, comment_body)

    # 4. Also print the analysis to stdout for CI logs
    print("\n" + "=" * 60)
    print("QA ANALYSIS REPORT")
    print("=" * 60)
    print(analysis)


if __name__ == "__main__":
    main()
