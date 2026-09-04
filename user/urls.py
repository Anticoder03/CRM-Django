from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_home, name="user_home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Customers
    path("customer/", views.customer_list, name="customer_list"),
    path("customer/<int:pk>/edit/", views.customer_update, name="customer_update"),
    path("customer/<int:pk>/delete/", views.customer_delete, name="customer_delete"),

    # Leads
    path("lead/", views.lead_list, name="lead_list"),
    path("lead/<int:pk>/edit/", views.lead_update, name="lead_update"),
    path("lead/<int:pk>/delete/", views.lead_delete, name="lead_delete"),

    # Opportunities
    path("opportunity/", views.opportunity_list, name="opportunity_list"),
    path("opportunity/<int:pk>/edit/", views.opportunity_update, name="opportunity_update"),
    path("opportunity/<int:pk>/delete/", views.opportunity_delete, name="opportunity_delete"),

    # Activities
    path("activity/", views.activity_list, name="activity_list"),
    path("activity/<int:pk>/edit/", views.activity_update, name="activity_update"),
    path("activity/<int:pk>/delete/", views.activity_delete, name="activity_delete"),

    # Tasks
    path("task/", views.task_list, name="task_list"),
    path("task/<int:pk>/edit/", views.task_update, name="task_update"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),

    # Email
    path("email/compose/", views.email_compose, name="email_compose"),
    path("email/bulk/", views.email_bulk, name="email_bulk"),
    path("email/log/", views.email_log, name="email_log"),
]
