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
## 2. Add Required Fields in `secret.py` File
  ### 2.1. Create & Add Your <PUBLIC_SSH_KEY>
  - If you don’t already have an SSH key, open a new terminal on your local machine and run the following command. Otherwise, skip this step, and move directly to copy your public SSH key:  
  (Make sure to replace <username@email.com> with your actual email.)
  ```
  ssh-keygen -t ed25519 -C "username@email.com"
  ```
  - Then copy your public SSH key by using this command and copying the output:
  ```
  cat ~/.ssh/id_ed25519.pub
  ```
  - Then paste your <PUBLIC_SSH_KEY> in `secret.py` file in the local project repsitory.
  ### 2.2. Add Your <GITHUB_PAT>
  - Copy GitHup Personal Access Token (classic) from your GitHub profile.
  - Paste your <GITHUB_PAT> in the `secret.py` file.
  - Then push the local project repsitory to the GitHub.
## 3. Import `server-config` Project (Remote Server)
- Open terminal on remote server.
- Change directory to `./home`
- Run this command to clone the `server-config` poject from the GitHub repository:
```
git clone https://github.com/Ramin-Hashemi/server-config.git
```
## 4. Configure the Remote Server
  ### 4.1. Run Configurations Script
  - Change directory to `./home/server_config/`
  - Run this command to execute the required server configurations shell commands:
  ```
  sudo python3 server_config.py run
  ```

### Enjoy!


## Helps:


