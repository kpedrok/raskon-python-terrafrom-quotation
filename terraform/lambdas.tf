locals {
  variables = {
    RULES_TABLE = "${aws_dynamodb_table.rules.name}"
  }
}

module "lambda_raskon_quotation" {
  source        = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path          = "../quotation/"
  handler       = "quotation-final.lambda_handler"
  function_name = "raskon-quotation-coverage"
  runtime       = "python3.7"
  timeout       = "15"
  memory_size   = "512"

  variables = "${local.variables}"

  extra_policy_statements = [<<EOF
  {
    "Effect": "Allow",
    "Action": "dynamodb:*",
    "Resource": "*"
  }
  EOF
  ]
}

module "lambda_raskon_input_rule" {
  source        = "github.com/fernandoruaro/serverless.tf//lambda/api_gateway"
  path          = "../api/"
  handler       = "input_rule.lambda_handler"
  function_name = "${local.prefix_dash}input-rules"
  runtime       = "python3.7"
  timeout       = "5"
  memory_size   = "320"

  variables = "${local.variables}"

  extra_policy_statements = [<<EOF
  {
    "Effect": "Allow",
    "Action": "dynamodb:*",
    "Resource": "*"
  }
  EOF
  ]
}
