from django import forms

from base.models import AuthorApplication, AuthorInfo


class AuthorApplicationForm(forms.ModelForm):
    class Meta:
        model = AuthorApplication
        fields = ('pen_name', 'self_intro')

    def clean_pen_name(self):
        pen_name = self.cleaned_data['pen_name']
        author_exists = AuthorInfo.objects.filter(pen_name=pen_name).exists()
        application_exists = AuthorApplication.objects.filter(
                    pen_name=pen_name, status=AuthorApplication.STATUS['unapproved']).exists()
        if author_exists or application_exists:
            raise forms.ValidationError('该笔名已存在', code='pen_name_exists')
        return pen_name
