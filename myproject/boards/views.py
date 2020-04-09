from django.shortcuts import render
from django.http import HttpResponse
from .models import Board

# Create your views here.
def home(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'boards/home.html', context)

def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'boards/topics.html', {'board': board})
