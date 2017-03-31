# data-processor

AWS lambda function that get user data from kinesis and store in S3 buckets

The project uses [Serverless](https://github.com/serverless/serverless) for deploying the lambda function.

## Set up

Install serverless and required plugins on your machine:

```
npm install
```


## Deploy

You can deploy the latest version to amazon running this command:

```
npm run serverless deploy 
```

## Fast Deploy


```
npm run serverless deploy -f data-processor
```
