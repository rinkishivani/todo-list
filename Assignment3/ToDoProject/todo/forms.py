from django import forms
from django.core.exceptions import ValidationError

from .models import ToDoList
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField


class ToDoListForm(forms.ModelForm):
    title = forms.CharField(required=False)
    details = RichTextFormField(required=False)

    class Meta:
        model = ToDoList
        fields = ['title', 'details', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task title'}),
            'details': CKEditorWidget(attrs={'placeholder': 'Task details'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Add your custom validation for the title
        if len(title) == 0:
            raise ValidationError('There must be a valid Title.')
        return title

    def clean_details(self):
        details = self.cleaned_data.get('details')
        # Add your custom validation for details
        if len(details) < 10:
            raise ValidationError('Details must be at least 10 characters long.')
        return details


# class NewTaskForm(forms.ModelForm):
#     title = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Task title'}
#         ),
#         max_length=100,
#         help_text='The max length for title is 100.'
#     )
#     rich_text = forms.RichTextField(
#         widget=forms.Textarea(
#             attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
#         ),
#         max_length=4000,
#         help_text='The max length of the text is 4000.'
#     )
#
#     class Meta:
#         model = ToDoList
#         fields = ['subject', 'message']
