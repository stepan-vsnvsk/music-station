from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'email', 'date_of_birth', 'date_joined', 'last_login')
    list_filter = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('username', 'date_of_birth')}),
    )

    search_fields = ('username',)
    ordering = ('date_joined',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
