from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

from .models import FocusSession
User = get_user_model()

class HomeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@user.com",
            password="tuse@123"
        )
        self.client.login(
            email="test@user.com",
            password="tuse@123"
        )

    def test_home_shows_zero_when_no_session(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_duration"], 0)
        self.assertTemplateUsed("home.html")

    def test_home_sums_today_focus_session(self):
        now = timezone.now()

        FocusSession.objects.create(
            user = self.user,
            duration_minutes = 25,
            session_started = now - timedelta(minutes=30)
        )

        FocusSession.objects.create(
            user = self.user,
            duration_minutes = 40,
            session_started = now - timedelta(minutes=45)
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_duration"], 65)


    def test_only_today_session_is_added(self):
        yesterday = timezone.now() - timedelta(days=1)

        FocusSession.objects.create(
            user=self.user,
            duration_minutes=15,
            session_started=yesterday
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_duration"], 0)

    def test_home_only_count_logged_in_users_session(self):
        other_user = User.objects.create_user(
            username="testuser2",
            email="test@user2.com",
            password="tuse2@123"
        )
        now = timezone.now()

        FocusSession.objects.create(
            user=other_user,
            duration_minutes=30,
            session_started=now
        )
        FocusSession.objects.create(
            user=self.user,
            duration_minutes=45,
            session_started=now
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_duration"], 45)