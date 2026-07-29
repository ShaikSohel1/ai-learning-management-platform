# Contributing to AI LMS

First off, thank you for considering contributing to the **AI Learning Management Platform**! We welcome contributions from developers of all skill levels, whether you are fixing a bug, adding a feature, or improving documentation.

---

## 🛠️ Getting Started

### 1. Fork and Clone
1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/[YOUR-USERNAME]/ai-learning-management-platform.git
   ```

### 2. Branching Strategy
We follow the [Conventional Commits](https://www.conventionalcommits.org/) and standard Git Flow strategies.
- **`main`**: The stable production branch.
- **`feat/your-feature`**: For new features (e.g., `feat/add-gemini-vision`).
- **`fix/issue-name`**: For bug fixes (e.g., `fix/auth-token-refresh`).
- **`docs/update-readme`**: For documentation updates.

### 3. Setup Your Environment
Please refer to the [Deployment Guide](../DEPLOYMENT.md) for full instructions on setting up the React Frontend, FastAPI Backend, and connecting to Supabase.

---

## 💻 Coding Standards

### Backend (Python/FastAPI)
- **Type Hinting**: All Python code MUST use strict type hints.
- **Linting & Formatting**: We use `black` for formatting and `flake8` for linting.
  ```bash
  black app/
  flake8 app/
  ```
- **Asynchronous Code**: Use `async`/`await` for all IO-bound operations (Database queries, API calls).
- **Testing**: Write unit tests for new features using `pytest`.

### Frontend (React/Vite)
- **Components**: Use Functional Components and React Hooks exclusively. No Class Components.
- **Styling**: Use TailwindCSS utility classes. Avoid creating custom CSS files unless strictly necessary for animations.
- **Prop Types / TypeScript**: Although the current stack is JS/JSX, ensure explicit validations where necessary using Context and sensible defaults.

---

## 🚀 Submitting a Pull Request (PR)

1. **Commit your changes**:
   Write clear, concise commit messages.
   ```bash
   git commit -m "feat(ai): integrate gemini 2.0 flash for agent reasoning"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feat/your-feature
   ```
3. **Open a PR**:
   - Navigate to the main repository.
   - Click "New Pull Request".
   - Fill out the PR template completely. Link any related issues (e.g., `Closes #42`).
   - Include screenshots if your changes affect the UI!

---

## 🐞 Reporting Bugs

If you find a bug, please create an issue on GitHub. Include:
- A clear descriptive title.
- Steps to reproduce the bug.
- Expected vs. actual behavior.
- Screenshots or console logs.

---

## 📜 Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. We are dedicated to providing a welcoming, inclusive, and harassment-free experience for everyone.
