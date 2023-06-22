from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.utils.translation import gettext


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50)

    class Meta:
        model = Post
        fields = ["author", "category", "title", "text", "rating"]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        # type = cleaned_data.get("type")

        if title == text:
            raise ValidationError(gettext("Title and text should be different."))

        return cleaned_data
