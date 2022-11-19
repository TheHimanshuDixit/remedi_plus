from tortoise import fields, models


class Timer(models.Model):
    class Meta:
        table = "timers"

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    dosage = fields.CharField(max_length=50)
    phone = fields.BigIntField()

    created_at = fields.DatetimeField(auto_now=True)
    expires = fields.DatetimeField()


class FreeUse(models.Model):
    class Meta:
        table = "free_uses"

    phone = fields.BigIntField(pk=True, generated=False)
    timer_id = fields.IntField()
    used_at = fields.DatetimeField(auto_now=True)
