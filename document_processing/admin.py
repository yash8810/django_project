from django.contrib import admin
from .models import CustomUser, Document, AnalysisResult

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at', 'file_type')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('title', 'user__username')

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('document', 'created_at')