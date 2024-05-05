from django.db import models
from django.urls import reverse

# Create your models here.
class Skill(models.Model):

    name = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/skills/')
    slug = models.SlugField(null=True, blank=True, max_length=300, unique=True, allow_unicode=True)

    def get_absolute_url(self):
        return reverse('skills:skill_details', args=(self.id, self.slug))