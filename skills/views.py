from django.shortcuts import render
from django.views import View
from . import models

# Create your views here.
class SkillsView(View):
    def setup(self, request, *args, **kwargs):
        # gets a particular teacher time
        self.skills_instance = models.Skill.objects.all()
        super().setup(request, *args, **kwargs)

    def get(self, request):
        context = {'skills': self.skills_instance}
        return render(request, 'skills/skills_home.html', context)
    
class SkillDetailsView(View):

    def setup(self, request, *args, **kwargs):
        # gets a particular teacher time
        self.skill_instance = models.Skill.objects.get(slug=kwargs['skill_slug'])

        super().setup(request, *args, **kwargs)

    def get(self, request, skill_id, skill_slug):
        context = {'skill':self.skill_instance}
        return render(request, 'skills/skill_details.html', context)