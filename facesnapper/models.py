from django.db import models

# Create your models here.
class StudentClass(models.Model):
    tag = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.tag


class Student(models.Model):
    photo = models.ImageField(upload_to='students/', null=True, blank=True)
    name = models.CharField(max_length=100)
    class_category = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    captured = models.BooleanField(default=False)
    adm_no = models.CharField(max_length=33, null=True, blank=True)

    def __str__(self):
        return self.name