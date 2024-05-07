from django.db import models

class Tale(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title
    
class Question(models.Model):
    tale = models.ForeignKey(Tale, on_delete=models.CASCADE, related_name='questions', verbose_name='Сказка')
    question_text = models.CharField(max_length=255, verbose_name='Текст вопроса')
    choice_a = models.CharField(max_length=200, verbose_name='Вариант А')
    choice_b = models.CharField(max_length=200, verbose_name='Вариант B')
    choice_c = models.CharField(max_length=200, verbose_name='Вариант C')
    choice_d = models.CharField(max_length=200, verbose_name='Вариант D')
    correct_answer = models.CharField(max_length=200, verbose_name='Правильный ответ')

    def __str__(self):
        return self.question_text