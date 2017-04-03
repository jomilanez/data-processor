import boto3
import json
import logging
import base64
import os
import sys
import time

logger = logging.getLogger()
logger.setLevel(logging.WARN)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./.requirements"))

from aws_kinesis_agg.deaggregator import deaggregate_records
from datadog import initialize, api

options = {
    'api_key': '5590e1ccc09e95eb8be59d73b9b808de',
    'app_key': '4077817914fe339015139cbb1a65b2ff8e972369'
}
initialize(**options)

bucket_1 = os.environ['BUCKET_1']
bucket_2 = os.environ['BUCKET_2']
environment = os.environ['ENVIRONMENT']

client = boto3.client('s3')

RECOMMENDATION_DATA = ['teaser_open', 'teaser_opened',
                      'interested_enabled', 'interested_disabled', 'not_interested_enabled', 'not_interested_disabled']


def save(parsed_data, key, bucket_name):
    client.put_object(Bucket=bucket_name, Key=key, Body=parsed_data)

def handle(event, context):
    parsed_successful = 0
    parsed_failed = 0
    for record in deaggregate_records(event['Records']):
        payload = base64.b64decode(record['kinesis']['data'])
        try:
            parsed_data = json.loads(payload)
            key = "%s.json" % parsed_data['eventId']
            if parsed_data['eventType'] in RECOMMENDATION_DATA:
                save(payload, key, bucket_1)
            save(payload, key, bucket_2)
            parsed_successful += 1
        except Exception:
            logging.exception('message')
            parsed_failed += 1
    send_metrics('parsed.successfull', parsed_successful)
    send_metrics('parsed.failed', parsed_failed)

def send_metrics(metric_name, number):
    api.Metric.send(metric=metric_name, points=(time.time(), number), tags=['environment:%s' % environment])
