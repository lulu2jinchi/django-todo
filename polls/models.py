from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class TodoItem(models.Model):
    userid = models.IntegerField()
    title = models.TextField()
    create_date = models.DateTimeField('date created')
    due_date = models.DateTimeField('due date')
    # normal: 正常，未完成
    # starred: 星标事件
    # suspended: 挂起事件
    # finished: 已完成事件
    # deleted: 已删除事件
    status = models.TextField(max_length=20)

    def __str__(self):
        return self.status + ': ' + self.title

    def toJSON(self):
        return {
                'id': self.id,
                'title': self.title,
                'create_date': self.create_date.timestamp() * 1000,
                'due_date': self.due_date.timestamp() * 1000,
                'status': self.status
            }
