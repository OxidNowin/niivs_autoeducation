from django.contrib import admin
from quiz.models import *

admin.site.register(Poll)
admin.site.register(Answer)
admin.site.register(Question)