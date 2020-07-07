#!/usr/bin/env bash

printf "Configuring localstack components..."
sleep 5;
set -x

aws configure set aws_access_key_id foo
aws configure set aws_secret_access_key bar

echo "[default]" > ~/.aws/config
echo "region = us-east-1" >> ~/.aws/config
echo "output = json" >> ~/.aws/config

aws --endpoint http://localstack:4576 sqs create-queue --queue-name blockchain-local-engine-cancel
aws --endpoint http://localstack:4576 sqs create-queue --queue-name blockchain-local-engine-input.fifo --attributes FifoQueue=true,MessageGroupId=blockchain
aws --endpoint http://localstack:4576 sqs create-queue --queue-name blockchain-local-engine-output.fifo --attributes FifoQueue=true,MessageGroupId=blockchain


aws --endpoint-url=http://localstack:4572 s3api create-bucket --bucket blockchain-s3-local-bitcoin
aws --endpoint-url=http://localstack:4572 s3api create-bucket --bucket blockchain-s3-local-ziliqa
aws --endpoint-url=http://localstack:4572 s3api create-bucket --bucket blockchain-s3-local-xrp
aws --endpoint-url=http://localstack:4572 s3api create-bucket --bucket blockchain-s3-local-ada
aws --endpoint-url=http://localstack:4572 s3api create-bucket --bucket blockchain-s3-local-eth

aws --endpoint-url=http://localstack:4572 s3api create-bucket --bucket nyc-tlc

set +x

printf "Localstack dashboard : http://localhost:8080/#!/infra"