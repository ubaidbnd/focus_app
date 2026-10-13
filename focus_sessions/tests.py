from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import TruncDate

from datetime import datetime, time, timedelta

from .models import FocusSession
from accounts.models import UserGoal

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
        self.assertEqual(response.context["total_duration"], '0 min')
        self.assertTemplateUsed(response, "home.html")

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
        self.assertEqual(response.context["total_duration"], '1h 5m')


    def test_only_today_session_is_added(self):
        yesterday = timezone.now() - timedelta(days=1)

        FocusSession.objects.create(
            user=self.user,
            duration_minutes=15,
            session_started=yesterday
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_duration"], '0 min')

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
        self.assertEqual(response.context["total_duration"], '45 min')

class StreakTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="test-password-123",
        )
        UserGoal.objects.create(user=self.user, goal=60)

        self.client.force_login(self.user)
        self.today = timezone.localdate()
        self.url = reverse("home")

    def create_session(self, day, minutes, user=None):
        user = user or self.user
        local_datetime = timezone.make_aware(
            datetime.combine(day, time(12, 0)),
            timezone.get_current_timezone(),
        )
        return FocusSession.objects.create(
            user=user,
            duration_minutes=minutes,
            session_started=local_datetime,
        )

    def get_streak(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        return response.context["streak_count"]

    def test_streak_counts_consecutive_days(self):
        self.create_session(self.today - timedelta(days=1), 60)
        self.create_session(self.today - timedelta(days=2), 75)
        self.create_session(self.today - timedelta(days=3), 60)

        self.assertEqual(self.get_streak(), 3)

    def test_streak_is_zero_when_yesterday_failed(self):
        self.create_session(self.today - timedelta(days=1), 45)
        self.create_session(self.today - timedelta(days=2), 60)

        self.assertEqual(self.get_streak(), 0)

    def test_today_counts_when_goal_is_reached(self):
        self.create_session(self.today, 60)
        self.create_session(self.today - timedelta(days=1), 60)
        self.create_session(self.today - timedelta(days=2), 60)

        self.assertEqual(self.get_streak(), 3)

    def test_missing_day_breaks_streak(self):
        self.create_session(self.today - timedelta(days=1), 60)
        # No session on the day before yesterday.
        self.create_session(self.today - timedelta(days=3), 60)

        self.assertEqual(self.get_streak(), 1)

    def test_no_goal_returns_none(self):
        UserGoal.objects.filter(user=self.user).delete()

        self.create_session(self.today - timedelta(days=1), 60)

        self.assertIsNone(self.get_streak())

    def test_another_users_sessions_do_not_affect_streak(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="test-password-123",
        )

        self.create_session(self.today - timedelta(days=1), 30)
        self.create_session(
            self.today - timedelta(days=2), 120, user=other_user
        )

        self.assertEqual(self.get_streak(), 0)

    def test_session_near_indian_midnight_uses_correct_date(self):
        india_tz = timezone.get_current_timezone()
        today = timezone.localdate()

        session_time = datetime.combine(
            today,
            time(23, 55),
            tzinfo=india_tz,
        )

        session = FocusSession.objects.create(
            user=self.user,
            duration_minutes=60,
            session_started=session_time,
        )

        local_day = (
            FocusSession.objects
            .filter(pk=session.pk)
            .annotate(
                day=TruncDate(
                    "session_started",
                    tzinfo=india_tz,
                )
            )
            .values_list("day", flat=True)
            .get()
        )

        self.assertEqual(local_day, today)

class HistoryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@user.com',
            password='tuse1234'
        )
        self.client.force_login(self.user)
        self.url = reverse("focus_history")

    def test_history_page_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

    def test_user_only_sees_own_sessions(self):
        other_user = User.objects.create_user(
            username='testuser2',
            email='test@2.com',
            password='tuse2123'
        )

        FocusSession.objects.create(
            user = self.user,
            duration_minutes = 30,
            session_started = timezone.now() - timedelta(minutes=40)
        )

        FocusSession.objects.create(
            user = other_user,
            duration_minutes = 45,
            session_started = timezone.now() - timedelta(minutes=60)
        )

        response = self.client.get(self.url)

        grouped_sessions = response.context["grouped_sessions"]

        sessions = [session for sessions in grouped_sessions.values()
                    for session in sessions]

        duration = [session.duration_minutes for session in sessions]

        self.assertEqual(duration, [30])

    def test_date_filter_shows_only_selected_date_sessions(self):
        selected_date = timezone.localdate()
        yesterday = selected_date - timedelta(days=1)

        today_datetime = timezone.make_aware(
            datetime.combine(selected_date, time(12, 0)),
            timezone.get_current_timezone()
        )

        yesterday_datetime = timezone.make_aware(
            datetime.combine(yesterday, time(12, 0)),
            timezone.get_current_timezone()
        )

        today_session = FocusSession.objects.create(
            user=self.user,
            duration_minutes=30,
            session_started=today_datetime
        )
        yesterday_session = FocusSession.objects.create(
            user=self.user,
            duration_minutes=45,
            session_started=yesterday_datetime
        )
        response = self.client.get(self.url,
                                   {"date":selected_date.isoformat()})
        
        grouped_sessions = response.context["grouped_sessions"]

        sessions = [session for sessions in grouped_sessions.values()
                    for session in sessions]

        session_ids = {session.pk for session in sessions}

        self.assertEqual(session_ids, {today_session.pk})

    def test_invalid_date_shows_error(self):
        response = self.client.get(self.url,
                                   {"date":"not-a-date"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["error"])

    def test_select_date_with_no_session(self):
        selected_date = timezone.localdate()

        response = self.client.get(self.url,
                                   {"date":selected_date.isoformat()})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["grouped_sessions"], {})
        self.assertContains(response, "No sessions on this date.")

    def test_history_with_no_sessions(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["grouped_sessions"], {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your focus journey starts here.")

