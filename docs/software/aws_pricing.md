# AWS Pricing

## RDBMS

### Amazon Aurora

[Amazon Aurora Pricing](https://aws.amazon.com/rds/aurora/pricing/) [Pricing Calculator](https://calculator.aws/#/createCalculator/AuroraMySQL)

Amazon Aurora is a modern relational database service. It offers unparalleled high performance and high availability at global scale with fully open-source MySQL- and PostgreSQL-compatible editions and a range of developer tools for building serverless and machine learning (ML)-driven applications.

1. Instance type:
	1. Aurora Standard
	2. Aurora I/O Optimized
1. Pricing by database instances:
	1. Serverless: auto-scaling, billed per Aurora Capacity Units(ACU) per hour
	2. Provisioned On-Demand: billed per instance hour
	3. Provisioned Reserved: billed per term (1 year or 3 years)
2. Pricing by database storage and I/Os:
	1. Storage: billed per GB per month
	2. I/O: billed per million requests, free if using Aurora I/O-Optimized
3. Aurora Global Database: single Aurora database to span multiple regions
	1. Billing: billed per million replicated write I/Os
4. Backup storage costs: billed per GB per month
5. Backtrack: quickly move to a prior point in time to recover from user errors
	1. Billing: billed per 1 million change records(logs)
6. Data API: execute SQL queries through HTTPS
	1. Billing: billed per 1 million requests
	2. 32 KB metered per request, one 35KB payload accounts for two requests
7. Data transfer costs:
	1. Free transfer from Internet to AWS
	2. Transfer from AWS to Internet billed per GB
	3. Transfer from one AWS region to another billed per GB
8. Extended support: billed per ACU/VCPU per hour
9. Snapshot export to S3: billed per GB
10. Zero-ETL integration with Amazon Redshift: no additional fee

### Amazon Redshift

[Amazon Redshift Pricing](https://aws.amazon.com/redshift/pricing/)

1. On-demand pricing: billed per instance per hour
2. Serverless: billed per RPU(Redshift Processing Unit) per hour
3. Redshift managed storage: billed per GB per month
4. Redshift Spectrum: directly run SQL queries against S3
	1. Pricing: billed per TB of data scanned
5. Concurrency scaling: billed per instance per second
6. Redshift ML: billed per million cells
7. Reserved instance: billed per term (1 year or 3 years)
8. Zero-ETL integration cost with Amazon Aurora: no additional fee
9. Backup storage: billed per GB per month
10. Data transfer: billed per GB

## NoSQL

### Amazon OpenSearch

[Amazon OpenSearch pricing](https://aws.amazon.com/opensearch-service/pricing/)

1. On-demand instance: billed per instance per hour
2. Reserved instance: reserve for 1 year or 3 years
	1. No upfront reserved instances: pay nothing upfront, pay a discounted hourly rate every hour
	2. Partial upfront reserved instances: pay a portion upfront, pay a discounted hourly rate
	3. All upfront reserved instances, pay entirety of the cost upfront
3. Serverless:
	1. Compute(Indexing, Search and Query): billed per OCU(OpenSearch Compute Unit) per hour
	2. Storage: billed per GB per month
4. Ingestion: billed per OCU per hour
5. Direct Query: billed per OCU per hour
6. EBS volume pricing: billed per GB per month
7. UltraWarm and cold storage:
	1. Compute: billed per hour per instance
	2. Storage: billed per GB per month

### Amazon DocumentDB

[Amazon DocumentDB pricing](https://aws.amazon.com/documentdb/pricing/)


AWS Pricing Calculator
AWS Pricing Calculator

Calculate your Amazon DocumentDB (with MongoDB compatibility) and architecture cost in a single estimate.

Create your custom estimate now »

Amazon DocumentDB (with MongoDB compatibility) is a fully managed document database service that supports MongoDB workloads. With Amazon DocumentDB, you only pay for what you use, and there are no upfront costs.

1. Instance types: Standard vs I/O-Optimized
2. On-demand instances: billed per instance per hour
3. Storage: billed per GB per month
4. I/O: billed per 1 million requests, free if using I/O-Optimized
5. Elastic cluster:
	1. Compute: billed per vCPU hour
	2. Storage: billed per GB per month
	3. Backup storage: billed per GB per month
6. Global clusters: fast replication across regions, billed per million replicated write I/O
7. Data transfer: billed per GB
8. Backup storage: billed per GB per month

### Amazon DynamoDB

[Amazon DynamoDB pricing](https://aws.amazon.com/dynamodb/pricing/)

1. On-demand/Provisioned:
	1. Write request: billed per million write request units (1KB)
	2. Read request: billed per million read request units (4KB)
	3. Storage: billed per GB per month
	4. Backup: billed per GB per month
	5. Restore from backup: billed per GB
	6. Global table: billed per million replicated write request units
	7. Change data capture for AWS Kinesis Data Streams/AWS Glue: billed per million change data capture units (1KB)
	8. Data import/export from/to S3: billed per GB
	9. DynamoDB Accelerator(caching service): billed per instance per hour
	10. DynamoDB Streams: billed per million read request units
	11. Data transfer: billed per GB


## Others

### Amazon Athena

[Amazon Athena Pricing](https://aws.amazon.com/athena/pricing/)

Amazon Athena is a serverless, interactive analytics service built on open-source frameworks that enables you to analyze petabytes of data where it lives. With Athena, you can use SQL or Apache Spark and there is no infrastructure to set up or manage. Pricing is simple: you pay based on data processed or compute used.

1. SQL queries: billed per TB of data scanned
	1. Save up to 90% by compressing, partitioning and using columnar formats
2. SQL queries with Provision Capacity: billed per DPU-hour(4 vCPU and 16GB memory) per minute
3. Apache Spark application: billed per DPU-hour per minute
