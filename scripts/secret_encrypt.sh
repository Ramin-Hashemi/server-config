#!/bin/bash

# Encrypt the Secrets

echo "ime-server-admin" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > user.txt
echo "ime-app-group" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > group_name.txt
echo "/.ssh" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > ssh_key_path.txt
echo "********" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > public_ssh_key.txt
echo "185.213.165.171" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > ip_address.txt

# Database
# mysql
echo "ime_app_mysql_db" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > mysql_database_name.txt
echo "ime-app-db-admin" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > mysql_database_username.txt
echo "123456789" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > mysql_database_password.txt
# postgres
echo "ime_app_postgre_db" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > postgres_database_name.txt
echo "ime-app-db-admin" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > postgres_database_username.txt
echo "123456789" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > postgres_database_password.txt

# GitHub
echo "Ramin-Hashemi" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > github_username.txt
echo "ghp_********" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > github_pat.txt

echo "github.com/CognitiveLearn-Innovations/apache-server.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_1.txt
echo "github.com/CognitiveLearn-Innovations/nginx-server.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_2.txt
echo "github.com/CognitiveLearn-Innovations/backend-api.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_3.txt
echo "github.com/CognitiveLearn-Innovations/home-domain.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_4.txt
echo "github.com/CognitiveLearn-Innovations/dashboard.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_5.txt
echo "github.com/CognitiveLearn-Innovations/blog.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_6.txt
echo "github.com/CognitiveLearn-Innovations/solutions.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_7.txt
echo "github.com/CognitiveLearn-Innovations/ime-agent.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_8.txt
echo "github.com/CognitiveLearn-Innovations/wiki.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_9.txt
echo "github.com/CognitiveLearn-Innovations/ime-nft.git" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > repo_url_10.txt

# Docker Hub Credentials
echo "raminhashemi" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > name_real.txt
echo "ramin.hashemi@usa.com" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > name_email.txt

echo "docker" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > group_name_docker.txt
echo "kubernetes.local" | openssl enc -aes-256-cbc -md sha512 -a -pbkdf2 -iter 100000 -salt -pass pass:encryption_key > hostname.txt