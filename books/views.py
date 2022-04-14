from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from django.contrib.auth.decorators import login_required
from authentication.models import User
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator


@login_required()
def home(request):
    stars = [1, 2, 3, 4, 5]
    follow = models.UserFollows.objects.filter(user=request.user)
    followed = [user.followed_user for user in follow]
    followed.append(request.user)
    ticket_user = models.Ticket.objects.filter(user=request.user)
    follow_user = models.Ticket.objects.filter(user__in=followed)
    review = models.Review.objects.filter(Q(user__in=followed) | Q(ticket__in=ticket_user) | Q(ticket__in=follow_user))
    ticket_exclude = [r.ticket.id for r in review]
    tickets = models.Ticket.objects.filter(user__in=followed).exclude(id__in=ticket_exclude)

    tickets_and_reviews = sorted(
        chain(tickets, review),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    paginator = Paginator(tickets_and_reviews, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/home.html', {'page_obj': page_obj, 'post': False,
                                               'stars': stars})


@login_required()
def posts(request):
    stars = [1, 2, 3, 4, 5]
    review = models.Review.objects.filter(user=request.user)
    ticket_exclude = [r.ticket.id for r in review]
    tickets = models.Ticket.objects.filter(user=request.user).exclude(id__in=ticket_exclude)

    tickets_and_reviews = sorted(
        chain(tickets, review),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    paginator = Paginator(tickets_and_reviews, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/posts.html', {'page_obj': page_obj, 'post': True,
                                                'stars': stars, 'edit': True})


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
    context = {'form': form, 'ticket': ticket, 'post': True, 'edit': False}
    return render(request, 'books/create_review.html', context=context)


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


@login_required()
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


@login_required()
def delete_follow(request, followed_user_id):
    followed_user = User.objects.get(id=followed_user_id)
    row = models.UserFollows.objects.filter(Q(user=request.user) & Q(followed_user=followed_user))
    row.delete()
    return redirect('subscribe-page')


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('posts')

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
        'edit': True,
    }
    return render(request, 'books/edit_ticket.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('posts')

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
        'review': review,
        'edit': True,

    }
    return render(request, 'books/edit_review.html', context=context)
