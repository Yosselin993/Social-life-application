from django_summernote.fields import SummernoteTextFormField

class SafeSummernoteField(SummernoteTextFormField):
    def to_python(self, value):
        return value  # bypass bleach completely
