from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from base.constants.novel import DEFAULT_COVER
from base.models import Novel, Chapter
from general.utils.image import process_novel_cover


class NovelCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.update(label_suffix='')
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '请选择'
        self.fields['sub_category'].empty_label = '请选择'

    class Meta:
        model = Novel
        fields = ('name', 'intro', 'category', 'sub_category', 'cover')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 64,
                'minlength': 1,
                'focus': True
            }),
            'intro': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'category': forms.Select(attrs={
                'class': 'form-control selectpicker'
            }),
            'sub_category': forms.Select(attrs={
                'class': 'form-control selectpicker',
                'disabled': True
            })
        }

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if not cover:
            return DEFAULT_COVER
        return cover

    def _post_clean(self):
        super()._post_clean()
        cover = self.cleaned_data.get('cover')
        if isinstance(cover, InMemoryUploadedFile):
            # process and save avatar
            try:
                self.instance.cover = process_novel_cover(cover)
            except Exception:
                raise forms.ValidationError('请上传正确格式的图片')
        return cover


class ChapterUpdateForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ('title', 'content')


class ChapterCreateForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ('title', 'content', 'volume')
