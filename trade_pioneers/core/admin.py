from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post, Group, Comment, Like


# Register the CustomUser model with the admin site
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'date_posted', 'group', 'deleted_at')
    search_fields = ('title', 'user__username')  # fields that can be searched
    list_filter = ('date_posted', 'group', 'deleted_at')  # filters on the right side - added 'deleted_at' for easier filtering of deleted posts

     # Step 1: Add the function for undoing the delete
    def undo_delete(modeladmin, request, queryset):
        queryset.update(deleted_at=None)
    undo_delete.short_description = "Undo delete selected posts"

    # Step 2: Add the action to the actions list
    actions = [undo_delete]

admin.site.register(Post, PostAdmin) 

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )
    filter_horizontal = ('users', )

admin.site.register(Group, GroupAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'date_commented', 'deleted_at']  # Fields you want to display in the list view
    search_fields = ['user__username', 'text']  # Fields you want to be able to search by
    list_filter = ['date_commented', 'deleted_at']  # Filters on the right side

    # Step 1: Add the function for undoing the delete
    def undo_delete(self, request, queryset):
        queryset.update(deleted_at=None)

    undo_delete.short_description = "Undo delete selected comments"

    # Step 2: Add the action to the actions list
    actions = [undo_delete]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']  # Adjusted timestamp to created_at
    search_fields = ['user__username']
