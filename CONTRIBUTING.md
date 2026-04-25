# Contributing to AESTHETICS MISSION Analytics Dashboard

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Be kind, constructive, and professional in all interactions.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/aesthetics-mission-analytics.git
   cd aesthetics-mission-analytics
   ```
3. **Add upstream** remote:
   ```bash
   git remote add upstream https://github.com/OopsSOLVED/aesthetics-mission-analytics.git
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Making Changes

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes with clear, descriptive commits:
   ```bash
   git commit -m "feat: add new visualization for lead conversion funnel"
   ```

3. Keep your branch up to date:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix   | Description                    |
|----------|--------------------------------|
| `feat:`  | New feature                    |
| `fix:`   | Bug fix                        |
| `docs:`  | Documentation changes          |
| `style:` | CSS/formatting changes         |
| `refactor:` | Code refactoring            |
| `test:`  | Adding or fixing tests         |
| `chore:` | Maintenance tasks              |

## Pull Request Process

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request against the `main` branch

3. In the PR description, include:
   - **What** the change does
   - **Why** the change is needed
   - **Screenshots** for any UI changes
   - **Testing** steps you followed

4. Wait for a review and address any feedback

## Style Guide

### Python
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions
- Use type hints where applicable
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines where possible

### CSS
- Use CSS custom properties (variables) defined in the root
- Follow the existing naming conventions (`.metric-card`, `.section-header`, etc.)
- Use the established gradient variables for consistency

### Streamlit Components
- Use `st.markdown()` with `unsafe_allow_html=True` for custom HTML
- Apply the `plotly_theme()` helper to all Plotly charts
- Use `format_inr()` for all currency formatting

## Reporting Bugs

Open a GitHub Issue with:
- **Title**: Clear, concise description
- **Environment**: OS, Python version, browser
- **Steps to Reproduce**: Numbered steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable

## Feature Requests

Open a GitHub Issue with the label `enhancement` and include:
- **Problem**: What problem does this solve?
- **Solution**: Your proposed solution
- **Alternatives**: Other approaches you considered
- **Priority**: How important is this to you?

---

Thank you for contributing to AESTHETICS MISSION! 🏠✨
