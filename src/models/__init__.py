from tortoise import fields, models
import aiohttp
from decouple import config


class Timer(models.Model):
    class Meta:
        table = "timers"

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    dosage = fields.CharField(max_length=50)
    phone = fields.BigIntField()

    created_at = fields.DatetimeField(auto_now=True)
    dispatched = fields.BooleanField(default=False)
    expires = fields.DatetimeField()

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(config("WHATSAPP_API")),
        }

    @property
    def body(self):
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "919996071403",
            "type": "template",
            "template": {"name": "hello_world", "language": {"code": "en_US"}},
        }

    async def dispatch(self):
        print("[ID: {}] Dispatching Reminder...".format(self.id))
        await Timer.get(pk=self.pk).update(dispatched=True)

        url = "https://graph.facebook.com/v15.0/103233349288425/messages"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=self.body, headers=self.headers) as resp:
                print(await resp.json())


class FreeUse(models.Model):
    class Meta:
        table = "free_uses"

    phone = fields.BigIntField(pk=True, generated=False)
    timer_id = fields.IntField()
    used_at = fields.DatetimeField(auto_now=True)
