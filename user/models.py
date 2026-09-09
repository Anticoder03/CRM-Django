import hashlib
import os
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

    @staticmethod
    def hash_password(raw_password):
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac(
            "sha256", raw_password.encode("utf-8"), salt, 100000
        )
        return salt.hex() + ":" + hashed.hex()

    def check_password(self, raw_password):
        try:
            salt_hex, hash_hex = self.password.split(":")
            salt = bytes.fromhex(salt_hex)
            hashed = hashlib.pbkdf2_hmac(
                "sha256", raw_password.encode("utf-8"), salt, 100000
            )
            return hashed.hex() == hash_hex
        except Exception:
            return False


class Customer(models.Model):
    Status_Choices = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=Status_Choices, default="Active"
    )
    notes = models.TextField(blank=True, null=True)
    assign_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_customers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name


class Lead(models.Model):
    Source_Choices = [
        ("Website", "Website"),
        ("Referral", "Referral"),
        ("Social Media", "Social Media"),
        ("Other", "Other"),
    ]
    Status_Choices = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Qualified", "Qualified"),
        ("Converted", "Converted"),
        ("Lost", "Lost"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    source = models.CharField(
        max_length=20, choices=Source_Choices, default="Website"
    )
    status = models.CharField(
        max_length=20, choices=Status_Choices, default="New"
    )
    assign_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    Stage_Choices = [
        ("Prospecting", "Prospecting"),
        ("Qualified", "Qualified"),
        ("Proposal", "Proposal"),
        ("Negotiation", "Negotiation"),
        ("Won", "Won"),
        ("Lost", "Lost"),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(
        max_length=20, choices=Stage_Choices, default="Prospecting"
    )
    probability = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    expected_close_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    assign_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_opportunities"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Activity(models.Model):
    Type_Choice = [
        ("Call", "Call"),
        ("Email", "Email"),
        ("Meeting", "Meeting"),
        ("Note", "Note"),
        ("Other", "Other"),
    ]
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=Type_Choice, default="Call")
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    assign_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_activities"
    )
    ctreated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Task(models.Model):
    Priority_Choices = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    Status_Choices = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=20, choices=Priority_Choices, default="Medium"
    )
    status = models.CharField(
        max_length=20, choices=Status_Choices, default="Pending"
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    assign_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EmailLog(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    recipient_emails = models.TextField()
    recipient_count = models.PositiveIntegerField(default=0)
    sent_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_bulk = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[("Sent", "Sent"), ("Failed", "Failed")],
        default="Sent",
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
