from django import forms


from rentmeapp.models import ToRent, CATEGORY, Area


# class AreaForm(forms.ModelForm):
#
#     class Meta:
#         model = Area
#         fields = ['city', 'pincode']
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', '')
#         super(AreaForm, self).__init__(*args, **kwargs)


class ToRentForm(forms.ModelForm):

    class Meta:
        model = ToRent
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(ToRentForm, self).__init__(*args, **kwargs)
        #self.fields['user_defined_area'] = forms.ModelChoiceField(queryset=Area.objects.filter(user=user))
