#creating zip file required to input lambda funtion

data "archive_file" "pylambda_script_file" {
  type        = "zip"
  source_file = "${path.module}/py_scripts/${var.lambda_function_name}.py"
  output_path = "${path.module}/lambda-funtion.zip"
}

# lambda function
resource "aws_lambda_function" "lambdafunction_image_rekognition" {
  filename      = data.archive_file.pylambda_script_file.output_path
  function_name = var.lambda_function_name

  role          = aws_iam_role.lambda_assume_role.arn
  handler       = "${var.lambda_function_name}.lambda_handler"

  source_code_hash = filebase64sha256(data.archive_file.pylambda_script_file.output_path)

  runtime = "python3.8"
  timeout = 6

  environment {
    variables = {
      "METADATA_TABLE" = aws_dynamodb_table.lambda_image_rekognition.name
    }
  }

}