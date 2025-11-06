# Book Tracking System – Automated Cloud Deployment

This project demonstrates the automated deployment of a **Book Tracking System** web application on **Amazon Web Services (AWS)** using **Terraform**, **Ansible**, **Docker**, and **GitHub Actions**.  
The system allows users to record and manage their reading progress while showcasing a complete **DevOps automation workflow**.

---

## Overview

This project integrates modern DevOps tools to automate infrastructure provisioning, configuration management, containerization, and continuous deployment.

| Tool | Purpose |
|------|----------|
| **Terraform** | Infrastructure as Code (IaC) for provisioning AWS EC2, VPC, and networking. |
| **Ansible** | Configuration management — installs Docker and prepares the server environment. |
| **Docker** | Packages and runs the FastAPI Book Tracking application. |
| **GitHub Actions** | Automates CI/CD to build, push, and deploy containers. |
| **AWS EC2** | Cloud platform hosting the deployed application. |

---

## Project Structure

book-tracking-system/
├── app/
│   ├── app.py                # FastAPI app entry
│   ├── templates/            # HTML templates
│   ├── requirements.txt      # Dependencies
│   └── Dockerfile            # Docker configuration
│
├── terraform/                # AWS infrastructure setup
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── provider.tf
│
├── ansible/                  # Configuration management
│   ├── playbooks/setup-docker.yml
│   └── inventory.ini
│
├── .github/workflows/        # CI/CD workflow
│   └── deploy.yml
│
└── README.md

---

## Terraform – Infrastructure Setup

Provision AWS resources:
cd terraform
terraform init
terraform plan -out plan.tfplan
terraform apply "plan.tfplan"

After execution, Terraform outputs the EC2 public IP.  
Note: An Elastic IP was later assigned for stable hosting.

---

## Ansible – Server Configuration

Configure the EC2 instance and install Docker:
ansible -i inventory.ini all -m ping
ansible-playbook -i inventory.ini playbooks/setup-docker.yml

Ensures Docker is installed, enabled, and ready for deployment.

---

## Docker – Application Deployment

Create and run the Docker container on the **cloud server (AWS EC2)**:

Build the Docker image:
docker build -t fastapi-app .

Run the container on the cloud server:
docker run -d -p 8000:8000 --name fastapi-container fastapi-app

Access the running application in the browser: http://50.16.26.60:8000/

The FastAPI application is running inside a Docker container on the EC2 instance, served using Uvicorn.

---

## GitHub Actions – CI/CD Automation

GitHub Actions automates deployment whenever code is pushed to the main branch.

Workflow Steps:
1. Builds Docker image from the latest code.
2. Pushes image to Docker Hub.
3. SSHs into EC2 instance.
4. Pulls and redeploys the updated container.

Required Secrets:
DOCKER_USERNAME  
DOCKER_PASSWORD  
SSH_PRIVATE_KEY  
SSH_USER  
SERVER_IP  
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

---

## Accessing the Application

After deployment, open browser:  http://50.16.26.60:8000/

Will see the Book Tracking homepage.

---

## Author

Name: Hsu Myint Myat Kyaw
Program: MSc Information Systems with Computing
Module Title: Network Systems and Administration CA 2025
Module Code: B9IS121
Assessment Title: Automated Container deployment and Administration in the cloud
Project: Automated Cloud Deployment – Book Tracking System  
Technologies: FastAPI, Terraform, Ansible, Docker, GitHub Actions, AWS 

---

## 🏁 Conclusion

This project demonstrates how **Infrastructure as Code (Terraform)**, **Configuration Management (Ansible)**, **Containerization (Docker)**, and **CI/CD Automation (GitHub Actions)** can work together to create a reliable, scalable, and fully automated cloud deployment pipeline.
