<div align="center"h1>
 <img alt="iME" height="300px" src="assets/ime_logo.png"</h1>
</div>

# iME Server Config Project

Get up and config the server to run the iME projects.

# Quick Start

## 1. Import `server-config` Project (Remote Server)

- Open terminal on remote server.
- Change directory to `./home`
- Run this command to clone the `server-config` poject from the GitHub repository:

```text
git clone https://github.com/Ramin-Hashemi/server-config.git
```

## 2. Add Required Fields in `secret_script.sh` File

### 2.1. Create & Add Your <PUBLIC_SSH_KEY>

- If you don't already have an SSH key, open a new terminal on your local machine and run the following command. Otherwise, skip this step, and move directly to copy your public SSH key:  
  (Make sure to replace <username@email.com> with your actual email.)

  ```text
  ssh-keygen -t ed25519 -C "username@email.com"
  ```

- Then copy your public SSH key by using this command and copying the output:

  ```text
  cat ~/.ssh/id_ed25519.pub
  ```

- Change directory to `./home/server_config/`
- Run this command to open the `secret_script.sh` file:

```text
sudo nano secret_script.sh
```

- Then paste your <PUBLIC_SSH_KEY> in `secret_script.sh` file.

### 2.2. Add Your <GITHUB_PAT>

- Copy GitHup Personal Access Token (classic) from your GitHub profile.
- Paste your <GITHUB_PAT> in the `secret_script.sh` file.
- Then save and exit.

## 3. Change the script files permissions to make them executable.

- Run this command:

```text
chmod +x secret_script.sh config.sh run_script.sh server_monitoring_script.sh backup_script.sh
```

Execute files:

- Run this command to execute the `secret_script.sh` file encription shell commands:

```text
./secret_script.sh
```

- Run this command to execute the `run_script.sh` file server configurations shell commands:

```text
bash -i ./run_script.sh run
```

## 5. Edit the Crontab

- Run this command to open the crontab editor:

```text
crontab -e
```

- Add the Cron Job:
Run the following commands to schedule the script to run daily at 2 AM and log the output:

```text
0 2 * * * /home/server-config/server_monitoring_script.sh >> /home/ime-server-admin/server_monitoring.log 2>&1
```

```text
0 3 * * * /home/server-config/server_backup_script.sh >> /home/ime-server-admin/backup.log 2>&1
```

### Enjoy

## Bash Scripts Best Practices

Following best practices can help you create a robust and maintainable script.

1. Structure Your Script
Modularize: Break down your script into functions. Each function should perform a single task.
Validate User Input: Always validate user input to ensure that your scripts can handle unexpected or malicious input gracefully. Use conditional statements and error handling to catch and respond to invalid input.
Comments: Use comments to explain what each part of the script does. This makes it easier to understand and maintain.
Error Handling: Implement error handling to manage unexpected issues gracefully.
2. Use Configuration Files
Store configuration variables in a separate file. This makes it easier to update configurations without modifying the script.
3. Logging
Implement logging to track the script’s execution. This helps in debugging and monitoring.
4. Environment Checks
Check for necessary dependencies and environment variables at the beginning of the script.
5. Security
Avoid hardcoding sensitive information like passwords. Use environment variables or secure vaults.
Validate inputs to prevent injection attacks.
6. Testing
Test your script in a staging environment before deploying it to production.

## Helps

- A Bash scripting template incorporating best practices & several useful functions.
  <https://github.com/ralish/bash-script-template>

- Setting up Django with Nginx, Gunicorn, virtualenv, supervisor and PostgreSQL.
  <https://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/>

## UML Diagram

!UML Diagram

# Final server directory structure

/home/nginx-server/
├── bin                          <= Directory created by virtualenv
│   ├── activate                 <= Environment activation script
│   ├── django-admin.py
│   ├── gunicorn
│   ├── gunicorn_django
│   ├── gunicorn_start           <= Script to start application with Gunicorn
│   └── python
├── ime-app-django               <= Django project directory, add this to PYTHONPATH
│   ├── manage.py
│   ├── project_application_1
│   ├── project_application_2
│   └── ime-app-settings                    <= Project settings directory
│       ├── __init__.py
│       ├── settings.py          <= ime-app.settings - settings module Gunicorn will use
│       ├── urls.py
│       └── wsgi.py              <= hello.wsgi - WSGI module Gunicorn will use
├── include
│   └── python3.12 -> /usr/include/python3.12
├── lib
│   └── python2.7
├── lib64 -> /web-apps/ime-app/lib
├── logs                         <= Application logs directory
│   ├── gunicorn_supervisor.log
│   ├── nginx-access.log
│   └── nginx-error.log
├── media                        <= User uploaded files folder
├── run
│   └── gunicorn.sock 
└── static                       <= Collect and serve static files from here





Here’s an enhanced and more modern version of the README file, complete with examples for each point:

# Project

## NameTable of Contents

- Project Overview
- Getting Started
- File Naming Conventions
- Coding Standards
- Branching Strategy
- Commit Message Guidelines
- Pull Request Process
- Issue Tracking
- Contribution Guidelines
- License
- Contact

# Project Overview

Welcome to Project Name! This project aims to [brief description of the project’s purpose and key features]. For example, "This project aims to provide a seamless user experience for managing personal finances through an intuitive web application."

# Getting Started

## Prerequisites

Ensure you have the following software installed:

- Python 3.9+
- Docker
- Node.js

## Installation

Follow these steps to set up the project locally:

```text
# Clone the repository
git clone https://github.com/yourusername/yourproject.git

# Navigate to the project directory
cd yourproject

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

# File Naming Conventions

To maintain consistency, follow these naming conventions:

- Python files: Use snake_case (e.g., data_processor.py).
- Configuration files: Use hyphens (e.g., docker-compose.yml).
- Directories: Use lowercase and hyphens (e.g., data-files).

## Examples:

- Python file: data_processor.py
- Configuration file: docker-compose.yml
- Directory: data-files

# Coding Standards

## Python

- Follow PEP 8 guidelines.
- Use type hints for function signatures.
- Write docstrings for all public modules, classes, and functions.

### Example:

```text
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers and return the result.

    :param a: First number
    :param b: Second number
    :return: Sum of a and b
    """
    return a + b
```

## JavaScript

- Follow Airbnb JavaScript Style Guide.
- Use ES6+ features.
- Write JSDoc comments for functions and classes.

### Example:

```text
/**
 * Add two numbers and return the result.
 * @param {number} a - First number
 * @param {number} b - Second number
 * @return {number} Sum of a and b
 */
const addNumbers = (a, b) => a + b;
```

## HTML/CSS

- Use semantic HTML5 elements.
- Follow BEM methodology for CSS.

### Example:

```text
<!-- HTML -->
<article class="card card--featured">
  <h1 class="card__title">Title</h1>
  <p class="card__description">Description</p>
</article>

<!-- CSS -->
.card {
  /* styles */
}
.card--featured {
  /* styles */
}
.card__title {
  /* styles */
}
.card__description {
  /* styles */
}
```

# Branching Strategy

- main: Production-ready code.
- develop: Latest development changes.
- feature/xyz: New features.
- bugfix/xyz: Bug fixes.
- hotfix/xyz: Critical fixes in production.

## Example:

```text
# Create a new feature branch
git checkout -b feature/add-user-authentication
```

# Commit Message Guidelines

- Use the Conventional Commits format.

## Example:

```text
feat: add user authentication
fix: resolve issue with data fetching
docs: update README with setup instructions
```

# Pull Request Process

- Ensure your code follows the coding standards.
- Write tests for new features or bug fixes.
- Update documentation if necessary.
- Create a pull request against the develop branch.
- Request a review from at least one team member.

## Example:

```text
# Push your branch to the remote repository
git push origin feature/add-user-authentication

# Create a pull request on GitHub
```

# Issue Tracking

```text
- Use GitHub Issues to report bugs, request features, or ask questions.
- Follow the issue templates provided.
Example:
Title: Bug: Unable to login with valid credentials

Description:
Steps to reproduce:
1. Go to the login page
2. Enter valid credentials
3. Click on the login button
4. See error

Expected behavior:
User should be logged in successfully.
```

# Contribution Guidelines

- Fork the repository and create your branch from develop.
- Ensure your code passes all tests.
- Follow the commit message guidelines.
- Submit a pull request for review.

## Example:

```text
# Fork the repository
# Clone your fork
git clone https://github.com/yourusername/yourproject.git

# Create a new branch
git checkout -b feature/add-user-authentication

# Make your changes and commit them
git commit -m "feat: add user authentication"

# Push your branch to your fork
git push origin feature/add-user-authentication

# Open a pull request on GitHub
```

# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Contact

For any questions or support, please contact:

- Project Lead: Your Name
- Slack Channel: #project-name
