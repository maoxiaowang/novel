from django import forms

from base.constants.novel import DEFAULT_COVER
from base.models import Novel


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
