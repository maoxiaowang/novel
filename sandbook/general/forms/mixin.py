

class FormValidationMixin:
    """
    non_field_replacement must be a field name
    """
    non_field_replacement = None

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Append css class to every field that contains errors.
        for field in form.errors:
            if field == '__all__':
                if self.non_field_replacement:
                    field = self.non_field_replacement
                else:
                    continue
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super().form_invalid(form)
