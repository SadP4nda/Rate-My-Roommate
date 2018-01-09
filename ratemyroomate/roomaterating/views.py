from django.views.generic import TemplateView, ListView, DetailView
from .models import College, Roomate, Comment, CollegeSuggestion
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse
from .forms import CommentForm, RoommateCreateForm, CollegeSuggestionCreateForm
from django.views.generic.detail import SingleObjectMixin
from decimal import Decimal
from django.db.models import Q
from itertools import chain
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db import IntegrityError
# Create your views here.

def get_avg(lst):
    total = 0
    for item in lst:
        total += item
    return total/len(lst)


class IndexView(TemplateView):
    template_name = "roomaterating/index.html"


class CollegeView(ListView):
    template_name = "roomaterating/collegeview.html"
    context_object_name = "colleges"
    paginate_by = 5
    def get_queryset(self):
        return College.objects.all().order_by('campus')


class RoomateView(ListView):
    template_name = "roomaterating/roommateview.html"
    context_object_name = "roommates"
    paginate_by = 5
    def get_queryset(self):
        return Roomate.objects.all().order_by('last_name')


class CollegeRoomatesView(ListView):
    template_name = "roomaterating/roommateview.html"
    context_object_name = "roommates"
    paginate_by = 5
    def get_queryset(self):
        return College.objects.get(pk=self.kwargs['pk']).roomate_set.all().order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(CollegeRoomatesView, self).get_context_data(**kwargs)
        context['campus'] = College.objects.get(pk=self.kwargs['pk'])
        return context


class RoommateDetailView(DetailView):
    model = Roomate
    template_name = "roomaterating/RoommateDetailView.html"
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(RoommateDetailView,self).get_context_data(**kwargs)
        roommatecomments = self.get_object().comment_set.all()
        context['OverallAvg'] = "No rating Available"
        if len(roommatecomments) > 0:
            rating_lst = []
            for comment in roommatecomments:
                rating_lst.append(comment.Overall_Rating)
            OverallAvg = round(Decimal(get_avg(rating_lst)),1)
            context['OverallAvg'] = OverallAvg
            context['comments'] = roommatecomments

        context['form'] = CommentForm()
        return context


class AddComment(FormView, SingleObjectMixin):
    form_class = CommentForm
    template_name = "roomaterating/RoommateDetailView.html"
    model = Roomate

    def form_valid(self, form):

        try:
            Comment.objects.create(
                roomate = Roomate.objects.get(pk=self.kwargs['pk']),
                username = form.cleaned_data['username'],
                Overall_Rating = form.cleaned_data['Overall_Rating'],
                Description = form.cleaned_data['Description']
                )
        except IntegrityError:
            return HttpResponseRedirect(
                reverse('roomaterating:viewroommate', kwargs={'pk': self.kwargs['pk']}))
        return super(AddComment, self).form_valid(form)

    def form_invalid(self, form):

        return HttpResponseRedirect(reverse('roomaterating:viewroommate', kwargs={'pk': self.kwargs['pk']}))

    def get_success_url(self):
        return reverse('roomaterating:viewroommate', kwargs={'pk': self.kwargs['pk']})


class RoommateDetail(TemplateView):

    def get(self, request, *args, **kwargs):
        view = RoommateDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AddComment.as_view()
        return view(request, *args, **kwargs)


class RoomateCreateView(CreateView):
    model = Roomate
    template_name = 'roomaterating/AddRoommate.html'
    form_class = RoommateCreateForm
    def get_success_url(self):
        return reverse('roomaterating:index')


class CollegeCreateView(CreateView):
    model = CollegeSuggestion
    form_class = CollegeSuggestionCreateForm
    template_name = 'roomaterating/AddCollege.html'

    def get_success_url(self):
        return reverse('roomaterating:index')

class RoommateSearch(ListView):
    template_name = "roomaterating/roommateviewsearch.html"
    context_object_name = 'roommates'
    paginate_by = 5
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            splitted_query = query.split(' ')
            if len(splitted_query) > 1:
                first_name_matches = Roomate.objects.all().filter(Q(first_name__icontains=splitted_query[0]) |
                                                                  Q(last_name__icontains=splitted_query[0])).\
                    order_by('first_name', 'last_name')
                last_name_matches = Roomate.objects.all().filter(Q(first_name__icontains=splitted_query[len(splitted_query)-1])
                                                                 | Q(last_name__icontains=splitted_query[len(splitted_query)-1]))\
                    .order_by('first_name', 'last_name')
                name_set = set(chain(first_name_matches, last_name_matches))
                result = []
                for name in name_set:
                    result.append(name)
            else:
                result = Roomate.objects.all().filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).\
                    order_by('first_name', 'last_name')
        else:
            return[]
        return result
