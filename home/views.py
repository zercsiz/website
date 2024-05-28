from django.shortcuts import render
from courses.models import Course
from django.views import View
from skills.models import Skill


class HomeView(View):

    def setup(self, request, *args, **kwargs):
        self.courseListInstance = Course.objects.all()[:6]
        self.skillsListInstance = Skill.objects.all()[:3]
        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        context = {'courses': self.courseListInstance, 'skills': self.skillsListInstance}

        return render(request, 'home/home.html', context)
    