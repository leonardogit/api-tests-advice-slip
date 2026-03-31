# API Tests - Advice Slip

API test automation project for the [Advice Slip API](https://api.adviceslip.com) using **Cucumber + RestAssured + Spring Boot**.

## Tech Stack

- Java 17
- Spring Boot 3.2.5
- Cucumber 7.15.0 (BDD)
- RestAssured 5.4.0
- JUnit Platform
- Maven

## Running Tests

```bash
mvn clean test
```

### Environment Selection

Set the `ENVIRONMENT` variable to choose between `dev` and `hom`:

```bash
ENVIRONMENT=hom mvn clean test
```

Default is `dev`.

---

## QA PR Reviewer (GPT-4)

This project includes an automated **QA Specialist & PR Reviewer** powered by OpenAI GPT-4. It runs on every pull request and posts a detailed QA analysis as a PR comment.

### What It Does

When a pull request is opened or updated, the reviewer automatically:

1. **Fetches the PR diff** from GitHub
2. **Analyzes the changes** using GPT-4, acting as a senior QA specialist
3. **Posts a comment** on the PR with:
   - Summary of changes
   - Affected areas of the codebase
   - Risk assessment
   - Recommended test cases (with type and priority)
   - Recommended test types (unit, integration, e2e, etc.)
   - Suggestions for improvement

### Setup

#### 1. Add the OpenAI API Key as a GitHub Secret

1. Go to your repository on GitHub
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Name: `OPENAI_API_KEY`
5. Value: your OpenAI API key
6. Click **Add secret**

> The `GITHUB_TOKEN` is provided automatically by GitHub Actions — no extra setup needed.

#### 2. That's it!

The GitHub Actions workflow (`.github/workflows/qa-review.yml`) triggers automatically on every PR. No further configuration is required.

### Running Locally

You can also run the QA reviewer script locally against any PR:

```bash
pip install -r scripts/requirements.txt

export OPENAI_API_KEY="your-openai-api-key"
export GITHUB_TOKEN="your-github-token"
export GITHUB_REPOSITORY="leonardogit/api-tests-advice-slip"
export PR_NUMBER="1"

python scripts/qa_reviewer.py
```

### Architecture

```
scripts/
  qa_reviewer.py        # Main QA analysis script
  requirements.txt      # Python dependencies (openai, requests)

.github/workflows/
  qa-review.yml         # GitHub Actions workflow triggered on PRs
```

### Configuration

| Environment Variable | Description | Required |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes (GitHub Secret) |
| `GITHUB_TOKEN` | GitHub token for API access | Yes (auto-provided by Actions) |
| `GITHUB_REPOSITORY` | Repository in `owner/repo` format | Yes (auto-provided by Actions) |
| `PR_NUMBER` | Pull request number to analyze | Yes (auto-provided by Actions) |
