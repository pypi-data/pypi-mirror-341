from django.contrib import admin

from .models import Question, Choice


# Register your models here.
class ChoiceInline(admin.TabularInline):
    # 表示要内联的模型是Choice
    model = Choice
    # 指定默认显示 3 个空的 Choice 表单，供用户填写。
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("问题", {"fields": ["question"]}),
        # "classes": ["collapse"] 表示该分组默认是折叠的，用户需要点击展开才能看到内容。
        ("时间", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]

    inlines = [ChoiceInline]
    list_display = ["question", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]

    # 自定义Published recently列排序
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self, obj):
        """检查问题是否在一天之内发布"""
        return obj.was_published_recently()


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
