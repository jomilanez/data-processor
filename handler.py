import boto3
import json
import logging
import base64
import os
import sys

logger = logging.getLogger()
logger.setLevel(logging.WARN)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./.requirements"))

from aws_kinesis_agg.deaggregator import deaggregate_records

client = boto3.client('s3')

RECOMMENDATION_DATA = ['teaser_open', 'teaser_opened',
                      'interested_enabled', 'interested_disabled', 'not_interested_enabled', 'not_interested_disabled']


def save(parsed_data, key, bucket_name):
    client.put_object(Bucket=bucket_name, Key=key, Body=parsed_data)

def handle(event, context):
    for record in deaggregate_records(event['Records']):
        payload = base64.b64decode(record['kinesis']['data'])
        try:
            parsed_data = json.loads(payload)
            key = "%s.json" % parsed_data['eventId']
            if parsed_data['eventType'] in RECOMMENDATION_DATA:
                save(payload, key, 'bucket-josiane1')
            save(payload, key, 'bucket-josiane2')
        except Exception:
            logging.exception('message')


