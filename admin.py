from django.contrib import admin
from myHome.models import MY_HOME
# Register your models here.

class viewAdmin(admin.ModelAdmin):
	list_display = ('userID','studentNum','name','major','announcement','subject','resource','createDate')
admin.site.register(MY_HOME, viewAdmin)