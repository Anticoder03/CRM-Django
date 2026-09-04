from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail

from .models import Customer, Lead, Opportunity, Activity, Task, User, EmailLog
from .forms import (
    CustomerForm,
    LeadForm,
    OpportunityForm,
    ActivityForm,
    TaskForm,
    EmailForm,
    BulkEmailForm,
)


def _require_login(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(user_name=username)
            if user.check_password(password) and user.is_active:
                request.session["user_id"] = user.id
                request.session["user_name"] = user.user_name
                messages.success(request, f"Welcome back, {user.user_name}!")
                return redirect("user_home")
            else:
                messages.error(request, "Invalid username or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
    return render(request, "user/login.html")


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        errors = []
        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if User.objects.filter(user_name=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, "user/register.html", {
                "form_data": {"username": username, "email": email}
            })

        user = User(
            user_name=username,
            email=email,
            password=User.hash_password(password),
        )
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "user/register.html", {"form_data": {}})


def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("login")


def user_home(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    total_customers = Customer.objects.count()
    total_leads = Lead.objects.count()
    total_opportunities = Opportunity.objects.count()
    won_opportunities = Opportunity.objects.filter(stage="Won").count()
    lost_opportunities = Opportunity.objects.filter(stage="Lost").count()
    total_activities = Activity.objects.count()
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status="Pending").count()
    completed_tasks = Task.objects.filter(status="Completed").count()

    new_leads = Lead.objects.filter(status="New").count()
    contacted_leads = Lead.objects.filter(status="Contacted").count()
    qualified_leads = Lead.objects.filter(status="Qualified").count()
    converted_leads = Lead.objects.filter(status="Converted").count()
    lost_leads = Lead.objects.filter(status="Lost").count()

    total_revenue = (
        Opportunity.objects.filter(stage="Won").values_list("amount", flat=True)
    )
    revenue_sum = sum(float(a) for a in total_revenue)

    pipeline_value = (
        Opportunity.objects.exclude(stage__in=["Won", "Lost"]).values_list(
            "amount", flat=True
        )
    )
    pipeline_sum = sum(float(a) for a in pipeline_value)

    recent_leads = Lead.objects.order_by("-created_at")[:5]
    recent_customers = Customer.objects.order_by("-created_at")[:5]
    recent_activities = Activity.objects.order_by("-activity_date")[:5]
    upcoming_tasks = Task.objects.filter(status="Pending").order_by("due_date")[:5]
    email_count = EmailLog.objects.count()

    lead_status_data = {
        "New": new_leads,
        "Contacted": contacted_leads,
        "Qualified": qualified_leads,
        "Converted": converted_leads,
        "Lost": lost_leads,
    }

    stage_data = {}
    for stage, _ in Opportunity.Stage_Choices:
        stage_data[stage] = Opportunity.objects.filter(stage=stage).count()

    context = {
        "current_user": current_user,
        "total_customers": total_customers,
        "total_leads": total_leads,
        "total_opportunities": total_opportunities,
        "won_opportunities": won_opportunities,
        "lost_opportunities": lost_opportunities,
        "total_activities": total_activities,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "new_leads": new_leads,
        "contacted_leads": contacted_leads,
        "qualified_leads": qualified_leads,
        "converted_leads": converted_leads,
        "lost_leads": lost_leads,
        "revenue_sum": revenue_sum,
        "pipeline_sum": pipeline_sum,
        "recent_leads": recent_leads,
        "recent_customers": recent_customers,
        "recent_activities": recent_activities,
        "upcoming_tasks": upcoming_tasks,
        "email_count": email_count,
        "lead_status_data": lead_status_data,
        "stage_data": stage_data,
    }
    return render(request, "user/user_home.html", context)


# ===================== CUSTOMER CRUD =====================

def customer_list(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer created successfully!")
            return redirect("customer_list")
    else:
        form = CustomerForm()

    search = request.GET.get("search", "")
    customers = Customer.objects.all()
    if search:
        customers = customers.filter(
            models.Q(customer_name__icontains=search)
            | models.Q(company__icontains=search)
            | models.Q(email__icontains=search)
            | models.Q(phone__icontains=search)
        )

    context = {
        "customers": customers,
        "form": form,
        "current_user": current_user,
        "search": search,
    }
    return render(request, "user/customer_list.html", context)


def customer_update(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully!")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)

    context = {
        "form": form,
        "title": "Edit Customer",
        "entity": customer,
        "current_user": current_user,
        "cancel_url": "customer_list",
    }
    return render(request, "user/edit_form.html", context)


def customer_delete(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    customer = get_object_or_404(Customer, pk=pk)
    name = customer.customer_name
    customer.delete()
    messages.success(request, f"Customer '{name}' deleted successfully!")
    return redirect("customer_list")


# ===================== LEAD CRUD =====================

def lead_list(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead created successfully!")
            return redirect("lead_list")
    else:
        form = LeadForm()

    leads = Lead.objects.all()
    context = {
        "leads": leads,
        "form": form,
        "current_user": current_user,
    }
    return render(request, "user/lead_list.html", context)


def lead_update(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead updated successfully!")
            return redirect("lead_list")
    else:
        form = LeadForm(instance=lead)

    context = {
        "form": form,
        "title": "Edit Lead",
        "entity": lead,
        "current_user": current_user,
        "cancel_url": "lead_list",
    }
    return render(request, "user/edit_form.html", context)


def lead_delete(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    lead = get_object_or_404(Lead, pk=pk)
    name = lead.name
    lead.delete()
    messages.success(request, f"Lead '{name}' deleted successfully!")
    return redirect("lead_list")


# ===================== OPPORTUNITY CRUD =====================

def opportunity_list(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity created successfully!")
            return redirect("opportunity_list")
    else:
        form = OpportunityForm()

    opportunities = Opportunity.objects.all()
    context = {
        "opportunities": opportunities,
        "form": form,
        "current_user": current_user,
    }
    return render(request, "user/opportunity_list.html", context)


def opportunity_update(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity updated successfully!")
            return redirect("opportunity_list")
    else:
        form = OpportunityForm(instance=opportunity)

    context = {
        "form": form,
        "title": "Edit Opportunity",
        "entity": opportunity,
        "current_user": current_user,
        "cancel_url": "opportunity_list",
    }
    return render(request, "user/edit_form.html", context)


def opportunity_delete(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    opportunity = get_object_or_404(Opportunity, pk=pk)
    title = opportunity.title
    opportunity.delete()
    messages.success(request, f"Opportunity '{title}' deleted successfully!")
    return redirect("opportunity_list")


# ===================== ACTIVITY CRUD =====================

def activity_list(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity created successfully!")
            return redirect("activity_list")
    else:
        form = ActivityForm()

    activities = Activity.objects.all()
    context = {
        "activities": activities,
        "form": form,
        "current_user": current_user,
    }
    return render(request, "user/activity_list.html", context)


def activity_update(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            return redirect("activity_list")
    else:
        form = ActivityForm(instance=activity)

    context = {
        "form": form,
        "title": "Edit Activity",
        "entity": activity,
        "current_user": current_user,
        "cancel_url": "activity_list",
    }
    return render(request, "user/edit_form.html", context)


def activity_delete(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    activity = get_object_or_404(Activity, pk=pk)
    subject = activity.subject
    activity.delete()
    messages.success(request, f"Activity '{subject}' deleted successfully!")
    return redirect("activity_list")


# ===================== TASK CRUD =====================

def task_list(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully!")
            return redirect("task_list")
    else:
        form = TaskForm()

    tasks = Task.objects.all()
    context = {
        "tasks": tasks,
        "form": form,
        "current_user": current_user,
    }
    return render(request, "user/task_list.html", context)


def task_update(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    context = {
        "form": form,
        "title": "Edit Task",
        "entity": task,
        "current_user": current_user,
        "cancel_url": "task_list",
    }
    return render(request, "user/edit_form.html", context)


def task_delete(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    task = get_object_or_404(Task, pk=pk)
    title = task.title
    task.delete()
    messages.success(request, f"Task '{title}' deleted successfully!")
    return redirect("task_list")


# ===================== EMAIL FEATURES =====================

def email_compose(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            try:
                send_mail(
                    subject,
                    message,
                    None,
                    [customer.email],
                    fail_silently=False,
                )
                EmailLog.objects.create(
                    subject=subject,
                    body=message,
                    recipient_emails=customer.email,
                    recipient_count=1,
                    sent_by=current_user,
                    is_bulk=False,
                    status="Sent",
                )
                messages.success(
                    request,
                    f"Email sent successfully to {customer.customer_name} ({customer.email})!",
                )
                return redirect("email_log")
            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
    else:
        form = EmailForm()

    context = {
        "form": form,
        "current_user": current_user,
    }
    return render(request, "user/email_compose.html", context)


def email_bulk(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    if request.method == "POST":
        form = BulkEmailForm(request.POST)
        if form.is_valid():
            recipients = list(form.cleaned_data["recipients"])
            include_leads = form.cleaned_data.get("include_leads", False)
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            recipient_emails = set()
            for c in recipients:
                if c.email:
                    recipient_emails.add(c.email)
            if include_leads:
                for l in Lead.objects.all():
                    if l.email:
                        recipient_emails.add(l.email)

            if not recipient_emails:
                messages.error(request, "No valid email recipients selected.")
                return render(
                    request,
                    "user/email_bulk.html",
                    {"form": form, "current_user": current_user},
                )

            try:
                send_mail(
                    subject,
                    message,
                    None,
                    list(recipient_emails),
                    fail_silently=False,
                )
                EmailLog.objects.create(
                    subject=subject,
                    body=message,
                    recipient_emails=", ".join(sorted(recipient_emails)),
                    recipient_count=len(recipient_emails),
                    sent_by=current_user,
                    is_bulk=True,
                    status="Sent",
                )
                messages.success(
                    request,
                    f"Bulk email sent to {len(recipient_emails)} recipient(s)!",
                )
                return redirect("email_log")
            except Exception as e:
                messages.error(request, f"Failed to send bulk email: {e}")
    else:
        form = BulkEmailForm()

    context = {
        "form": form,
        "current_user": current_user,
    }
    return render(request, "user/email_bulk.html", context)


def email_log(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")

    logs = EmailLog.objects.all().order_by("-sent_at")
    context = {
        "logs": logs,
        "current_user": current_user,
    }
    return render(request, "user/email_log.html", context)
