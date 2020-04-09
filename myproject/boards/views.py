from django.shortcuts import render
from django.http import HttpResponse
from .models import Board

# Create your views here.
def home(request):
    """
    Home view showing all the boards and board related informations.
    """
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'boards/home.html', context)

def board_topics(request, pk):
    """
    Topics view showing the topics created in the given specific board and
    the relevant information of these topics.
    """
    board = Board.objects.get(pk=pk)
    return render(request, 'boards/topics.html', {'board': board})
