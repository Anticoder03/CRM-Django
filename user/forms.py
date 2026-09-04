from django import forms
from .models import Customer, Lead, Opportunity, Activity, Task, User

TW_INPUT = "w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-900 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
TW_SELECT = "w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-900 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
TW_TEXTAREA = "w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-900 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200 resize-vertical"


class EmailForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label="Send To (Customer)",
        required=True,
        widget=forms.Select(attrs={"class": TW_SELECT}),
    )
    subject = forms.CharField(
        label="Subject",
        required=True,
        widget=forms.TextInput(
            attrs={"class": TW_INPUT, "placeholder": "Enter email subject"}
        ),
    )
    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": TW_TEXTAREA,
                "rows": 6,
                "placeholder": "Write your email message here...",
            }
        ),
    )


class BulkEmailForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.all(),
        label="Select Recipients (Customers)",
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": TW_SELECT,
                "size": "8",
            }
        ),
    )
    include_leads = forms.BooleanField(
        label="Also include all Leads?",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "w-4 h-4 text-indigo-600"}),
    )
    subject = forms.CharField(
        label="Subject",
        required=True,
        widget=forms.TextInput(
            attrs={"class": TW_INPUT, "placeholder": "Enter email subject"}
        ),
    )
    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": TW_TEXTAREA,
                "rows": 6,
                "placeholder": "Write your bulk email message here...",
            }
        ),
    )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "customer_name", "company", "email", "phone",
            "address", "city", "status", "notes",
        ]
        labels = {
            "customer_name": "Customer Name",
            "company": "Company",
            "email": "Email Address",
            "phone": "Phone Number",
            "address": "Address",
            "city": "City",
            "status": "Status",
            "notes": "Notes",
        }
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter customer name"}),
            "company": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter company name"}),
            "email": forms.EmailInput(attrs={"class": TW_INPUT, "placeholder": "Enter email address"}),
            "phone": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter phone number"}),
            "address": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Enter address", "rows": 3}),
            "city": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter city"}),
            "status": forms.Select(attrs={"class": TW_SELECT}),
            "notes": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Add notes", "rows": 3}),
        }


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "company", "email", "phone", "source", "status", "assign_to", "notes"]
        labels = {
            "name": "Lead Name",
            "company": "Company",
            "email": "Email Address",
            "phone": "Phone Number",
            "source": "Lead Source",
            "status": "Status",
            "assign_to": "Assign To",
            "notes": "Notes",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter lead name"}),
            "company": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter company name"}),
            "email": forms.EmailInput(attrs={"class": TW_INPUT, "placeholder": "Enter email address"}),
            "phone": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter phone number"}),
            "source": forms.Select(attrs={"class": TW_SELECT}),
            "status": forms.Select(attrs={"class": TW_SELECT}),
            "assign_to": forms.Select(attrs={"class": TW_SELECT}),
            "notes": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Add notes", "rows": 3}),
        }


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            "title", "customer", "amount", "stage",
            "probability", "expected_close_date", "notes",
        ]
        labels = {
            "title": "Opportunity Title",
            "customer": "Customer",
            "amount": "Amount ($)",
            "stage": "Stage",
            "probability": "Probability (%)",
            "expected_close_date": "Expected Close Date",
            "notes": "Notes",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter opportunity title"}),
            "customer": forms.Select(attrs={"class": TW_SELECT}),
            "amount": forms.NumberInput(attrs={"class": TW_INPUT, "placeholder": "Enter amount"}),
            "stage": forms.Select(attrs={"class": TW_SELECT}),
            "probability": forms.NumberInput(attrs={"class": TW_INPUT, "placeholder": "0-100", "min": "0", "max": "100"}),
            "expected_close_date": forms.DateInput(attrs={"class": TW_INPUT, "type": "date"}),
            "notes": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Add notes", "rows": 3}),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["customer", "lead", "type", "subject", "description", "activity_date", "created_by"]
        labels = {
            "customer": "Customer",
            "lead": "Lead",
            "type": "Activity Type",
            "subject": "Subject",
            "description": "Description",
            "activity_date": "Activity Date & Time",
            "created_by": "Created By",
        }
        widgets = {
            "customer": forms.Select(attrs={"class": TW_SELECT}),
            "lead": forms.Select(attrs={"class": TW_SELECT}),
            "type": forms.Select(attrs={"class": TW_SELECT}),
            "subject": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter subject"}),
            "description": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Enter description", "rows": 3}),
            "activity_date": forms.DateTimeInput(attrs={"class": TW_INPUT, "type": "datetime-local"}),
            "created_by": forms.Select(attrs={"class": TW_SELECT}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "customer", "lead", "due_date", "priority", "status", "description", "created_by"]
        labels = {
            "title": "Task Title",
            "customer": "Customer",
            "lead": "Lead",
            "due_date": "Due Date",
            "priority": "Priority",
            "status": "Status",
            "description": "Description",
            "created_by": "Created By",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter task title"}),
            "customer": forms.Select(attrs={"class": TW_SELECT}),
            "lead": forms.Select(attrs={"class": TW_SELECT}),
            "due_date": forms.DateInput(attrs={"class": TW_INPUT, "type": "date"}),
            "priority": forms.Select(attrs={"class": TW_SELECT}),
            "status": forms.Select(attrs={"class": TW_SELECT}),
            "description": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Enter description", "rows": 3}),
            "created_by": forms.Select(attrs={"class": TW_SELECT}),
        }
