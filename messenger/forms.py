from django import forms

class NewMessageForm(forms.Form):
    receiver = forms.CharField(max_length=30)
    
    text = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    # source = forms.CharField(       # A hidden input for internal use
    #     max_length=50,              # tell from which page the user sent the message
    #     widget=forms.HiddenInput()
    # )

    def clean(self):
        cleaned_data = super(NewMessageForm, self).clean()
        receiver = cleaned_data.get('receiver')
        text = cleaned_data.get('text')
        if not receiver and not text:
            raise forms.ValidationError('You have to write something!')