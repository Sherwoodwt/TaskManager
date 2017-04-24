'''
Library of sns functions
'''

import boto3

from django.conf import settings

def notify_comment(comment, url, targets):
    '''
    @param comment: Comment made on task
    @param url: link to task page
    @param targets: everyone to notify
    '''
    task = comment.task
    commenter = comment.created_by
    subject = commenter.username + " has commented on a task"
    message = COMMENT_MESSAGE.format(
        commenter.username,
        task.title,
        comment.text,
        url
    )
    for target in targets:
        notify_user(target, subject, message)

def notify_assigned_task(task, url):
    '''
    @param task: Task that has been assigned to somebody
    '''
    assignee = task.assignee
    assigner = task.created_by
    subject = "You have been assigned a task"
    message = TASK_MESSAGE.format(
        assigner.username,
        task.title,
        task.due_date,
        url
    )
    notify_user(assignee, subject, message)


def notify_user(user, subject, message):
    '''
    Params:
        User user: The user being notified
        str subject: The subject of the message
        str message: The body of the message

    If the user.userprofile.is_notifiable, a message is published to their notification_arn.
    If the notification_arn is not set, if the user is not notifiable, or if the subscription
    has not been confirmed, nothing is sent.
    '''
    try:
        profile = user.userprofile
        sns = boto3.resource('sns')
        if (
                profile.is_notifiable and
                profile.notification_arn
        ):
            topic = sns.Topic(profile.notification_arn)
            topic.publish(Subject=subject, Message=message)
    except:
        print('User requested might not have a UserProfile')

def create_topic(user):
    '''
    Params:
        User user: User getting notification arn
    '''
    client = boto3.client('sns')
    topic_name = user.username + '_notifications'
    topic = client.create_topic(Name=topic_name)
    return topic['TopicArn']

def create_subscription(topic_arn, user):
    '''
    Params:
        str topic_arn: arn of topic to subscribe to
    '''
    client = boto3.client('sns')
    return client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=user.email
    )['SubscriptionArn']

COMMENT_MESSAGE = """{} has commented on this task:
{}

'{}'
{}
"""

TASK_MESSAGE = """{} has assigned you to a task:
{}

Due Date: {}
{}
"""
