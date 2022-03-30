from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from authentication.models import User


@login_required()
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'books/home.html', {'tickets': tickets})


@login_required()
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'books/ticket_create.html', context={'form': form})


@login_required()
def create_review(request, ticket_id):
    form = forms.ReviewForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    return render(request, 'books/create_review.html', context={'form': form, 'ticket': ticket})


@login_required()
def create_review_ticket(request):
    form_review = forms.ReviewForm()
    form_ticket = forms.TicketForm()
    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        if all([form_review.is_valid(), form_ticket.is_valid()]):
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    return render(request, 'books/create_review_ticket.html',
                  context={'form_ticket': form_ticket, 'form_review': form_review})


def subscribe_user(request):
    form = forms.SubscriptionsForm()
    subscriptions = models.UserFollows.objects.filter(user=request.user)
    subscribers = models.UserFollows.objects.filter(followed_user=request.user)

    if request.method == 'POST':
        form = forms.SubscriptionsForm(request.POST)
        if form.is_valid():
            user_follow = models.UserFollows()
            user_follow.user = request.user
            follow = User.objects.filter(username=form.cleaned_data['username'])[0]
            user_follow.followed_user = follow
            user_follow.save()
            return redirect('subscribe-page')
    return render(request, 'books/subscription.html',
                  {'form': form, 'subscriptions': subscriptions, 'subscribers': subscribers})

