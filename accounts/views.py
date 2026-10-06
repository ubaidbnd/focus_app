from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserGoalForm
from django.views import generic
from django.views.decorators.http import require_POST
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

class SignUp(generic.CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def set_goal(request):

    user_goal_instance = getattr(request.user, 'usergoal', None)

    if request.method == 'POST':
        form = UserGoalForm(request.POST, instance=user_goal_instance)

        if form.is_valid():
            goal_obj = form.save(commit=False)
            goal_obj.user = request.user
            goal_obj.save()
            return redirect('home')
        
    else:
        form = UserGoalForm(instance=user_goal_instance)
       
    context = {
        'form':form
    }
    return render(request, 'manage_goal.html', context)

@login_required
@require_POST
def remove_goal(request):
    goal_instance = getattr(request.user, 'usergoal', None)

    print(goal_instance)

    if goal_instance:
        goal_instance.delete()

    return redirect('home')



    
# class SetGoal(LoginRequiredMixin, generic.CreateView):
#     model = UserGoal
#     fields = ["goal",]
#     success_url = reverse_lazy("home")
#     template_name = "set_goal.html"

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    

