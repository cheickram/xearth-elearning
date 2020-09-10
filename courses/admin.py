from django.contrib import admin
from .models import Course, Lesson, FeedBack, Comment, Reply, Tracking


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'title', 'description', 'price', 'discount', 'avg_rating',
        'number_of_courses', 'total_duration', 'tutor_owner',
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'course', 'position', 'video_duration')


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('message', 'rating', 'course', 'learner')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'lesson', 'user',)
    

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('message', 'comment', 'user',)


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'learner', 'watched', 'video_duration')
