from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from .models import FocusSession
# Create your views here.

@login_required
def create_focus_session(request):
    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'start':

            duration_minutes = request.POST.get('duration_minutes')

            try:
                duration_minutes = int(duration_minutes)
            except (TypeError, ValueError):
                return JsonResponse({"success":False,
                            "error":"Invalid Duration"
                            }, status=400)
            
            if duration_minutes < 5 or duration_minutes > 240:
                return JsonResponse({"success":False,
                            "error":"Duration must be between 5 and 240 minutes"
                            }, status=400)
            
            request.session['focus_duration'] = duration_minutes
            request.session['focus_start'] = timezone.now().isoformat()

            return JsonResponse({
                'success':True,
                'remaining_duration':duration_minutes
            })

        elif action == 'pause':

            focus_start = request.session.get("focus_start")
            focus_duration = request.session.get("focus_duration")

            if focus_start is None or focus_duration is None:
                return JsonResponse({
                    "success":False,
                    "error":"No active focus session"
                }, status=400)

            focus_start = parse_datetime(focus_start)

            elapsed_minutes = int(
                (timezone.now() - focus_start).total_seconds() / 60)

            if elapsed_minutes >= 1:
                FocusSession.objects.create(
                            user = request.user,
                            duration_minutes = elapsed_minutes,
                            session_started = focus_start
                        )

            remaining_minutes = max(0, focus_duration - elapsed_minutes)

            request.session["focus_duration"] = remaining_minutes
            request.session.pop("focus_start", None)

            return JsonResponse({
                "success":True,
                "elapsed_minutes":elapsed_minutes,
                'remaining_minutes':remaining_minutes
            })

        elif action == 'continue':

            focus_duration = request.session.get("focus_duration")

            if focus_duration is None:
                return JsonResponse({
                    "success":False,
                    "error":"No paused focus session"
                }, status=400)

            if focus_duration <= 0:
                return JsonResponse({
                    "success":False,
                    "error":"No time remaining"
                }, status=400)
            
            request.session['focus_start'] = timezone.now().isoformat()

            return JsonResponse({
                "success":True,
                'remaining_duration':focus_duration
            })

        elif action == 'cancel':

            focus_start = request.session.get("focus_start")

            if focus_start:

                focus_start = parse_datetime(focus_start)
                elapsed_minutes = int((timezone.now() - focus_start).total_seconds()/60)

                if elapsed_minutes >= 1:
                    FocusSession.objects.create(
                                user = request.user,
                                duration_minutes = elapsed_minutes,
                                session_started = focus_start
                            )
                    
            request.session.pop("focus_start", None)
            request.session.pop("focus_duration", None)

            return JsonResponse({
                "success":True,
            })

        elif action == 'complete':

            focus_start = request.session.get("focus_start")
            focus_remaining = request.session.get("focus_duration")

            if focus_start is None or focus_remaining is None:
                return JsonResponse({
                    "success":False,
                    "error":"No active focus session"
                }, status=400)

            focus_start = parse_datetime(focus_start)
            elapsed_minutes = int((timezone.now() - focus_start).total_seconds()/60)

            if focus_remaining > elapsed_minutes:
                return JsonResponse({
                    "success":False,
                    "error":"Focus duration has not benn completed"
                }, status=400)

            final_minutes = min(elapsed_minutes, focus_remaining)
            FocusSession.objects.create(
                user = request.user,
                duration_minutes = final_minutes,
                session_started = focus_start
            )

            request.session.pop("focus_start", None)
            request.session.pop("focus_duration", None)

            return JsonResponse({
                "success":True
            })

        return JsonResponse({
            "success":False,
            "error":"Invalid action"
        }, status=400)
        
    return render(request, "focus_session.html")
            