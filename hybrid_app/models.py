from django.db import models
from django.contrib.auth.models import User

class Block(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100)
    order = models.IntegerField(blank=True, null=True)
    next_block_pk = models.IntegerField(blank=True, null=True)
    min_block_order = models.IntegerField(blank=True, null=True)
    max_block_order = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    equation = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

class Student(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    matched = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email

class StudentList(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_lists', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)

class Document(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    min_block_order = models.IntegerField(blank=True, null=True)
    max_block_order = models.IntegerField(blank=True, null=True)
    shared_with = models.ManyToManyField(StudentList)
    copy_of = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Teacher(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    matched = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email
