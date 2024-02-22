# main/admin.py

from django.contrib import admin
from .models import College, Payment, Sport, Team, ContactMessage, SportInformation, TeamMember, CarouselSlide, Complaint


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'logo_preview')
    search_fields = ('name', 'location')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="max-height: 50px; max-width: 50px;" />'
        return None

    logo_preview.allow_tags = True
    logo_preview.short_description = 'Logo Preview'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('college', 'reference_code', 'amount', 'payment_date')
    search_fields = ('college__name', 'reference_code')
    list_filter = ('payment_date',)

class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('college', 'display_sports')
    search_fields = ('college__name',)
    many_to_many = ('sports',)

    def display_sports(self, obj):
        return ', '.join([sport.name for sport in obj.college.sports.all()])


    display_sports.short_description = 'Sports'
    
# class TeamAdmin(admin.ModelAdmin):
#     filter_horizontal = ('sport',)

admin.site.register(College, CollegeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Team, TeamAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']

admin.site.register(ContactMessage, ContactMessageAdmin)

class SportInformationAdmin(admin.ModelAdmin):
    list_display = ['sport', 'id']
    search_fields = ['sport__name']

admin.site.register(SportInformation, SportInformationAdmin)

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']
    search_fields = ['name', 'role']

admin.site.register(TeamMember, TeamMemberAdmin)

class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'id']
    search_fields = ['alt_text']

admin.site.register(CarouselSlide, CarouselSlideAdmin)

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'category']
    search_fields = ['name', 'college', 'category__name']

admin.site.register(Complaint, ComplaintAdmin)

