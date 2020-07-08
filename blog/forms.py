from django import forms
from .models import Post, Comment, registerCamera


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class CameraForm(forms.ModelForm):

    class Meta:
        model = registerCamera
        fields = {'address', 'pincode', 'state', 'city'}
