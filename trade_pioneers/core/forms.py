from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser  # Import the CustomUser model
from .models import Post  
from .models import Comment

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Enter your first name.',
        error_messages={
            'required': 'Please enter your first name.',
            'max_length': 'First name is too long.'
        }
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Enter your last name.',
        error_messages={
            'required': 'Please enter your last name.',
            'max_length': 'Last name is too long.'
        }
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser  # Use your custom user model
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')  # Add your custom fields

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})


#############
# Post Form #
#############

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'group']  # list other fields but exclude the 'user' field

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Add any other fields you want to allow users to edit
