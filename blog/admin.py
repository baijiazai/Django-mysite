from django.contrib import admin

from blog.models import User, Person, Exponent, Topic, ChoiceText, ChoiceImage, ChoiceFile, Comment


class PersonInline(admin.StackedInline):
    model = Person
    extra = 1


class ExponentInline(admin.StackedInline):
    model = Exponent
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = [PersonInline, ExponentInline]
    list_display = ('username', 'password', 'email', 'status', 'active')
    list_filter = ['status', 'active']
    search_fields = ['username']


class PersonAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'name', 'sex', 'birthday', 'job', 'education')
    list_filter = ['sex', 'job', 'education']
    search_fields = ['nickname', 'name']


class ExponentAdmin(admin.ModelAdmin):
    list_display = ('fans_num', 'concern_num', 'publish_num', 'reply_num', 'zan_num', 'view_num')


class ChoiceTextInline(admin.TabularInline):
    model = ChoiceText
    extra = 1


class ChoiceImageInline(admin.TabularInline):
    model = ChoiceImage
    extra = 1


class ChoiceFileInline(admin.TabularInline):
    model = ChoiceFile
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    inlines = [ChoiceTextInline, ChoiceImageInline, ChoiceFileInline]
    list_display = ('title', 'reply_num', 'view_num', 'pub_time', 'big_class', 'type')
    list_filter = ['pub_time', 'big_class', 'type']
    search_fields = ['title']


class ChoiceTextAdmin(admin.ModelAdmin):
    list_display = ('text', 'vote')
    search_fields = ['text']


class ChoiceImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'vote')
    search_fields = ['image']


class ChoiceFileAdmin(admin.ModelAdmin):
    list_display = ('audio', 'vote')
    search_fields = ['audio']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'rep_time', 'zan_num')
    list_filter = ['rep_time']
    search_fields = ['content']


admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Exponent, ExponentAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(ChoiceText, ChoiceTextAdmin)
admin.site.register(ChoiceImage, ChoiceImageAdmin)
admin.site.register(ChoiceFile, ChoiceFileAdmin)
admin.site.register(Comment, CommentAdmin)
