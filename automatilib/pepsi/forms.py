from django import forms


class COLAUserForm(forms.Form):
    email = forms.EmailField()
