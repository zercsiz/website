from django.shortcuts import render
from courses.models import Course
from accounts.models import Account
from django.views import View


def home_view(request):
    teacher_list = Account.objects.filter(is_teacher=True).exclude(slug__exact="")[:6]
    course_list = Course.objects.all()[:6]
    context = {'courses': course_list, "teachers": teacher_list}
    return render(request, 'home/home.html', context)


class PaletteView(View):
    def get(self, request):
        return render(request, 'home/palette.html')
