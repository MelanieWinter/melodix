from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Playlist, Song

# Create your views here.
def home(request):
    return render(request, 'home.html')

def playlist_index(request):
    playlists = Playlist.objects.all()
    return render(request, 'playlists/index.html', {
        'playlists': playlists
    })

@login_required
def playlists_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    # create list of songs

    return render(request, 'playlists/detail.html', {
        'playlist': playlist,
        # needs to render songs
    })

class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name']

class PlaylistUpdate(LoginRequiredMixin, UpdateView):
    model = Playlist
    fields = ['name']

class PlaylistDelete(LoginRequiredMixin, DeleteView):
    model = Playlist
    success_url = '/playlists'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)    