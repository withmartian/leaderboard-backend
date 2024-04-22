terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.0.0"
    }
  }

  backend "s3" {

  }
}

provider "aws" {
  region = var.region
}

# terraform init -reconfigure -upgrade -backend-config=env/backend-dev.conf
# terraform plan -var-file=env/dev.tfvars
# terraform apply -var-file=env/dev.tfvars
