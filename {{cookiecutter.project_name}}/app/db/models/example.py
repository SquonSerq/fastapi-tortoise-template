from tortoise import models, fields


class Example(models.Model):
    id = fields.IntField(pk=True)
