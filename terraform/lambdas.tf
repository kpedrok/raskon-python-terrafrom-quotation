module "lambda_raskon_quotation" {
  source        = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path          = "../quotation-final/"
  handler       = "quotation-final.lambda_handler"
  function_name = "raskon-quotation-coverage"
  runtime       = "python3.7"
  timeout       = "15"
  memory_size   = "512"

  #   extra_policy_statements = [<<EOF
  # {
  #   "Effect": "Allow",
  #   "Action": "dynamodb:*",
  #   "Resource": "*"
  # }
  # EOF
  #   ]
}
