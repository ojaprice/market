from django.contrib import admin
from .models import CustomUser, CompanyInfo

# Register your models here.
@admin.register(CompanyInfo)
class AdminCompany(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    # search_fields = ('name', 'location')
    # list_filter = ('created_at',)  # Add filters

    # To disable add permission 
    # def has_add_permission(self, request, obj=None):
    #     return False
    
    # To disable update permission 
    def has_change_permission(self, request, obj=None):
        return False
    
    # set specific field to diable update 
    readonly_fields = [
        'email'
    ]
    
    # To disable delete permission 
    def has_delete_permission(self, request, obj=None):
        return False
    
    # To disable module from displaying 
    def has_module_permission(self, request, obj=None):
        return False

admin.site.register(CustomUser)
