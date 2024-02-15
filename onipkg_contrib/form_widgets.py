from django import forms
from django.utils.html import format_html


class DisablePopulatedText(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        if value is None:
            return super().render(name, value, attrs, renderer)
        # Just return the value, as normal read_only fields do
        # Add Hidden Input otherwise the old fields are still required
        HiddenInput = forms.HiddenInput()
        return format_html("{}\n" + HiddenInput.render(name, value), self.format_value(value))

class Select2ForFormsetField(forms.CharField):
    pass
