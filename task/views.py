from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Task
from django.views import View
from .forms import TaskCreateForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    template_name = 'home.html'
    return render(request,template_name,{})

@login_required(login_url='/login/')
def task_updateview(request, task_id):
    instance = get_object_or_404(Task,id=task_id)
    form = TaskCreateForm(request.POST or None, instance=instance)
    errors = None
    if form.is_valid() and request.user.is_authenticated():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/tasks/")
    if form.errors:
        errors = form.errors
    template_name = 'update_task.html'
    context = {
        "instance" : instance,
        "form" : form

    }
    return render(request,template_name,context)

@login_required(login_url='/login/')
def task_listview(request):
    template_name = 'task_list.html'
    user_id = request.user.id
    queryset = Task.objects.filter(taskuserid=user_id)
    context = {
        "object_list" : queryset
    }
    return render(request, template_name, context)

@login_required(login_url='/login/')
def create_task(request):
    form = TaskCreateForm(request.POST or None)
    errors = None
    if form.is_valid() and request.user.is_authenticated():
        instance = form.save(commit=False)
        instance.taskuserid = request.user.id
        instance.save()
        return HttpResponseRedirect ("/tasks/")
    if form.errors:
        errors = form.errors
    template_name = 'new_task.html'
    context = {
        "form":form,
        "errors":errors
    }
    return render(request,template_name,context)

@login_required(login_url='/login/')
def delete_task(request,task_id):
    instance = Task.objects.get(id=task_id)
    instance.delete()
    return HttpResponseRedirect("/tasks/")

@login_required(login_url='/login/')
def about_view(request):
    return render(request,"about.html",{})