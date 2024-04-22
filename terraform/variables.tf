variable "region" {
  type = string
}

variable "team" {
  default = "martian"
}

variable "service" {
  default = "leaderboard"
}

variable "env" {
  type = string
}

// VPC
variable "vpc_cidr_block" {
  description = "CIDR block to use as address space for the VPC"
  type        = string
}

locals {
  default_tags = {
    Terraform   = "true"
    Team        = var.team
    Service     = var.service
    Environment = var.env
  }
}
