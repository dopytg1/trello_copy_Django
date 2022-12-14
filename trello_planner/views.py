from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound

from .forms import AddBoardForm
from .models import Board, Column, Card

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

    columns = Column.objects.filter(board_id=id)
    board = Board.objects.get(pk=id)
    context = {
        'columns': columns,
        'board_id': id,
        'board': board
    }
    return render(request, 'trello_planner/inside_the_board.html', context)


@login_required(login_url='/login')
def delete_column(request, board_id, column_id ):
    try:
        column = Column.objects.get(pk=column_id)
        column.delete()

        return redirect('boards', board_id)
    except Column.DoesNotExist:
         HttpResponseNotFound("<h2>Column not found</h2>")


def delete_board(request, id):
    try:
        board = Board.objects.get(pk=id)
        board.delete()

        return redirect('home')
    except Board.DoesNotExist:
         HttpResponseNotFound("<h2>Board not found</h2>")
         

@login_required(login_url='/login')
def inside_the_card(request, board_id, card_id):
    card = Card.objects.get(pk=card_id)

    context = {
        'card_id': card_id,
        'card': card
    }
    return render(request, 'trello_planner/inside_the_card.html', context)
