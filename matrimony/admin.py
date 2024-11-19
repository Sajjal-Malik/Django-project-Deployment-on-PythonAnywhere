from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'name', 'age', 'gender', 'occupation', 'email')
    # Fields to display in the admin list view into links
    list_display_links = ('name', 'email')
    # Enable filters in the list view
    list_filter = ('gender', 'is_married')
    # Fields to be searchable in the admin panel
    search_fields = ('occupation',)

class FatherProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation')
    search_fields = ('name', 'occupation')
    list_filter = ('occupation',)

class HobbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_profiles')
    list_display_links = ('name',)
    def get_profiles(self, obj):
        hobby_followers = ", ".join([profile.name for profile in obj.profiles.all()])
        return hobby_followers

    get_profiles.short_description = "Followers"

admin.site.site_header = 'Matrimony Admin'
admin.site.site_title = 'Matrimony Admin Panel'
admin.site.index_title = 'Welcome to Matrimony Admin'

# Register the customized admin class
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FatherProfile, FatherProfileAdmin)
admin.site.register(Religion)
admin.site.register(Sect)
admin.site.register(Caste)
admin.site.register(Hobby, HobbyAdmin)

# admin.site.register(Profile)