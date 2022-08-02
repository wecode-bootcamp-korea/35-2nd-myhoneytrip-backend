from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel): 
    name     = models.CharField(max_length=50)
    email    = models.CharField(max_length=200, unique=True, null=True)
    kakao_id = models.BigIntegerField()
    point    = models.DecimalField(max_digits=20 ,decimal_places=2, default=100000000)

    class Meta: 
        db_table = 'users'