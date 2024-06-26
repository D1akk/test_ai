from django.db import models
from ckeditor.fields import RichTextField

class Tale(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = RichTextField(verbose_name='Текст')
    translated_content = RichTextField(verbose_name='Перевод')

    def __str__(self):
        return self.title
    
class Question(models.Model):
    tale = models.ForeignKey(Tale, on_delete=models.CASCADE, related_name='questions', verbose_name='Сказка')
    question_text = models.CharField(max_length=255, verbose_name='Текст вопроса')
    answer = models.TextField(verbose_name='Ответ')
    choice_a = models.CharField(max_length=200, verbose_name='Вариант A')
    choice_b = models.CharField(max_length=200, verbose_name='Вариант B')
    choice_c = models.CharField(max_length=200, verbose_name='Вариант C')
    choice_d = models.CharField(max_length=200, verbose_name='Вариант D')
    correct_answer = models.CharField(max_length=1, verbose_name='Правильный ответ')

    def __str__(self):
        return self.question_text
