from django.contrib import admin

from polls.models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    # 字段排序
    # fields = ['pub_date', 'question_text']
    # 字段集标题
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # 在 Question 后台页面编辑，默认提供2个足够的选项字段
    inlines = [ChoiceInline]
    # 后台选项显示的字段
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # 过滤器
    list_filter = ['pub_date']
    # 以 question_text 字段搜索
    search_fields = ['question_text']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'votes']


# 在后台管理页面注册
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
