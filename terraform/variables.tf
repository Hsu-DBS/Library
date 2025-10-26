variable "key_name" {
  default = "terraform-ec2-key"  # AWS key pair name
}

variable "public_key_path" {
  default = "~/.ssh/id_rsa.pub"  # local public key
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}
