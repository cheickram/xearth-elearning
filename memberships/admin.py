from django.contrib import admin
from .models import Membership, SuperUser, Tutor, Learner, TutorMembership, Subscription


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_type', 'stripe_plan_id', 'price')


@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'stripe_customer_id', 'course_list')


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('superuser', 'title', 'study')


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ('superuser',)


@admin.register(TutorMembership)
class TutorMembershipAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'membership')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('tutor_membership', 'stripe_subscription_id', 'active')