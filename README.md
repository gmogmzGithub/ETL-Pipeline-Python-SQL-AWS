# ETL-Pipeline-Python-SQL-AWS
A Python-based data engineering project demonstrating an ETL (Extract, Transform, Load) pipeline. The project extracts data from REST APIs and text files, processes it through transformations, and stores the results in MongoDB, PostgreSQL, MySQL, and AWS S3. Designed to showcase data engineering skills and integration with modern data technologies such as Docker, MongoDB, and AWS.

## Project Overview
This project simulates a full ETL pipeline where:
- **Extraction**: Data is pulled from external sources like text files and REST APIs.
- **Transformation**: The extracted data is cleaned and transformed (e.g., calculating profit margins, converting fields to uppercase).
- **Loading**: The transformed data is loaded into different storage systems like MongoDB and AWS S3.

The project demonstrates how to manage multiple data sources, transform the data, and store it efficiently using cloud and database technologies.

## Technologies Used
- **Python**: Core programming language for the ETL pipeline.
- **Django**: Web framework used for creating REST APIs and managing the project.
- **Django REST Framework (DRF)**: For building the REST API.
- **MongoDB**: NoSQL database for storing transformed data, running inside Docker.
- **PostgreSQL & MySQL**: Relational databases for data storage (expandable based on future project needs).
- **AWS S3**: Cloud storage for uploading transformed data as CSV files.
- **Docker**: Used to run MongoDB in a containerized environment.
- **Boto3**: AWS SDK for Python to interact with S3.
- **pymongo**: MongoDB client for Python.

## Project Features
- **Data Extraction**: Extracts data from text files (e.g., `CoffeeChain.txt`) and REST APIs.
- **Data Transformation**: Data is cleaned and transformed (e.g., converting fields to uppercase, calculating new fields like profit margins).
- **Data Loading**:
  - Inserts the transformed data into MongoDB.
  - Saves the data as a CSV and uploads it to AWS S3.
- **API Endpoints**:
  - **GET /data/extract**: Extracts, transforms, and uploads data to MongoDB and AWS S3.
  - **POST /data/transform**: Accepts input, applies transformations, and returns the result.

## High-Level Design Diagram
```
+-------------------------------+                     
|         API Layer (Views)      |                     
|-------------------------------|                     
| - Defines API endpoints        |                     
| - Accepts requests             |                     
| - Validates data using         |                     
|   serializers (e.g., DRF)      |                     
| - Delegates logic to services  |                     
|                               |
| Example:                      |
|   - GET /data/extract          |
|   - POST /data/transform       |
+-------------------------------+
                |
                v
+-------------------------------+
|         Service Layer          |                     
|-------------------------------|                     
| - Core business logic          |
| - Implements ETL functionality |
| - Calls utilities for REST API |
|   and AWS interaction          |
|                               |
| Subcomponents:                 |
|  1. ExtractionService          |
|     - Fetch data from external |
|       sources (REST API, DB)   |
|  2. TransformationService      |
|     - Clean, transform, and    |
|       validate data            |
|  3. LoadingService             |
|     - Save data to databases   |
|       or upload to AWS S3      |
+-------------------------------+
                |
                v
+----------------------------------+     +-----------------------------------+
|      Data Access Layer (ORM)     |     |        Utility Layer              |
|----------------------------------|     |-----------------------------------|
| - Interacts with PostgreSQL,     |     | - Provides reusable utilities     |
|   MySQL, etc. using Django ORM   |     |   for external services           |
| - Defines models and performs    |     | - Handles HTTP requests to REST   |
|   CRUD operations                |     |   APIs using requests library     |
|                                  |     | - Uploads/downloads files to/from |
| Example:                         |     |   AWS S3 using Boto3              |
|   - Models: DataRecord, TransLog |     |                                   |
|   - Queries: .filter(), .all(),  |     | Example:                          |
|     .save()                      |     |  - REST API fetch (requests.get)  |
|                                  |     |  - S3 upload (s3.upload_file)     |
+----------------------------------+     +-----------------------------------+
```

## How to Run the Project

### Prerequisites
- **Python 3.10+**
- **Docker** (for running MongoDB)
- **AWS Account** with an S3 bucket (for storing CSV files)
- **Postman** or any API testing tool (to interact with the REST API)

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ETL-Pipeline-Python-SQL-AWS.git
   cd ETL-Pipeline-Python-SQL-AWS
   ```

2. **Install Dependencies**:
   Set up a virtual environment and install the required Python packages:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start MongoDB in Docker**:
   Run the MongoDB container using Docker:
   ```bash
   docker run --name mongodb -d -p 27017:27017 mongo
   ```

4. **Configure AWS**:
   Ensure you have the AWS CLI configured with your credentials:
   ```bash
   aws configure
   ```

5. **Run the Project**:
   ```bash
   python manage.py runserver
   ```

6. **Test the API**:
   - Use the GET endpoint to extract, transform, and load data:
     ```
     GET /api/extract
     ```
   - Use the POST endpoint to transform input data:
     ```
     POST /api/transform
     Body: {"name": "John", "age": 30}
     ```

### Example of Running the Pipeline:
1. **Extract and Transform Data** from `CoffeeChain.txt`.
2. **Save Transformed Data** to MongoDB and CSV file.
3. **Upload CSV to AWS S3**.

## Contributing
Feel free to fork the repository and submit pull requests. If you'd like to make improvements or add more features, your contributions are welcome!

## License
This project is licensed under the MIT License.

---

### Next Steps:
- Add more transformations and extract data from various sources (APIs, databases).
- Explore integrating with more advanced data processing tools (e.g., Apache Spark, Kafka).
