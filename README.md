<div align="center">
 <img alt="iME" height="300px" src="assets/ime_logo.png">
</div>

# iME Server Config Project
Get up and config the server to run the iME projects.

# Quick Start
## 1. Import `server-config` Project (Local)
- Open terminal on your local machine.
- Run this command to clone the `server-config` poject from the GitHub repository:
```
git clone https://github.com/Ramin-Hashemi/server-config.git
```
## 2. Add Required Fields in `secret_script.sh` File
  ### 2.1. Create & Add Your <PUBLIC_SSH_KEY>
  - If you don't already have an SSH key, open a new terminal on your local machine and run the following command. Otherwise, skip this step, and move directly to copy your public SSH key:  
  (Make sure to replace <username@email.com> with your actual email.)
  ```
  ssh-keygen -t ed25519 -C "username@email.com"
  ```
  - Then copy your public SSH key by using this command and copying the output:
  ```
  cat ~/.ssh/id_ed25519.pub
  ```
  - Then paste your <PUBLIC_SSH_KEY> in `secret_script.sh` file in the local project repsitory.
## 3. Import `server-config` Project (Remote Server)
- Open terminal on remote server.
- Change directory to `./home`
- Run this command to clone the `server-config` poject from the GitHub repository:
```
git clone https://github.com/Ramin-Hashemi/server-config.git
```
## 4. Configure the Remote Server
- Change directory to `./home/server_config/`
- Run this command to check for syntax errors:
```
bash -n run_script.sh
```
  ### 4.1. Add Your <GITHUB_PAT>
  - Run this command to open the `secret_script.sh` file:
```
sudo nano secret_script.sh
```
  - Copy GitHup Personal Access Token (classic) from your GitHub profile.
  - Paste your <GITHUB_PAT> in the `secret_script.sh` file.
  - Then save and exit.
Change the script files permissions to make them executable.
- Run this command:
```
chmod +x secret_script.sh config.sh run_script.sh server_monitoring_script.sh backup_script.sh
```
Execute files:
- Run this command to execute the `secret_script.sh` file encription shell commands:
```
./secret_script.sh
```
- Run this command to execute the `run_script.sh` file server configurations shell commands:
```
bash -i ./run_script.sh run
```
## 5. Edit the Crontab
- Run this command to open the crontab editor:
```
crontab -e
```
- Add the Cron Job:
Run the following commands to schedule the script to run daily at 2 AM and log the output:
```
0 2 * * * /home/server-config/server_monitoring_script.sh >> /home/ime-server-admin/server_monitoring.log 2>&1
```
```
0 3 * * * /home/server-config/backup_script.sh >> /home/ime-server-admin/backup.log 2>&1
```
### Enjoy!


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

## Helps:
 Final server directory structure

