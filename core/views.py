from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncDate
from focus_sessions.models import FocusSession

def format_duration(duration):
    if duration<60:
        return f"{duration} min"
    h = duration//60
    m = duration%60
    if m == 0:
        return f"{h}h"
    return f"{h}h {m}m"

@login_required
def home(request):
    
    total_duration = FocusSession.objects.filter(user=request.user,
        session_started__date=timezone.localdate()
        ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    user_goal = getattr(request.user, 'usergoal', None)
    goal_duration = user_goal.goal if user_goal else None

    streak_count = None

    if goal_duration:

        today = timezone.localdate()

        if total_duration >= goal_duration:
            start_date = today
        else:
            start_date = today - timedelta(days=1)

        daily_totals = FocusSession.objects.filter(
                user=request.user).annotate(
                    day=TruncDate("session_started",
                    tzinfo=timezone.get_current_timezone(),)).values("day").annotate(
                    total=Sum("duration_minutes"))

        streak_dict = {
            item["day"]: item["total"]
            for item in daily_totals
        }

        streak_count = 0

        while (
            start_date in streak_dict and
            streak_dict[start_date] >= goal_duration
        ):
            streak_count += 1 
            start_date = start_date - timedelta(days=1)

    remaining_duration = max(
        goal_duration - total_duration, 0) if goal_duration else None

    progress = min(total_duration/goal_duration*100,
                   100) if goal_duration else None

    context = {"total_duration":format_duration(total_duration),
               "goal_duration":(format_duration(goal_duration)
                    if goal_duration else None),
               "remaining_duration":(format_duration(remaining_duration)
                    if remaining_duration else None),
               "progress":progress,
               "goal_complete":(
                   total_duration>=goal_duration if goal_duration
                   else None
               ),
               "streak_count":streak_count}
    return render(request, "home.html", context)