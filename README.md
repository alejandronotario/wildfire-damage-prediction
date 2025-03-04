# wildfire-damage-prediction

This project demonstrates an end-to-end MLOps architecture for predicting wildfire damage, integrating data ingestion, data contract validation, model training and deployment, a RESTful API backend, infrastructure provisioning with Terraform, and CI/CD automation with GitHub Actions.

## Project Components

1. **Data Ingestion & Storage**
   - **Dataset**: A `.geojson` file containing wildfire damage data, stored in an S3 bucket.
   - **Ingestion Scripts**:
     - `scripts/ingest_data.py`: Downloads the geojson file from S3 and loads the records into the DynamoDB table `FireDamageRecords`.
     - `scripts/synthetic_ingest.py`: Simulates periodic ingestion of new records (using synthetic data or dataset partitioning) to demonstrate real-time ingestion.
   - **Storage**:
     - DynamoDB table **FireDamageRecords** to store the dataset records.
     - DynamoDB table **PredictionResults** to store model prediction results along with execution timestamps.

2. **Data Contracts**
   - A data contract is defined in `data_contract/data_contract.yaml` using the style and tool from [datacontract/datacontract-cli](https://github.com/datacontract/datacontract-cli).
   - This contract ensures that the dataset meets the expected schema.
   - Data contract validation is integrated into the CI/CD pipeline using GitHub Actions.

3. **Model Training & Deployment**
   - The pre-trained wildfire damage prediction model is extracted from a notebook and modularized (e.g., in `src/training/train.py`).
   - Periodic re-training is scheduled with Apache Airflow, with experiments tracked and versioned using MLflow.
   - The model is deployed as an inference endpoint on Amazon SageMaker.

4. **Backend API**
   - A RESTful API is implemented using FastAPI (located at `src/api/main.py`) to expose prediction results and common MLOps functionalities.
   - The API backend is containerized using Docker for ease of deployment.

5. **Infrastructure as Code (IaC)**
   - Terraform scripts (in `terraform/main.tf`) are used to provision AWS resources such as the S3 bucket, DynamoDB tables, SageMaker endpoints, etc.

6. **CI/CD and Data Contract Validation**
   - GitHub Actions automatically runs tests (using pytest) and validates the data contract using the DataContract CLI on every push or pull request.
   - Test results and validation logs are stored in a `logs/` folder for review.

## Repository Structure

project-root/ ├── .github/ │ └── workflows/ │ └── ci-cd.yml # CI/CD workflow (pytest and data contract validation) ├── configs/ │ └── aws_config.json # (Optional) AWS configuration (region, etc.) ├── data_contract/ │ └── data_contract.yaml # Expected schema definition for the dataset ├── docker/ │ ├── Dockerfile # Dockerfile for the ingestion and/or backend service │ └── docker-compose.yml # (Optional) To run local services ├── notebooks/ │ └── exploration.ipynb # Notebooks for development and exploration ├── scripts/ │ ├── create_tables.py # Script to create DynamoDB tables │ ├── ingest_data.py # Script for ingesting data from S3 into DynamoDB │ └── synthetic_ingest.py # Script to simulate periodic ingestion of data ├── src/ │ ├── api/ │ │ └── main.py # FastAPI backend for predictions and MLOps functionalities │ ├── inference/ # Code for model inference on SageMaker (adapted) │ └── training/ # Scripts for model training and re-training ├── terraform/ │ └── main.tf # Terraform code for provisioning AWS resources ├── tests/ │ └── test_data_contract.py # Pytest tests to validate the data contract ├── requirements.txt # Project dependencies └── README.md # This file

## Installation & Deployment

### Prerequisites
- An AWS account with permissions to create resources (S3, DynamoDB, SageMaker, etc.)
- Python 3.8+ and pip
- Terraform installed
- Docker and Docker Compose (optional for local deployment)

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Install Dependencies**

   ```bash
    pip install -r requirements.txt
   ```
3. **Provision Infrastructure with Terraform**

   ```bash
   cd terraform
   terraform init
   terraform apply
   ```
4. **Data Ingestion**

- Upload your .geojson file to the configured S3 bucket.
- Run the ingestion script:

   ```bash
   python scripts/ingest_data.py
   ```
5. **Simulate Real-Time Ingestion**

   ```bash
   python scripts/synthetic_ingest.py
   ```
6. **Run Tests & Data Contract Validation**

   ```bash
   pytest
   ```
7. **Run the Backend API**
  
   Build and run the docker container
   
   ```bash
   docker build -t fire-damage-api -f docker/Dockerfile .
   docker run -p 8000:8000 fire-damage-api
   ```
   
   Alternatively, use Docker Compose:
   ```bash
   docker-compose -f docker/docker-compose.yml up
   ```




