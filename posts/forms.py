from django import forms
from .models import Post

class AddQuestionForm(forms.Form):
    question = forms.CharField(
        label='Ask something', max_length=100, widget=forms.Textarea(
        attrs={'rows': 4}))
    choice_text_1 = forms.CharField(
        label='Provide some choices #1', max_length=100, widget=forms.Textarea(
        attrs={'rows': 1}))
    choice_text_2 = forms.CharField(
        label='Provide choice #2', max_length=100, widget=forms.Textarea(
        attrs={'rows': 1}))
    choice_text_3 = forms.CharField(
        label='Provide choice #3', max_length=100, widget=forms.Textarea(
            attrs={'rows': 1}),required=False,\
            help_text='Two choices might be enough')

class AddPostForm(forms.Form):
    body = forms.CharField(label='Enter a text:', max_length=450,\
        widget=forms.Textarea(attrs={'rows': 3}))


class EditPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5}), label='Enter a text:')
    class Meta:
        model = Post    
        fields = (
            'body',            
        )
        