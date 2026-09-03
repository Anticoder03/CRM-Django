from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer, Lead, Opportunity, Activity, Task, User
from .forms import CustomerForm, LeadForm, OpportunityForm, ActivityForm, TaskForm


# Create your views here.
def user_home(request):
    return render(request, "user/user_home.html")


def customer_list(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    customers = Customer.objects.all()
    context = {
        'customers': customers,
        'form': form,
    }
    return render(request, 'user/customer_list.html', context)


def lead_list(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead created successfully!')
            return redirect('lead_list')
    else:
        form = LeadForm()
    
    leads = Lead.objects.all()
    context = {
        'leads': leads,
        'form': form,
    }
    return render(request, 'user/lead_list.html', context)


def opportunity_list(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity created successfully!')
            return redirect('opportunity_list')
    else:
        form = OpportunityForm()
    
    opportunities = Opportunity.objects.all()
    context = {
        'opportunities': opportunities,
        'form': form,
    }
    return render(request, 'user/opportunity_list.html', context)


def activity_list(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity created successfully!')
            return redirect('activity_list')
    else:
        form = ActivityForm()
    
    activities = Activity.objects.all()
    context = {
        'activities': activities,
        'form': form,
    }
    return render(request, 'user/activity_list.html', context)


def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'user/task_list.html', context)
