from django import forms

from .models import Recipe, MyCalender


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = ('user', 'pub', 'name', 'ingredient', 'weight', 'recipe', 'hyojiweight', 'hyojiryo')


class CalenderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = MyCalender
        fields = ('date',)
        labels = {'date': "日付"}
        widgets = {
            'date': forms.SelectDateWidget
        }
