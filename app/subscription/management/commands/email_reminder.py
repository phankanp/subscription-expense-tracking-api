from datetime import timedelta, datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand

from subscription.models import Subscription


class Command(BaseCommand):
    help = "Send subscription reminder"

    def check_subscriptions(self, upcoming_subscriptions):
        """
        Checks and maps upcoming subscriptions by user
        """
        subscriptions = {}

        for sub in upcoming_subscriptions:
            subscriptions[sub.created_by.email] = (
                subscriptions.get(sub.created_by.email, "")
                + f"Your {sub.title} will be renewed on {sub.start_date} \n"
            )

        return subscriptions

    def update_subscription_date(self, upcoming_subscriptions):
        """
        Updates subscription date for subscriptions that are two days away
        """
        for sub in upcoming_subscriptions:
            next_renew_date = sub.start_date + timedelta(days=sub.renewal_cycle_days)
            sub.start_date = next_renew_date

            sub.save()

    def handle(self, *args, **options):
        """
        Sends email to each user with upcoming subscription payments
        """

        date_now = datetime.now()
        date_one_week = date_now + timedelta(weeks=1)
        date_two_days = date_now + timedelta(days=2)
        subscriptions_week_away = Subscription.objects.filter(start_date=date_one_week)
        subscriptions_two_days_away = Subscription.objects.filter(
            start_date=date_two_days
        )

        subs_week_away = self.check_subscriptions(subscriptions_week_away)

        for email in subs_week_away.keys():
            message = "Upcoming payment dates: \n" + subs_week_away[email]

            subject = "Upcoming subscription renewals in one week!"

            send_mail(subject, message, "noreply@email.com", [email])

            self.stdout.write("E-mail Report was sent.")

        subs_two_days_away = self.check_subscriptions(subscriptions_two_days_away)

        self.update_subscription_date(subscriptions_two_days_away)

        for email in subs_two_days_away.keys():
            message = "Upcoming payment dates: \n" + subs_two_days_away[email]

            subject = "REMINDER!!! Upcoming subscription renewals in two days!"

            send_mail(subject, message, "noreply@email.com", [email])

            self.stdout.write("E-mail Report was sent.")
