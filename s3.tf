
#S3 bucket for image upload being connected to lambda function
resource "aws_s3_bucket" "s3bucket_detect_faces" {
  bucket = "s3bucket-detect-faces"

  tags = {
    Name        = "s3bucket-detect-faces"
    Environment = "Lab"
  }
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.s3bucket_detect_faces.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambdafunction_image_rekognition.arn
    events              = ["s3:ObjectCreated:*"]
  }
}