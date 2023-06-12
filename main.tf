provider "aws" {
  region = "us-west-2"
}

resource "aws_lambda_function" "comic_app" {
  function_name    = "comic-app"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "app.handler"
  runtime          = "python3.9"
  timeout          = 30
  memory_size      = 128

  filename         = "deployment.zip"
  source_code_hash = filebase64sha256("deployment.zip")
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "comic-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id               = aws_apigatewayv2_api.api_gateway.id
  integration_type     = "AWS_PROXY"
  integration_uri      = aws_lambda_function.comic_app.invoke_arn
  integration_method   = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "$default"

  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "$default"
  auto_deploy = true
}

output "api_gateway_url" {
  value = aws_apigatewayv2_api.api_gateway.api_endpoint
}
