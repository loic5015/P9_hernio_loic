from django import forms
from .models import Ticket, Review



class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    CHOICES = (('0', 0), ('1', 1),  ('2', 2), ('3', 3), ('4', 4), ('5', 5))
    rating = forms.ChoiceField(choices=CHOICES, label='Note',
                               widget=forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}))
    headline = forms.CharField(label='Titre')
    body = forms.CharField(label='commentaire', widget=forms.Textarea)

    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class SubscriptionsForm(forms.Form):
    username = forms.CharField(max_length=128)


