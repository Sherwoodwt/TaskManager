'''
Library of sns functions
'''

import boto3

from django.conf import settings

def notify_comment(comment, url):
    '''
    @param comment: Comment made on task
    '''
    task = comment.task
    target = task.assignee
    commenter = comment.created_by
    subject = commenter.username + " has commented on the task '" + task.title + "'"
    message = comment.text + "\n\nurl: " + url + "\n\n\n\n"
    notify_user(target, subject, message)

def notify_assigned_task(task, url):
    '''
    @param task: Task that has been assigned to somebody
    '''
    assignee = task.assignee
    assigner = task.created_by
    subject = "You have been assigned a task by " + assigner.username
    message = (
        task.title +
        "\n\nI can't give you a link to it yet so you're gonna have to go to the site manually."
        "\nDue Date: " + str(task.due_date) +
        "\n\nurl: " + url + "\n\n\n\n"
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
    profile = user.userprofile
    sns = boto3.resource('sns')
    if (
            profile.is_notifiable and
            profile.notification_arn
    ):
        topic = sns.Topic(profile.notification_arn)
        topic.publish(Subject=subject, Message=message)

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
