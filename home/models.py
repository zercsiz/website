from django.db import models


languages = [
    ('e', 'English'),
    ('g', 'German')
]


class Course(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(verbose_name="Start Date")
    days = models.CharField(max_length=200)
    hour = models.CharField(max_length=200)
    language = models.CharField(max_length=1, choices=languages)
    mamad = models.CharField(max_length=250,blank=True, null=True)

    def __str__(self):
        return f"{self.title} | Language:{self.language} | Start Date:{self.start_date} | {self.description[:60]}... | Days:{self.created} | Hour:{self.edited}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

