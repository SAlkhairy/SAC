# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Feedback, NewsItem
from voting.models import SACYear
from .forms import FeedbackForm


def show_page(request, page_id):
    return render(request, 'general/'+page_id+'.html')

def add_feedback(request):
    current_year = SACYear.objects.get_current()

    if request.method == 'GET':
        if request.user.is_staff or not request.user.is_authenticated:
            form = FeedbackForm()
        else:
            city = request.user.profile.city
            college = request.user.profile.college
            email = request.user.email
            instance = Feedback(email=email,city=city, college=college)
            form = FeedbackForm(instance=instance)
    elif request.method == 'POST':
        instance = Feedback(year=current_year)
        form = FeedbackForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form = form.save()

    context = {'form': form}
    return render(request, 'general/add_feedback.html', context)

def list_news(request):
    news_items = NewsItem.objects.all().order_by('-submission_date')
    return render(request, 'general/news_list.html', {'news_items': news_items})

#def show_newsitem(request, news_id):
#    news_item = get_object_or_404(NewsItem, pk=news_id)
#    return render(request, 'general/news_item.html', {'news_item': news_item})
