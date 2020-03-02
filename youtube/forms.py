from django import forms


class YtDownloaderForm(forms.Form):
    url = forms.URLField(widget=forms.TextInput(
        attrs={'size': 100, 'placeholder': 'Copy and paste Youtube Link'}), label=False
    )

    def __init__(self, *args, **kwargs):
        super(YtDownloaderForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['style'] = "height:50px"
