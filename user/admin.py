from django.contrib import admin

from user.models import Customer, Lead, Opportunity, User, Activity, Task, EmailLog

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Lead)
admin.site.register(Opportunity)
admin.site.register(Activity)
admin.site.register(Task)
admin.site.register(EmailLog)
