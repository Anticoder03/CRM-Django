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


def _visible_customers(user):
    if user.is_admin:
        return Customer.objects.all()
    return Customer.objects.filter(assign_to=user)


def _visible_leads(user):
    if user.is_admin:
        return Lead.objects.all()
    return Lead.objects.filter(assign_to=user)


def _visible_opportunities(user):
    if user.is_admin:
        return Opportunity.objects.all()
    return Opportunity.objects.filter(assign_to=user)


def _visible_activities(user):
    if user.is_admin:
        return Activity.objects.all()
    return Activity.objects.filter(assign_to=user)


def _visible_tasks(user):
    if user.is_admin:
        return Task.objects.all()
    return Task.objects.filter(assign_to=user)


def _can_access(user, record):
    if user.is_admin:
        return True
    assignee = getattr(record, "assign_to", None)
    return assignee is not None and assignee.id == user.id


def _deny(request, url_name):
    messages.error(request, "You do not have permission to access this record.")
    return redirect(url_name)


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

    customers = _visible_customers(current_user)
    leads = _visible_leads(current_user)
    opportunities = _visible_opportunities(current_user)
    activities = _visible_activities(current_user)
    tasks = _visible_tasks(current_user)

    total_customers = customers.count()
    total_leads = leads.count()
    total_opportunities = opportunities.count()
    won_opportunities = opportunities.filter(stage="Won").count()
    lost_opportunities = opportunities.filter(stage="Lost").count()
    total_activities = activities.count()
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status="Pending").count()
    completed_tasks = tasks.filter(status="Completed").count()

    new_leads = leads.filter(status="New").count()
    contacted_leads = leads.filter(status="Contacted").count()
    qualified_leads = leads.filter(status="Qualified").count()
    converted_leads = leads.filter(status="Converted").count()
    lost_leads = leads.filter(status="Lost").count()

    total_revenue = (
        opportunities.filter(stage="Won").values_list("amount", flat=True)
    )
    revenue_sum = sum(float(a) for a in total_revenue)

    pipeline_value = (
        opportunities.exclude(stage__in=["Won", "Lost"]).values_list(
            "amount", flat=True
        )
    )
    pipeline_sum = sum(float(a) for a in pipeline_value)

    recent_leads = leads.order_by("-created_at")[:5]
    recent_customers = customers.order_by("-created_at")[:5]
    recent_activities = activities.order_by("-activity_date")[:5]
    upcoming_tasks = tasks.filter(status="Pending").order_by("due_date")[:5]
    email_logs = EmailLog.objects.all()
    if not current_user.is_admin:
        email_logs = email_logs.filter(sent_by=current_user)
    email_count = email_logs.count()

    lead_status_data = {
        "New": new_leads,
        "Contacted": contacted_leads,
        "Qualified": qualified_leads,
        "Converted": converted_leads,
        "Lost": lost_leads,
    }

    stage_data = {}
    for stage, _ in Opportunity.Stage_Choices:
        stage_data[stage] = opportunities.filter(stage=stage).count()

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
        form = CustomerForm(request.POST, user=current_user)
        if form.is_valid():
            customer = form.save(commit=False)
            if not current_user.is_admin:
                customer.assign_to = current_user
            customer.save()
            messages.success(request, "Customer created successfully!")
            return redirect("customer_list")
    else:
        form = CustomerForm(user=current_user)

    search = request.GET.get("search", "")
    customers = _visible_customers(current_user)
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
    if not _can_access(current_user, customer):
        return _deny(request, "customer_list")

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer, user=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully!")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer, user=current_user)

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
    if not _can_access(current_user, customer):
        return _deny(request, "customer_list")

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
        form = LeadForm(request.POST, user=current_user)
        if form.is_valid():
            lead = form.save(commit=False)
            if not current_user.is_admin:
                lead.assign_to = current_user
            lead.save()
            messages.success(request, "Lead created successfully!")
            return redirect("lead_list")
    else:
        form = LeadForm(user=current_user)

    leads = _visible_leads(current_user)
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
    if not _can_access(current_user, lead):
        return _deny(request, "lead_list")

    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead, user=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead updated successfully!")
            return redirect("lead_list")
    else:
        form = LeadForm(instance=lead, user=current_user)

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
    if not _can_access(current_user, lead):
        return _deny(request, "lead_list")

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
        form = OpportunityForm(request.POST, user=current_user)
        if form.is_valid():
            opportunity = form.save(commit=False)
            if not current_user.is_admin:
                opportunity.assign_to = current_user
            opportunity.save()
            messages.success(request, "Opportunity created successfully!")
            return redirect("opportunity_list")
    else:
        form = OpportunityForm(user=current_user)

    opportunities = _visible_opportunities(current_user)
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
    if not _can_access(current_user, opportunity):
        return _deny(request, "opportunity_list")

    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity, user=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity updated successfully!")
            return redirect("opportunity_list")
    else:
        form = OpportunityForm(instance=opportunity, user=current_user)

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
    if not _can_access(current_user, opportunity):
        return _deny(request, "opportunity_list")

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
        form = ActivityForm(request.POST, user=current_user)
        if form.is_valid():
            activity = form.save(commit=False)
            if not current_user.is_admin:
                activity.assign_to = current_user
                activity.created_by = current_user
            activity.save()
            messages.success(request, "Activity created successfully!")
            return redirect("activity_list")
    else:
        form = ActivityForm(user=current_user)

    activities = _visible_activities(current_user)
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
    if not _can_access(current_user, activity):
        return _deny(request, "activity_list")

    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity, user=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            return redirect("activity_list")
    else:
        form = ActivityForm(instance=activity, user=current_user)

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
    if not _can_access(current_user, activity):
        return _deny(request, "activity_list")

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
        form = TaskForm(request.POST, user=current_user)
        if form.is_valid():
            task = form.save(commit=False)
            if not current_user.is_admin:
                task.assign_to = current_user
                task.created_by = current_user
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(user=current_user)

    tasks = _visible_tasks(current_user)
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
    if not _can_access(current_user, task):
        return _deny(request, "task_list")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task, user=current_user)

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
    if not _can_access(current_user, task):
        return _deny(request, "task_list")

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
        form = EmailForm(request.POST, user=current_user)
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
        form = EmailForm(user=current_user)

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
        form = BulkEmailForm(request.POST, user=current_user)
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
                for l in _visible_leads(current_user):
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
        form = BulkEmailForm(user=current_user)

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
    if not current_user.is_admin:
        logs = logs.filter(sent_by=current_user)
    context = {
        "logs": logs,
        "current_user": current_user,
    }
    return render(request, "user/email_log.html", context)


# ===================== USER MANAGEMENT (ADMIN ONLY) =====================

def user_list(request):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")
    if not current_user.is_admin:
        messages.error(request, "Only admins can access user management.")
        return redirect("user_home")

    users = User.objects.all().order_by("id")
    context = {
        "users": users,
        "current_user": current_user,
    }
    return render(request, "user/user_list.html", context)


def user_toggle_admin(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")
    if not current_user.is_admin:
        return _deny(request, "user_list")

    target = get_object_or_404(User, pk=pk)
    if target.id == current_user.id:
        messages.error(request, "You cannot change your own admin status.")
    else:
        target.is_admin = not target.is_admin
        target.save()
        verb = "promoted to admin" if target.is_admin else "demoted to regular user"
        messages.success(request, f"'{target.user_name}' was {verb}.")
    return redirect("user_list")


def user_toggle_active(request, pk):
    current_user = _require_login(request)
    if not current_user:
        return redirect("login")
    if not current_user.is_admin:
        return _deny(request, "user_list")

    target = get_object_or_404(User, pk=pk)
    if target.id == current_user.id:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        target.is_active = not target.is_active
        target.save()
        verb = "activated" if target.is_active else "deactivated"
        messages.success(request, f"'{target.user_name}' was {verb}.")
    return redirect("user_list")
