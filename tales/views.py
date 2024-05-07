from django.shortcuts import render, redirect, get_object_or_404
from .models import Tale, Question
from .forms import TaleForm, QuestionForm
import json
import g4f

def generate_question_content(tale_content):
    prompt = "Сгенерируй по тексту вопрос с 4 вариантами ответов и верни в формате json(question, choices[], answer): "
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": prompt + tale_content,
        }]
    )
    return json.loads(response)


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
            generated_content = generate_question_content(tale.content)
            question.question_text = generated_content['question']
            question.choice_a = generated_content['choices'][0]
            question.choice_b = generated_content['choices'][1]
            question.choice_c = generated_content['choices'][2]
            question.choice_d = generated_content['choices'][3]
            question.correct_answer = generated_content['answer']
            question.save()
            return redirect('tale_detail', pk=tale_id)
    else:
        form = QuestionForm()
    return render(request, 'question_edit.html', {'form': form, 'tale': tale})

def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question.save()
            return redirect('tale_detail', pk=question.tale.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question_edit.html', {'form': form})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    tale_id = question.tale.pk
    question.delete()
    return redirect('tale_detail', pk=tale_id)


