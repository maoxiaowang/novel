from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from base.constants.novel import DEFAULT_COVER
from base.models import Novel, Chapter
from base.models.novel import Volume, NovelComment
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
                'class': 'form-control select select-primary'
            }),
            'sub_category': forms.Select(attrs={
                'class': 'form-control select select-primary',
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
        fields = ('title', 'content', 'status')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入标题',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'focus': True,
                'required': True,
                'placeholder': '请输入内容……'
            }),
            'status': forms.NumberInput(attrs={'hidden': True})
        }

    def clean_status(self):
        saved, submitted = Chapter.STATUS['saved'], Chapter.STATUS['submitted']
        status = self.cleaned_data.get('status')
        if self.instance.status == saved:
            # can be changed to submitted
            if status in (saved, submitted):
                return status
        elif self.instance.status == submitted:
            return submitted
        raise forms.ValidationError('Wrong status', code='wrong_status')

    def clean_content(self):
        content = self.cleaned_data['content']
        paragraph_lines = ['　　' + line.strip() for line in filter(lambda x: x.strip(), content.splitlines())]
        return '\n'.join(paragraph_lines)


class ChapterCreateForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ('title', 'content', 'volume')

    def clean_title(self):
        return '新章节'

    def clean_content(self):
        return ''


class VolumeCreateForm(forms.ModelForm):

    class Meta:
        model = Volume
        fields = ('novel', 'name')

    def clean_name(self):
        return '新卷'


class NovelCommentCreateForm(forms.ModelForm):

    class Meta:
        model = NovelComment
        fields = ('title', 'content')
