from django import forms
from django.forms import ModelForm
from .models import Comment

#! form
class EmailPostForm(forms.Form): 
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea) #? opcjonalne pole

#! models form#! models form
class CommentForm(ModelForm):
    # fields = "__all__"
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        # ? list = ModelName.objects.exclude(PassArguments)


    