import random
import string
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from wishlist.models import Wish


def index(request):
    wish_list = Wish.objects.order_by('bought', '-importance')
    context = {
        'wish_list': wish_list,
    }
    return render(request, 'wishlist/index.html', context)

def bought(request, secret):
    wish = get_object_or_404(Wish, unbuy_string=secret)
    return HttpResponse("You bought %s" % wish.title_text)

def buy(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    wish.bought = True
    wish.unbuy_string = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=20))
    wish.save()
    return HttpResponseRedirect('/wishlist')
    # return HttpResponseRedirect(reverse('wishlist:bought', args=(wish.unbuy_string,)))

def unbuy(request, secret):
    wish = get_object_or_404(Wish, unbuy_string=secret)
    wish.bought = False
    wish.unbuy_string = None
    wish.save()
    return HttpResponseRedirect('/wishlist')
