provider "aws" {
  region = "us-east-1"
}

# S3 Bucket para almacenar el dataset
resource "aws_s3_bucket" "dataset_bucket" {
  bucket = "company-dataset-bucket"
  acl    = "private"
}

# DynamoDB Table: FireDamageRecords
resource "aws_dynamodb_table" "fire_damage_records" {
  name           = "FireDamageRecords"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "OBJECTID"

  attribute {
    name = "OBJECTID"
    type = "N"
  }
}

# DynamoDB Table: PredictionResults
resource "aws_dynamodb_table" "prediction_results" {
  name           = "PredictionResults"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "PredictionID"

  attribute {
    name = "PredictionID"
    type = "S"
  }
}
