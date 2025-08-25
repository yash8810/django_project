from django.db import models
from django.conf import settings


class PlanModel(models.Model):
    plan_name = models.CharField(max_length=50, unique=True)
    plan_description = models.TextField()
    plan_price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 99999.99
    plan_token = models.IntegerField(help_text="Message token limit for the plan")
    plan_word_token = models.IntegerField(help_text="Word token limit for the plan")

    class Meta:
        db_table = 'planstb'

    def __str__(self):
        return self.plan_name


class SubscriptionModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanModel, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    remaining_token = models.IntegerField()
    remaining_word_token = models.IntegerField()

    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    card_expiry_month = models.IntegerField(blank=True, null=True)
    card_expiry_year = models.IntegerField(blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subscriptiontb'

    def __str__(self):
        return f"{self.user.email} - {self.plan.plan_name}"