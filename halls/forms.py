from django import forms

from halls.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'url', 'youtube_id']
        labels = { 'youtube_id': 'YouTube ID' }


class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label="Search the Video")