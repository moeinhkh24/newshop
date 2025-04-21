from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','stars']
        widget ={
            'stars':forms.Select(attrs={'class':'form-control'},choices= Comment.STARS_CHOICES)
        }