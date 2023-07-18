from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=150)
    topic = models.CharField(max_length=120)
    
    def __str__(self):
        return f"{self.name}-{self.topic}"

    class Meta:
        verbose_name_plural = 'Quizes'

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question_text)
    
class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.question_text}, answer: {self.answer_text}, correct: {self.correct}"

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)