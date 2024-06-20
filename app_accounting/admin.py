from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app_accounting.models import (
    User,
    Education,
    Experience,
    Task,
    Skill,
    Language,
    Course,
    Social,
)
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class SocialInline(admin.TabularInline):
    model = Social
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0


class CourseInline(admin.TabularInline):
    model = Course
    extra = 0


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": (
                "avatar",
                ("first_name", "last_name"),
                "email",
                "about",
            )
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    inlines = [
        SocialInline,
        ExperienceInline,
        SkillInline,
        LanguageInline,
        CourseInline,
    ]


class AbstractCVAdmin(admin.ModelAdmin):
    exclude = ['user']
    
    def get_queryset(self, request):
        current_user = request.user
        qs = super().get_queryset(request)
        return qs.filter(user=current_user)


    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

class CourseAdmin(AbstractCVAdmin):
    pass


class CompanyFilter(SimpleListFilter):
    title = 'company' # or use _('company') for translated title
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        # BAD
        # company_list = set([t.experience.company for t in model_admin.model.objects.filter(experience__user=request.user)])
        
        # BAD
        # company_list = [e.company for e in request.user.experiences.all()]
        
        return [(c, c) for c in request.user.experiences.values_list('company', flat=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(experience__company=self.value())


class TaskAdmin(admin.ModelAdmin):
    list_filter = [CompanyFilter, 'experience__company', 'experience__start_date', 'experience__end_date']
    search_fields = ['description', 'experience__company']
    list_display = ['description', 'get_company_name']

    def get_company_name(self, obj):
        return obj.experience.company

    get_company_name.short_description = 'Company Name'

    def get_queryset(self, request):
        current_user = request.user
        qs = super().get_queryset(request)
        return qs.filter(experience__user=current_user)
    
    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['experience'].queryset = request.user.experiences.all()
        return form



class ExperienceAdmin(AbstractCVAdmin):
    inlines = [TaskInline]


admin.site.register(User, UserAdmin)
admin.site.register(Education, AbstractCVAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Skill, AbstractCVAdmin)
admin.site.register(Language, AbstractCVAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Social, AbstractCVAdmin)