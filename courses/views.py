from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect
from .models import *
from shop.models import *
from django.views import View
from django.contrib import messages


class CoursesView(View):
    def get(self, request):
        coursesList = Course.objects.all()
        context = {'courses': coursesList}
        return render(request, 'courses/courses.html', context)

class CoursesSearchView(View):
    def post(self, request):
        searchWord = request.POST.get('courses-search')
        courses = Course.objects.filter(title__contains=searchWord)
        context = {'search': searchWord, 'courses':courses}
        return render(request, 'courses/courses_search.html', context)

class CourseDetailsView(View):
    def setup(self, request, *args, **kwargs):
        self.course_instance = Course.objects.get(id=kwargs['course_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, course_id):
        context = {'course':self.course_instance}
        return render(request, 'courses/course_details.html', context)
    
    def post(self, request, course_id):
        if not request.user.is_authenticated:
            return redirect('accounts:user_login')
        else:
            try:
                order = request.user.orders.get(status="incomplete")
                return redirect('shop:cart')
            except:
                course = self.course_instance
                order = Order.objects.create(student=request.user, courseId=course.id, total=course.price)
                return redirect('shop:cart')
