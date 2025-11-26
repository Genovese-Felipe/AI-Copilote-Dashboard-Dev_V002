# Contributing to AI Copilot Dashboard

Thank you for your interest in contributing to this project!

## Branch Protection

This repository uses branch protection on the `main` branch to ensure code quality and prevent accidental changes. The following protections are recommended:

### Recommended Branch Protection Rules

1. **Require pull request reviews before merging** - All changes must be reviewed
2. **Require status checks to pass before merging** - CI checks must pass
3. **Do not allow force pushes** - Prevents history rewriting
4. **Do not allow deletions** - Prevents accidental branch deletion

### Setting Up Branch Protection (For Repository Administrators)

1. Go to **Settings** → **Branches** in the repository
2. Click **Add branch protection rule**
3. Set branch name pattern to `main`
4. Enable the desired protection options

## Pull Request Process

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Ensure all CI checks pass
5. Submit a pull request to `main`
6. Wait for review and approval

## CI Checks

This repository runs the following checks on all pull requests:

- HTML file validation
- Python syntax checking

All checks must pass before a pull request can be merged.
