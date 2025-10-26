# Security Group for SSH and HTTP access
resource "aws_security_group" "terraform_web_sg" {
  name = "terraform-web-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH from anywhere
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow HTTP from anywhere
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outbound
  }
}

# EC2 instance
resource "aws_instance" "example" {
  ami                         = "ami-0fb0b230890ccd1e6"
  instance_type               = "t2.micro"
  key_name                    = "terraform-ec2-key"
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "My First EC2 Instance"
  }
}

