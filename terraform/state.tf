provider "aws" {
  region = "${var.region}"
}

terraform {
  backend "s3" {
    bucket  = "raskon-terraform"
    key     = "raskon-quotation.tfstate"
    region  = "us-east-1"
    encrypt = "true"
  }
}
