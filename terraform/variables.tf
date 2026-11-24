variable "aws_region" {
  type    = string
  default = "ap-southeast-2"
}

variable "project_name" {
  type    = string
  default = "workforcehub"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "public_key_path" {
  type    = string
  default = "~/.ssh/devops-task-key.pub"
}