from tortoise import fields
from tortoise.models import Model


class Bot(Model):
    id = fields.BigIntField(pk=True)
    avatar = fields.CharField(max_length=100, null=True)

    class Meta:
        table = "main_site_bot"


class Server(Model):
    id = fields.BigIntField(pk=True)
    icon = fields.CharField(max_length=100, null=True)

    class Meta:
        table = "main_site_server"


class MemberMeta(Model):
    access_token = fields.CharField(max_length=32, null=True)
    refresh_token = fields.CharField(max_length=32, null=True)

    class Meta:
        table = "main_site_membermeta"
