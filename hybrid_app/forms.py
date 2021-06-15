from django.forms import ModelForm
from . import models

class StudentListForm(ModelForm):
    class Meta:
        model = models.StudentList
        fields = ['name', 'students']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(StudentListForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = models.Student.objects.filter(user=self.user)
