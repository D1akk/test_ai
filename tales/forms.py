from django import forms
from .models import Tale, Question

class TaleForm(forms.ModelForm):
    class Meta:
        model = Tale
        fields = ('title', 'content')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_answer']