from django.shortcuts import render, redirect, get_object_or_404
from .models import Tale, Question
from .forms import TaleForm, QuestionForm
import json
import g4f

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest

def generate_question(request: HttpRequest, tale_id):
    tale = get_object_or_404(Tale, pk=tale_id)
    prompt = "Сгенерируй по тексту вопрос с 4 вариантами ответов и верни в формате json(question, choices[], answer): "
    text = tale.content
    rules = request.POST.get('rules', '')  # Получаем правила из формы

    if rules.strip():  # Проверяем, что правила не пустые
        full_prompt = f"{prompt}{text} {rules.strip()}"
    else:
        full_prompt = f"{prompt}{text}"

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": full_prompt,
        }]
    )
    data = json.loads(response)
    question = Question(
        tale=tale,
        question_text=data['question'],
        choice_a=data['choices'][0],
        choice_b=data['choices'][1],
        choice_c=data['choices'][2],
        choice_d=data['choices'][3],
        correct_answer=data['answer'],
    )
    question.save()
    return redirect('tale_detail', pk=tale_id)


def tale_list(request):
    tales = Tale.objects.all()
    return render(request, 'tale_list.html', {'tales': tales})

def tale_detail(request, pk):
    tale = get_object_or_404(Tale, pk=pk)
    return render(request, 'tale_detail.html', {'tale': tale})

def tale_new(request):
    if request.method == "POST":
        form = TaleForm(request.POST)
        if form.is_valid():
            tale = form.save(commit=False)
            tale.save()
            return redirect('tale_detail', pk=tale.pk)
    else:
        form = TaleForm()
    return render(request, 'tale_edit.html', {'form': form})

def tale_edit(request, pk):
    tale = get_object_or_404(Tale, pk=pk)
    if request.method == "POST":
        form = TaleForm(request.POST, instance=tale)
        if form.is_valid():
            tale = form.save(commit=False)
            tale.save()
            return redirect('tale_detail', pk=tale.pk)
    else:
        form = TaleForm(instance=tale)
    return render(request, 'tale_edit.html', {'form': form})

def tale_delete(request, pk):
    tale = get_object_or_404(Tale, pk=pk)
    tale.delete()
    return redirect('tale_list')

def question_new(request, tale_id):
    tale = get_object_or_404(Tale, pk=tale_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.tale = tale
            question.save()
            return redirect('tale_detail', pk=tale_id)  # Убедитесь, что здесь передается правильный pk
    else:
        form = QuestionForm()
    return render(request, 'question_edit.html', {'form': form, 'tale': tale})

def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    tale_id = question.tale.pk  # Убедитесь, что tale_id получает корректный pk из модели вопроса
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question.save()
            return redirect('tale_detail', pk=tale_id)  # Проверьте, что tale_id передаётся правильно
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question_edit.html', {'form': form, 'tale': question.tale})


def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    tale_id = question.tale.pk
    question.delete()
    return redirect('tale_detail', pk=tale_id)


