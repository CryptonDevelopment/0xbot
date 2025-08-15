import config
from tortoise import Tortoise, fields
from tortoise.models import Model
from time import time


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.TextField(null=True)
    lang = fields.TextField()
    last_seen = fields.BigIntField(default = int(time()))

    class Meta:
        table = "user"


class MessageToDelete(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()

    class Meta:
        table = "message_to_delete"


class TimerMessage(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="user_timer")
    created = fields.BigIntField(default = int(time()))
    timer = fields.BigIntField()
    after = fields.TextField()
    active = fields.BooleanField(default = True)

    class Meta:
        table = "timer_message"



async def init():
    try:
        await Tortoise.init(config.TORTOISE_ORM)
        await Tortoise.generate_schemas()
        #await TimerMessage.all().delete() # TODO DELETE
    except Exception as e:
        print(e)
