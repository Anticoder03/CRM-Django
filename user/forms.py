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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_admin:
                customers = Customer.objects.all()
            else:
                customers = Customer.objects.filter(assign_to=user)
            self.fields["customer"].queryset = customers


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_admin:
                customers = Customer.objects.all()
            else:
                customers = Customer.objects.filter(assign_to=user)
            self.fields["recipients"].queryset = customers


def _users_for_assignment():
    return User.objects.filter(is_active=True)


def _visible_customer_qs(user):
    if user is not None and not user.is_admin:
        return Customer.objects.filter(assign_to=user)
    return Customer.objects.all()


def _visible_lead_qs(user):
    if user is not None and not user.is_admin:
        return Lead.objects.filter(assign_to=user)
    return Lead.objects.all()


class AssignableFormMixin:
    def _apply_assignment(self, user):
        if "assign_to" not in self.fields:
            return
        if user is not None and not user.is_admin:
            self.fields.pop("assign_to")
        else:
            self.fields["assign_to"].queryset = _users_for_assignment()


class CustomerForm(AssignableFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "customer_name", "company", "email", "phone",
            "address", "city", "status", "notes", "assign_to",
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
            "assign_to": "Assign To",
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
            "assign_to": forms.Select(attrs={"class": TW_SELECT}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_assignment(user)


class LeadForm(AssignableFormMixin, forms.ModelForm):
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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_assignment(user)


class OpportunityForm(AssignableFormMixin, forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            "title", "customer", "amount", "stage",
            "probability", "expected_close_date", "notes", "assign_to",
        ]
        labels = {
            "title": "Opportunity Title",
            "customer": "Customer",
            "amount": "Amount ($)",
            "stage": "Stage",
            "probability": "Probability (%)",
            "expected_close_date": "Expected Close Date",
            "notes": "Notes",
            "assign_to": "Assign To",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter opportunity title"}),
            "customer": forms.Select(attrs={"class": TW_SELECT}),
            "amount": forms.NumberInput(attrs={"class": TW_INPUT, "placeholder": "Enter amount"}),
            "stage": forms.Select(attrs={"class": TW_SELECT}),
            "probability": forms.NumberInput(attrs={"class": TW_INPUT, "placeholder": "0-100", "min": "0", "max": "100"}),
            "expected_close_date": forms.DateInput(attrs={"class": TW_INPUT, "type": "date"}),
            "notes": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Add notes", "rows": 3}),
            "assign_to": forms.Select(attrs={"class": TW_SELECT}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = _visible_customer_qs(user)
        self._apply_assignment(user)


class ActivityForm(AssignableFormMixin, forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["customer", "lead", "type", "subject", "description", "activity_date", "created_by", "assign_to"]
        labels = {
            "customer": "Customer",
            "lead": "Lead",
            "type": "Activity Type",
            "subject": "Subject",
            "description": "Description",
            "activity_date": "Activity Date & Time",
            "created_by": "Created By",
            "assign_to": "Assign To",
        }
        widgets = {
            "customer": forms.Select(attrs={"class": TW_SELECT}),
            "lead": forms.Select(attrs={"class": TW_SELECT}),
            "type": forms.Select(attrs={"class": TW_SELECT}),
            "subject": forms.TextInput(attrs={"class": TW_INPUT, "placeholder": "Enter subject"}),
            "description": forms.Textarea(attrs={"class": TW_TEXTAREA, "placeholder": "Enter description", "rows": 3}),
            "activity_date": forms.DateTimeInput(attrs={"class": TW_INPUT, "type": "datetime-local"}),
            "created_by": forms.Select(attrs={"class": TW_SELECT}),
            "assign_to": forms.Select(attrs={"class": TW_SELECT}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not user.is_admin:
            if "created_by" in self.fields:
                self.fields.pop("created_by")
            self.fields["customer"].queryset = _visible_customer_qs(user)
            self.fields["lead"].queryset = _visible_lead_qs(user)
        self._apply_assignment(user)


class TaskForm(AssignableFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "customer", "lead", "due_date", "priority", "status", "description", "created_by", "assign_to"]
        labels = {
            "title": "Task Title",
            "customer": "Customer",
            "lead": "Lead",
            "due_date": "Due Date",
            "priority": "Priority",
            "status": "Status",
            "description": "Description",
            "created_by": "Created By",
            "assign_to": "Assign To",
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
            "assign_to": forms.Select(attrs={"class": TW_SELECT}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not user.is_admin:
            if "created_by" in self.fields:
                self.fields.pop("created_by")
            self.fields["customer"].queryset = _visible_customer_qs(user)
            self.fields["lead"].queryset = _visible_lead_qs(user)
        self._apply_assignment(user)
