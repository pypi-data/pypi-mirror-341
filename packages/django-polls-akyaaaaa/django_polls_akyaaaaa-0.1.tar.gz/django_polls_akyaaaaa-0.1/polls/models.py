from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=200, default='请输入问题')
    pub_date = models.DateTimeField(default=timezone.now)

    def was_published_recently(self):
        """检查问题是否在一天之内发布"""
        return self.pub_date - now() <= timedelta(days=1)

    # admin后台会显示__str__方法内的值
    def __str__(self):
        return self.question


class Choice(models.Model):
    # question 存储的是关联表Question表中的主键值，如果没有显示得定义主键 则主键为id
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
