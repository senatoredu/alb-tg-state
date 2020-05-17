# alb-tg-state

Application Load Balancer Target Health Recorder whose function is to record the target health unhealthy reason when a target goes unhealthy.
ALB in its current form only notifies when an unhealthy host count is recorded (>0) via Cloudwatch alarms, but it has no way of representating the current
state of the targets at the time of the alarm, i.e it tells you something went wrong (unhealthyhost), but doesn't tell you which host went unhealthy.

This program is built to persist that information (i.e when the alarm fired what targets where unhealthy and why).

Architecture leverages 4 aws services:

- Cloudwatch Alarm
- SNS
- Lambda
- Dynamodb (DDB)

#  Cloudwatch Alarm

Tracks the unhealthy target count of an ALB's target group and when the threshold is > 0 the alarm goes from 'ok' to 'alarm'.


#  SNS

Serves as in input trigger or link between the cw alarm and the lambda function.
cw alarm -> SNS -> lambda

#  Lambda

Python 3 codebase that uses the aws boto3 sdk, it connects to the alb and ddb objects, does a describe on the tg and then writes the information
gotten to ddb

#  DDB

DB that holds the persisted info of the target health state and unhealthy reason for admin to track what happened.
Keeps information of the time that the put_item was recorded and holds the information of the describe_target_health output.

This code is suited for usecases where the target state of alb tg's are unstable, if a target flips in and out of unhealthy you want to know the reason why.