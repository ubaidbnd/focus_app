from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
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
               )}
    return render(request, "home.html", context)