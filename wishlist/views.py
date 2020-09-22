"""
defines the methods for reacting to the defined urls
"""
import random
import string
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings

from wishlist.models import Wish

from .forms import NameForm


def index(request, nospoiler=False):
    if (nospoiler):
        wish_list = Wish.objects.order_by('-importance')
    else:
        wish_list = Wish.objects.order_by('bought', '-importance')
    context = {
        'wish_list': wish_list,
        'ownertext': settings.WISHLIST_OWNER_S,
        'titletext': settings.WISHLIST_TITLE,
        'nospoiler': nospoiler,
    }
    return render(request, 'wishlist/index.html', context)


def bought(request, secret):
    wish = get_object_or_404(Wish, unbuy_string=secret)
    context = {
        'wish': wish,
        'ownertext': settings.WISHLIST_OWNER_S,
        'titletext': settings.WISHLIST_TITLE,
        'base_url': settings.WISHLIST_URL,
    }
    return render(request, 'wishlist/bought.html', context)


def buy(request, wish_id):
    # TODO: Check if usernick valid
    if request.POST['user_nickname'].strip()=="":
        return HttpResponseBadRequest()
    wish = get_object_or_404(Wish, pk=wish_id)
    if not wish.bought:
        wish.bought = True
        wish.santa_nick = request.POST['user_nickname']
        wish.unbuy_string = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=20))
        wish.save()
        return HttpResponseRedirect(reverse('bought', args=(wish.unbuy_string,)))
    else:
        return HttpResponseRedirect('/buyerror')

def nick_entry(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    # wish.santa_nick = "Test"
    # wish.save()
    context = {
        'wish': wish,
        'ownertext': settings.WISHLIST_OWNER_S,
        'titletext': settings.WISHLIST_TITLE,
        'base_url': settings.WISHLIST_URL,
    }
    return render(request, 'wishlist/nick_entry.html', context)

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'nick_entry.html', {'form': form})


def unbuy(request, secret):
    wish = get_object_or_404(Wish, unbuy_string=secret)
    wish.bought = False
    wish.unbuy_string = None
    wish.santa_nick = ""
    wish.save()
    return HttpResponseRedirect('/')


def buyerror(request):
    context = {
        'ownertext': settings.WISHLIST_OWNER_S,
        'titletext': settings.WISHLIST_TITLE,
    }
    return render(request, 'wishlist/buyerror.html', context)

def stats(request):
    context = {
        'ownertext': settings.WISHLIST_OWNER_S,
        'titletext': settings.WISHLIST_TITLE,
        'nr_done': Wish.objects.filter(bought=True).count(),
        'nr_total': Wish.objects.count(),
    }
    return render(request, 'wishlist/stats.html', context)
