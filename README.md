<div align="center">
 <img alt="iME" height="300px" src="assets/ime_logo.png">
</div>

# iME Wiki Project

Get up and config the server to run the iME Wiki.


# Quickstart

## 1. Import <server_config> project (Local)
    - Open terminal on your local machine.
    - Run this command to clone the <server_config> poject from the GitHub repository:

      ```
      git clone https://github.com/Ramin-Hashemi/server_config.git
      ```

## 2. Create & add your public SSH key.
    - If you don’t already have an SSH key, open a new terminal on your local machine and run the following command. Otherwise, skip this step, and move directly to copy your public SSH key:
      (Make sure to replace <username@email.com> with your actual email.)

      ```
      ssh-keygen -t ed25519 -C "username@email.com"
      ```
     - Then, copy your public SSH key by using this command and copying the output:
      ```
      cat ~/.ssh/id_ed25519.pub
      ```
      Then paste your public SSH key in 'secret.py' file in the local project repsitory and push to the GitHub.

## 3. Import 'server_config' project (Remote Server)
    - Open terminal on remote server.
    - Change directory to </home>
    - Run this command to clone the <server_config> poject from the GitHub repository:

      ```
      git clone https://github.com/Ramin-Hashemi/server_config.git
      ```

## 4. Configure the remote server
  ### 4.1. Run configurations script
    - Change directory to </home/server_config/>
    - Run this command to execute the required server configurations shell commands:

      ```
      sudo python3 server_config.py run
      ```

### Enjoy!


## Helps:


