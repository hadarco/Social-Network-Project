from django.core.exceptions import ValidationError
import os


def read_bad_tokens():
    with open(os.path.join(os.getcwd(),'tweets/youtube.txt'), 'r') as f:
        lines = set(f.read().split(','))
    with open(os.path.join(os.getcwd(),'tweets/facebook.txt'), 'r') as f:
        lines | set(f.read().split(','))
    return list(map(lambda x: x.strip(), lines))


def validate_bad_content(val):
    if val not in read_bad_tokens():
        return val
    raise ValidationError("You can't use {} in your tweet".format(val))


def validate_blank_content(val):
    if val != "":
        return val
    raise ValidationError("You can't post a blank  tweet")