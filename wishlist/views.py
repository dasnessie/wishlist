"""
defines the methods for reacting to the defined urls
"""
import random
import string
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings

from wishlist.models import Wish


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
    wish = get_object_or_404(Wish, pk=wish_id)
    if not wish.bought:
        wish.bought = True
        wish.unbuy_string = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=20))
        wish.save()
        return HttpResponseRedirect(reverse('bought', args=(wish.unbuy_string,)))
    else:
        return HttpResponseRedirect('/buyerror')


def unbuy(request, secret):
    wish = get_object_or_404(Wish, unbuy_string=secret)
    wish.bought = False
    wish.unbuy_string = None
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
