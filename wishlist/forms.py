from django import forms

class NameForm(forms.Form):
    user_nickname = forms.CharField(label="Name:", max_length=200, required=True)