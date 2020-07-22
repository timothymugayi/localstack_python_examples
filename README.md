# Python Localstack Examples

This repo is to showcase how to use localstack with Python


Create new virtual envionment to run examples against 
localstack docker venv. Execution of your code can be 
done in docker as well.

```
$ cd localstack_service

$ docker-compose build --no-cache 

$ docker-compose up --scale dask-worker=4
```

# Dask Notes

**Dask dashboard Url**: http://localhost:8787/status

**Dask client Url**   : http://localhost:8786

When working with Dask the worker package versions should match with your 
client. Where client is your code that invokes your dask workers via the scheduler. In the examples shown 
client packages are stored in requirements.txt while dask packages 
are in conda environment.yml file

Python version is set to **3.8.3** in condo environment.yml. You may change
this if you wish to match with your client version or change your client version.



## Persisting data across restarts
Localstack's docker container lets you configure the data directory and put it in a mounted volume.

This means data for Kinesis, DynamoDB, Elasticsearch, S3 gets kept across container restarts. This is not the default behaviour.

We can enable this with an environment variable set DATA_DIR=/tmp/localstack/data, or we can hardcode our preferred DATA_DIR into the docker-compose file:

- DATA_DIR=/tmp/localstack/data


## Understanding some of the environment variables 

SERVICES=${SERVICES- }

PORT_WEB_UI=${PORT_WEB_UI- }
 
HOST_TMP_FOLDER


## Accessing your localstack with your AWS CLI

Each of your aws cli commands should consist of the endpoint url 
in the below example am using aws named profile which sets my default access and secret key

```
aws --endpoint-url=http://localhost:4572 s3 ls "s3://nyc-tlc/trip data/" --profile localstack
```

~/.aws/credentials

```
[localstack]
aws_access_key_id = foo
aws_secret_access_key = bar
```

~/.aws/config
```
[profile localstack]
region = us-east-1
output = json
```

## Serverless deploy steps 

```
$ npm install -g serverless

$ npm install

$ npm link    

$ serverless deploy --stage local  --profile localstack

$ serverless invoke --function currentTime --log --profile localstack --stage local

```
The URL pattern for API Gateway localstack executions is

```
http://localhost:4566/restapis/<apiId>/<stage>/_user_request_/<methodPath>
```

This would map to below

```
$ curl http://localhost:4567/restapis/4d0hum90mq/local/_user_request_/ping
```

## Localstack health check 

curl http://localhost:4566/health

Take note initial run of your rest api calls may take sometime

```
{
  "services": {
    "cloudformation": "running",
    "cloudwatch": "running",
    "iam": "running",
    "sts": "running",
    "lambda": "running",
    "logs": "running",
    "s3": "running",
    "sqs": "running",
    "events": "running",
    "apigateway": "running"
  }
}
```


## Want to contribute ?

Feel free to raise A PR with new examples
