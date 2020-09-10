from django.db import models
from django.conf import settings
from datetime import  datetime
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import stripe

baseUser = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

LANGUAGES = (
    ('en', 'English'),
    ('fr', 'French')
)

PROFESSION = (
    ('prof1', 'prof1'),
    ('prof2', 'prof2'),
    ('prof3', 'prof3'),
)

MEMBERSHIP_CHOICES = (
    ('super_membership', 'Super'),
    ('pro_membership', 'Pro'),
    ('free_membership', 'Free')
)

class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES, default='free_membership', max_length=40)
    price = models.PositiveIntegerField(default=27)
    stripe_plan_id = models.CharField(max_length=60)

    def __str__(self):
        return self.membership_type



class SuperUser(models.Model):
    """
    This class (model) extends the django base user model
    """

    slug = models.SlugField(null=True, blank=True)
    user = models.OneToOneField(
        baseUser, on_delete=models.CASCADE, related_name= '_base_user')
    stripe_customer_id = models.CharField(max_length=60, null=True, blank=True)
    language = models.CharField(
        choices=LANGUAGES, default='en', max_length=10)
    course_list = models.TextField(null=True, blank=True)
    website_url = models.CharField(max_length=100, null=True, blank=True)
    tweeter_url = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.CharField(max_length=100, null=True, blank=True)
    youtube_url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def get_course_list(self):
        return self.course_list


def post_save_superuser_create(sender, instance, created, *args, **kwargs):
    super_user = SuperUser.objects.filter(user= instance.user.pk)
    username = instance.user.username
    gen_slug = username.replace(' ', '-').replace('_', '-').replace("'", "-").replace('.', '-')
    super_user.update(slug=gen_slug)

post_save.connect(post_save_superuser_create, sender=SuperUser)


class Tutor(models.Model):
    superuser = models.OneToOneField(
        SuperUser, on_delete=models.CASCADE, related_name= '_superuser_tutor')
    profile_picture = models.ImageField(
        default='logo.png', upload_to='tutors/%Y%m%d/', blank=True)
    title = models.CharField(max_length=120)
    bio = models.TextField()
    study = models.CharField(
        choices=PROFESSION, default='prof1', max_length=30)

    def __str__(self):
        return self.superuser.user.username


class Learner(models.Model):
    superuser = models.OneToOneField(
        SuperUser, on_delete=models.CASCADE, related_name= '_superuser_learner'
    )
    profile_picture = models.ImageField(
        default='logo.png', upload_to='learners/%Y%m%d/', blank=True)
    
    def __str__(self):
        return self.superuser.user.username


class TutorMembership(models.Model):
    tutor = models.OneToOneField(
        Tutor, on_delete=models.CASCADE, related_name='_tutor')
    membership = models.ForeignKey(
        Membership, 
        on_delete=models.SET_NULL, 
        null=True)

    def __str__(self):
        return self.tutor.superuser.user.username
    

def post_save_tutormembership_create(sender, instance, created, *args, **kwargs):
    tutor_membership, created = TutorMembership.objects.get_or_create(tutor=instance)

    if tutor_membership.tutor.superuser.stripe_customer_id is None or tutor_membership.tutor.superuser.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.superuser.user.email)
        free_membership = Membership.objects.get(membership_type='free_membership')
        tutor_membership.tutor.superuser.stripe_customer_id = new_customer_id['id']
        tutor_membership.membership = free_membership
        tutor_membership.save()
        tutor_membership.tutor.superuser.save()


post_save.connect(post_save_tutormembership_create, sender=Tutor)


class Subscription(models.Model):
    tutor_membership = models.ForeignKey(
        TutorMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=60)
    active = models.BooleanField(default=True)  

    def __str__(self):
        return self.tutor_membership.tutor.superuser.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)