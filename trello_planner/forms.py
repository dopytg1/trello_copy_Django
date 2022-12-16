from django import forms

from .models import Board

class AddBoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('title', 'background')

        

