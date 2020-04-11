from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    """
    View showing all the boards and board related informations.
    """
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'boards/home.html', context)

def board_topics(request, pk):
    """
    View showing the topics created in the specific board with given pk and
    the relevant information of these topics.
    """
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'boards/topics.html', {'board': board})

def new_topic(request, pk):
    """
    View to create a new topic in the specific board with given pk.
    """
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        # TODO: get the currently logged in user
        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        # TODO: redirect to the created topic page
        return redirect('boards:board_topics', pk=board.pk)

    return render(request, 'boards/new_topic.html', {'board': board})
