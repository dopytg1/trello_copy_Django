from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound

from .forms import AddBoardForm
from .models import Board, Column, Card, Comment, Mark

@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        form = AddBoardForm(request.POST, request.FILES)

        if form.is_valid():
            board = Board.objects.create(**form.cleaned_data)
            board.user_id.add(request.user)

            board.save()
            return redirect("home")
        else:
            print(form.errors.as_data())

    form = AddBoardForm()
    boards = Board.objects.filter(user_id=request.user)
    context = {
        "form": form,
        "boards": boards
    }
    return render(request, 'trello_planner/home.html', context)

@login_required(login_url='/login')
def inside_the_board(request, id):
    columns = Column.objects.filter(board_id=id)
    board = Board.objects.get(pk=id)

    if request.method == "POST":
        if 'add_column' in request.POST:
            title = request.POST.get('title')
            board = Board.objects.get(pk=id)
            column = Column.objects.create(title=title, board_id=board)

            column.save()
            return redirect('boards', id)
        elif 'add_card' in request.POST:
            head = request.POST.get('head')
            columnPk = request.POST.get('column_value')
            column = Column.objects.get(pk=columnPk)
            card = Card.objects.create(title=head)

            column.cards_inside.add(card)
            column.save()

            return redirect('boards', id)
        elif 'change_board' in request.POST:
            form = AddBoardForm(request.POST, request.FILES)

            if form.is_valid():
                print(form.cleaned_data['background'])
                board.title = form.cleaned_data['title']
                board.background = form.cleaned_data['background']
                board.save()
                return redirect('boards', id)
            else:
                print(form.errors.as_data())

    form_change_board = AddBoardForm()
    context = {
        'columns': columns,
        'board_id': id,
        'board': board,
        'form_change_board': form_change_board
    }
    return render(request, 'trello_planner/inside_the_board.html', context)

@login_required(login_url='/login')
def inside_the_card(request, board_id, card_id):
    board = Board.objects.get(pk=board_id)
    card = Card.objects.get(pk=card_id)
    comments = Comment.objects.filter(card_id=card)
    marks = Mark.objects.filter(card_id= card)

    if request.method == "POST":
        if 'comments_creation_form' in request.POST:
            comment_body = request.POST.get('comment_body')
            comment = Comment.objects.create(author=request.user.username, body=comment_body, card_id=card)
            comment.save()

            return redirect('inside_the_card', board_id, card_id)
        if 'card_description' in request.POST:
            description = request.POST.get('description')
            card.description = description
            card.save()

            return redirect('inside_the_card', board_id, card_id)
        if 'add_mark' in request.POST:
            color = request.POST.get('mark_color')
            mark = Mark.objects.create(hex_color=color, card_id=card)
            mark.save()

            return redirect('inside_the_card', board_id, card_id)

    context = {
        'board': board,
        'card': card,
        'comments': comments,
        'marks': marks
    }
    return render(request, 'trello_planner/inside_the_card.html', context)

@login_required(login_url='/login')
def delete_column(request, board_id, column_id ):
    try:
        column = Column.objects.get(pk=column_id)
        column.delete()

        return redirect('boards', board_id)
    except Column.DoesNotExist:
         HttpResponseNotFound("<h2>Column not found</h2>")

@login_required(login_url='/login')
def delete_board(request, id):
    try:
        board = Board.objects.get(pk=id)
        board.delete()

        return redirect('home')
    except Board.DoesNotExist:
         HttpResponseNotFound("<h2>Board not found</h2>")

@login_required(login_url='/login')
def delete_card(request, board_id, card_id):
    try:
        card = Card.objects.get(pk=card_id)

        card.delete()
        return redirect('boards', board_id)
    except Card.DoesNotExist:
         HttpResponseNotFound("<h2>Card not found</h2>")

def delete_mark(request, board_id, card_id, mark_id):
    try:
        mark = Mark.objects.get(pk=mark_id)

        mark.delete()
        return redirect('inside_the_card', board_id, card_id)
    except Mark.DoesNotExist:
         HttpResponseNotFound("<h2>Mark not found</h2>")
