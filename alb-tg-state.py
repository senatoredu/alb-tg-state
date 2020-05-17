import boto3
import datetime


def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    alb = boto3.client('elbv2')

    time = datetime.datetime.now()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # describe tg hc
    tg_hc_state = alb.describe_target_health(
        TargetGroupArn='arn:aws:elasticloadbalancing:eu-west-1:123456789:targetgroup/azure-test/77693f6b63cdddd8')

    tg_hc_state = str(tg_hc_state)
    # put describe tg hc into the ddb

    response = dynamodb.put_item(
        Item={
            'Timestamp': {
                'S': timestamp,
            },
            'Health': {
                'S': tg_hc_state,
            }
        },
        TableName='azure-test_tg_hc_state',
    )
