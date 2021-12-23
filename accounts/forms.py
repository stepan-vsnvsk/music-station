from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Message
from .utils import resize_uploaded_image


class CustomUserCreationForm(UserCreationForm):
    # using django auth.forms for creating new users     
    IMAGE_WIDTH = 128
    IMAGE_HEIGHT = 128    

    def __init__(self, *args, **kwargs):        
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # help_text customizing
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self['date_of_birth'].help_text = '* It\'s really doesn\'t matter'

    def clean_avatar(self):
        # resize avatar
        image_uploaded = self.cleaned_data.get('avatar')
        image_resized = resize_uploaded_image(
            image_uploaded, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        return image_resized  

    class Meta(UserCreationForm):
        model = CustomUser
        # add fields for user's input
        fields = UserCreationForm.Meta.fields + ('email', 'date_of_birth', 'avatar')
        widgets = {
        # date widget
        'date_of_birth': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control',
         'placeholder':'Select a date', 'type':'date'}),
        }
              

class CustomUserChangeForm(UserChangeForm):
    IMAGE_WIDTH = 128
    IMAGE_HEIGHT = 128
    password = None # exclude password      

    class Meta:        
        model = CustomUser
        # add fields
        fields = ('username', 'email', 'avatar')   

    def clean_avatar(self):
        # resize avatar
        return CustomUserCreationForm.clean_avatar(self)


class EmptyForm(forms.Form):
    """
    for things that should be implemented as POST request
    """
    pass


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = ('body', )
        widgets = {
        'body': forms.Textarea(attrs={'rows': 4})
        }
        labels = {
            'body': 'Say something'
        }