from django import forms
from .models import Wait_task


class Wait_task_form(forms.ModelForm):

    class Meta:
        model = Wait_task
        fields = ('name', 'time_to_wait')
