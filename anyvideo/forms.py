from django import forms


class AnyVideoDownloadForm(forms.Form):
    url = forms.URLField(widget=forms.TextInput(
        attrs={'size': 100, 'placeholder': 'Copy and paste Youtube Link'}), label=False
    )

    def __init__(self, *args, **kwargs):
        super(AnyVideoDownloadForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['style'] = "height:50px"
