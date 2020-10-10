from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Entry, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
# Create your views here.

def LikeView(request, pk):
    entry = get_object_or_404(Entry, id=request.POST.get('entry_id'))
    liked = False
    if entry.entry_likes.filter(id=request.user.id).exists():
        entry.entry_likes.remove(request.user)
        liked = False
    else:
        entry.entry_likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('entry-detail', args=[str(pk)]))

class HomeView(ListView):
    model = Entry
    template_name = 'entries/index.html'
    context_object_name = "innow_entries"
    ordering = ['-entry_date']
    paginate_by = 3

class EntryView(DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EntryView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Entry, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.entry_likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        context["comment"] = Comment,
        return context

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'entries/add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('home')

class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        return super().form_valid(form)
