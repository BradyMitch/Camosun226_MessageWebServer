from django.db import models
from django.core.exceptions import ValidationError
import json

KEY_SIZE = 8
MAX_MSQ_SIZE = 160

# PURPOSE:
# Validate key for correct length (8 characters)
# Validate key for being alphanumeric
#
# PARAMETERS:
# 'value' is the key
#
# RETURN/SIDE EFFECTS/NOTES:
# Raises ValidationError if length is not 8 and/or not alphanumeric
# Called from Message class
#
def validate_key(value):
    if len(value) != KEY_SIZE or not value.isalnum():
        raise ValidationError('Key must be 8 (alphanumeric) characters long.')

# PURPOSE:
# Defines database columns 'key' and 'msg'
#
# PARAMETERS:
# 'models.Model' defines class as a Model
#
# RETURN/SIDE EFFECTS/NOTES:
# 'key' is primary key
#
class Message(models.Model):
    key = models.CharField(max_length=KEY_SIZE, primary_key=True, validators=[validate_key])
    msg = models.CharField(max_length=MAX_MSQ_SIZE)

    def __str__(self):
        return '(' + str(self.key) + ',' + str(self.msg) + ')'

# PURPOSE:
# Encode key-msg pairs of Message class into json format
#
class JSONEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return { 'key' : obj.key, 'msg' : obj.msg}
        return json.JSONEncoder.default(self, obj)
