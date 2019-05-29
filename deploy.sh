#/bin/bash

aws s3 ls

cd terraform
terraform init
terraform plan -out=plan
terraform apply plan
rm plan