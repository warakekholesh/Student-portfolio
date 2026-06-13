from django.contrib import admin

# Register your models here.
from .models import Resume
admin.site.register(Resume)
from .models import UserProfile
admin.site.register(UserProfile)
from .models import ConnectionRequest
admin.site.register(ConnectionRequest)