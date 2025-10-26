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
  ami                         = "ami-0c7114fa3eac14de1"   # Latest ARM64 Ubuntu
  instance_type               = "t4g.micro"              # Free Tier eligible
  key_name                    = "terraform-ec2-key"
  vpc_security_group_ids      = [aws_security_group.terraform_web_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "My First EC2 Instance"
  }
}


