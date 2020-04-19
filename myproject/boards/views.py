from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count

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
    topics = board.topics.order_by('-last_updated').annotate(
        replies=Count('posts') - 1
    )
    return render(request, 'boards/topics.html', {'board': board,
                                                  'topics': topics})

@login_required
def new_topic(request, pk):
    """
    View that renders a form to create a new topic in the specific
    board with given pk.
    """
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            # TODO: Redirect to the created topic page
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board,
                                                     'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'boards/topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic,
                                                       'form': form})
