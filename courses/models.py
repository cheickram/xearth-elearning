from django.db import models
from django.urls import reverse

from memberships.models import Membership, Tutor, Learner, SuperUser


LEVEL = (
    ('beginner', 'beginner'),
    ('intermediate', 'intermediate'),
    ('advanced', 'advanced'),
)

CATEGORY = (
    ('development', 'development'),
    ('business', 'business'),
    ('it_software', 'it_software'),
)

RATING = [(i,i) for i in range(1, 6)]

class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    objectives = models.TextField()
    category = models.CharField(
        choices=CATEGORY, default='development', max_length=40)
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    avg_rating = models.PositiveIntegerField(default=0)
    number_of_courses = models.PositiveIntegerField(default=0)
    total_duration = models.FloatField(default=0.0)
    tutor_owner = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})


    @property
    def get_lessons(self):
        return self.lesson_set.all().order_by('position')


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='crs')
    position = models.PositiveIntegerField(default=0)
    video_duration = models.FloatField(default=0.0)
    video_url = models.FileField(upload_to= f'videos/%Y%m%d/',)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('courses:lesson-detail',
                       kwargs={
                           'course_slug': self.course.slug,
                           'lesson_slug': self.slug
                       })


class FeedBack(models.Model):
    message = models.CharField(max_length=255)
    rating = models.IntegerField(
        choices= RATING, default= 1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Comment(models.Model):
    message = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(SuperUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Reply(models.Model):
    message = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(SuperUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Tracking(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    watched = models.FloatField(default=0.0)
    video_duration = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.lesson.title} => {self.learner.superuser.user.username}' 



