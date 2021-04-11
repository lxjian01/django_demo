from django.db import models

from utils.base_model import BaseModel


class UserInfo(BaseModel):
    class Meta:
        db_table = "userinfo"
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64,null=False,unique=True)
    pwd = models.CharField(max_length=128,null=False)
    email = models.CharField(max_length=128, null=False,unique=True)
    is_active = models.IntegerField(default=1, null=False,verbose_name="是否激活（0：已激活，1：未激活）")
    is_enabled = models.IntegerField(default=0,null=False,verbose_name="是否启用（0：启用，1：禁用）")
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()