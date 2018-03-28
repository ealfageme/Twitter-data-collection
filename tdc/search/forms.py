from django import forms


class hastag(forms.Form):
    has = forms.CharField(required = True, label='')
