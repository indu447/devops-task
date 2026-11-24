# WorkforceHub: CI/CD, IaC and Container Registry

A small Flask app deployed to AWS with Terraform and a GitHub Actions pipeline.

## Architecture

GitHub push -> GitHub Actions (Test, Build and push, Deploy, Health check) -> AWS ECR (private registry) -> EC2 server running Nginx (port 80) and the Flask app (port 5000).

## Repository layout

- `app/` Flask application
- `tests/` pytest tests
- `Dockerfile` multi-stage build, runs as non-root user `appuser`, exposes port 5000
- `nginx/nginx.conf` reverse proxy, port 80 to the app
- `docker-compose.yml` local run (builds the image)
- `docker-compose.prod.yml` server run (pulls the image from ECR)
- `terraform/` ECR repository, EC2 instance, security group, IAM role, Elastic IP
- `.github/workflows/deploy.yml` the pipeline

## Endpoints

- `GET /` welcome message
- `GET /health` returns 200 with `{"status":"ok"}`
- `GET /api/employees` list employees
- `POST /api/employees` add an employee (JSON: name, role)

## Run locally

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
docker compose up -d --build
curl http://localhost/health
```

## Infrastructure (Terraform)

All cloud resources are created by Terraform. The only manual step is creating the IAM user and access key that Terraform and the pipeline use.

```
cd terraform
terraform init
terraform apply
terraform output
```

## Pipeline stages

Triggered only on pushes to `main` (and manually via workflow_dispatch).

1. **Test**: pytest with a coverage report, uploaded as an artifact.
2. **Build and push**: builds the Docker image, tags it with the commit SHA, pushes it to ECR, and archives the image digest as an artifact.
3. **Deploy**: copies the compose and Nginx files to the server over SSH, logs in to ECR from the server, pulls the image and restarts the containers.
4. **Health check**: uses curl to confirm `/health` returns 200.

Required GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `EC2_HOST`, `EC2_SSH_KEY`.

## Rollback strategy

Every image is tagged with the Git commit SHA, so earlier versions stay in ECR.

**Option 1, via Git (preferred):** revert the bad commit and push. The pipeline redeploys the previous code.

```
git revert <bad-commit-sha>
git push
```

**Option 2, on the server (fastest):** point the server at an older image tag.

```
ssh -i ~/.ssh/devops-task-key ec2-user@<server-ip>
cd ~/app
echo 'IMAGE=<ecr-repo-url>:<old-commit-sha>' > .env
docker compose up -d
```

## Clean up

```
cd terraform
terraform destroy
```
