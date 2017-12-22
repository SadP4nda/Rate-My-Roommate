from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from .models import College, Roomate, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse
from .forms import CommentForm
from django.views.generic.detail import SingleObjectMixin
from decimal import Decimal
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
        return Roomate.objects.all().order_by('first_name')


class CollegeRoomatesView(ListView):
    template_name = "roomaterating/roommateview.html"
    context_object_name = "roommates"
    paginate_by = 5
    def get_queryset(self):
        return College.objects.get(pk=self.kwargs['pk']).roomate_set.all()

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
                rating_lst.append(comment.OverallRating)
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
        comment = Comment.objects.create(
            roomate = Roomate.objects.get(pk=self.kwargs['pk']),
            username = form.cleaned_data['username'],
            OverallRating = form.cleaned_data['OverallRating'],
            Description = form.cleaned_data['Description']
        )
        return super(AddComment, self).form_valid(form)

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
    fields = ['college', 'first_name', 'last_name']
    template_name = 'roomaterating/AddRoommate.html'

    def get_success_url(self):
        return reverse('roomaterating:index')


class CollegeCreateView(CreateView):
    model = College
    fields = ['campus','website_link']
    template_name = 'roomaterating/AddCollege.html'

    def get_success_url(self):
        return reverse('roomaterating:add-roommate')


