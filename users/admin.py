from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # champs pour le formulaire de modification d'un utilisateur
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Informations supplémentaires', {'fields': ('phone_number', 'city', 'profile_picture', 'bio',)}),)
    )

    # champs pour la liste des utilisateurs dans l'admin
    list_display = BaseUserAdmin.list_display + ('phone_number', 'city',)

    # ces machins c'est pour la recherche et les filtres dans l'admin
    search_fields = BaseUserAdmin.search_fields + ('phone_number', 'city',)
    list_filter = BaseUserAdmin.list_filter + ('city',)