resource "aws_api_gateway_rest_api" "api" {
  name        = "${local.prefix_dash}api"
  description = "Cotação de Transportadoras"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id       = "${aws_api_gateway_rest_api.api.id}"
  stage_name        = "prod"
  stage_description = "${md5(file("api.tf"))}"             #Forçar atualização do stage
}

module "raskon_quotation" {
  source      = "github.com/fernandoruaro/serverless.tf//api_gateway/resource"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  path_part   = "quote"
}

module "raskon_quotation_GET" {
  source              = "github.com/fernandoruaro/serverless.tf//api_gateway/method/lambda"
  rest_api_id         = "${aws_api_gateway_rest_api.api.id}"
  resource_id         = "${module.raskon_quotation.id}"
  http_request_method = "GET"
  lambda_invoke_arn   = "${module.lambda_raskon_quotation.lambda_invoke_arn}"
}

module "raskon_input_rule" {
  source      = "github.com/fernandoruaro/serverless.tf//api_gateway/resource"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  path_part   = "input_rule"
}

module "raskon_input_rule_ANY" {
  source              = "github.com/fernandoruaro/serverless.tf//api_gateway/method/lambda"
  rest_api_id         = "${aws_api_gateway_rest_api.api.id}"
  resource_id         = "${module.raskon_input_rule.id}"
  http_request_method = "ANY"
  lambda_invoke_arn   = "${module.lambda_raskon_input_rule.lambda_invoke_arn}"
}
