from django.contrib import admin
from leads.models import User, Agent, Lead, UserProfile
from leads.models import Category

admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(UserProfile)
admin.site.register(Category)

