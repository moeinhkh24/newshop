from django import forms

class AddToCartForm(forms.Form):
    AMOUNT_CHOICE = [(i,str(i)) for i in range(1,30)]

    quantity = forms.TypedChoiceField(choices=AMOUNT_CHOICE,coerce=int)
    inplace = forms.BooleanField(required=False,widget=forms.HiddenInput,initial=True)
    