output "server_public_ip" {
  value = aws_eip.web.public_ip
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "ssh_command" {
  value = "ssh -i ~/.ssh/devops-task-key ec2-user@${aws_eip.web.public_ip}"
}