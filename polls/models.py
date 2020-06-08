import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(verbose_name='问题题目', max_length=200)
    pub_date = models.DateTimeField(verbose_name='发布时间')

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = '问题表'

    # 是否在之前发布
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    # 后台管理——每条记录显示的标题
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='所属问题')
    choice_text = models.CharField(max_length=200, verbose_name='选项')
    votes = models.IntegerField(default=0, verbose_name='票数')

    class Meta:
        verbose_name_plural = '选项表'

    def __str__(self):
        return self.choice_text
