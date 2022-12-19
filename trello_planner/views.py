from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse  

from .forms import AddBoardForm
from .models import Board, Column, Card, Comment, Mark, CheckList, CheckListElement
from .permissions import (
    user_allowed_to_the_board, user_allowed_to_the_card, 
    user_allowed_to_delete_column, user_allowed_to_delete_mark,
    user_allowed_to_delete_checklist)

from trello_main.models import CustomUser

@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        if 'create_board' in request.POST:
            form = AddBoardForm(request.POST, request.FILES)

            if form.is_valid():
                board = Board.objects.create(**form.cleaned_data)
                board.user_id.add(request.user)

                board.save()
                return redirect("home")
            else:
                print(form.errors.as_data())
        if 'search_boards' in request.POST:
            boards_title = request.POST.get('boards-title')
            boards = Board.objects.filter(title__contains=boards_title)
            form = AddBoardForm()

            context = {
                "form": form,
                "boards": boards
            }

            return render(request, 'trello_planner/home.html', context)

    form = AddBoardForm()
    boards = Board.objects.filter(user_id=request.user)
    context = {
        "form": form,
        "boards": boards
    }
    return render(request, 'trello_planner/home.html', context)

@user_allowed_to_the_board()
def inside_the_board(request, board_id):
    columns = Column.objects.filter(board_id=board_id)
    board = Board.objects.get(pk=board_id)

    if request.method == "POST":
        if 'add_column' in request.POST:
            title = request.POST.get('title')
            board = Board.objects.get(pk=board_id)
            column = Column.objects.create(title=title, board_id=board)
            column.save()

            return redirect('boards', board_id)
        elif 'add_card' in request.POST:
            head = request.POST.get('head')
            columnPk = request.POST.get('column_value')
            column = Column.objects.get(pk=columnPk)
            card = Card.objects.create(title=head)

            column.cards_inside.add(card)
            column.save()

            return redirect('boards', board_id)
        elif 'change_board' in request.POST:
            form = AddBoardForm(request.POST, request.FILES)

            if form.is_valid():
                print(form.cleaned_data['background'])
                board.title = form.cleaned_data['title']
                board.background = form.cleaned_data['background']
                board.save()
                
                return redirect('boards', board_id)
            else:
                print(form.errors.as_data())
        elif 'change_column' in request.POST:
            title = request.POST.get('column_title')
            column_pk = request.POST.get('column')
            column = Column.objects.get(pk=column_pk)
            column.title = title
            column.save()

            return redirect('boards', board_id)
        elif 'add_new_user_to_the_board' in request.POST:
            email = request.POST.get('user_email')
            try:
                user = CustomUser.objects.get(email=email)
                board.user_id.add(user)
                board.save()
            except:
                return HttpResponseNotFound("<h2>User not found</h2>")

            return redirect('boards', board_id)
        

    form_change_board = AddBoardForm()
    context = {
        'columns': columns,
        'board_id': board_id,
        'board': board,
        'form_change_board': form_change_board
    }
    return render(request, 'trello_planner/inside_the_board.html', context)

@user_allowed_to_the_card()
def inside_the_card(request, board_id, card_id):
    board = Board.objects.get(pk=board_id)
    card = Card.objects.get(pk=card_id)
    comments = Comment.objects.filter(card_id=card)
    marks = Mark.objects.filter(card_id=card)
    checklists = CheckList.objects.filter(card_id=card)

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
            if color == None:
                color = request.POST.get('mark_color_user')

            mark = Mark.objects.create(hex_color=color, card_id=card)
            mark.save()

            return redirect('inside_the_card', board_id, card_id)

        if 'add_checklist' in request.POST:
            title = request.POST.get('checklist_title')

            cheklist = CheckList.objects.create(title=title, card_id=card)
            cheklist.save()

            return redirect('inside_the_card', board_id, card_id)

        if 'add_checklist_element' in request.POST:
            title = request.POST.get('element_title')
            cheklist_pk = request.POST.get('checklist')
            cheklist = CheckList.objects.get(pk=cheklist_pk)
            cheklist_element = CheckListElement.objects.create(title=title, cheklist_id=cheklist)
            cheklist_element.save()

            return redirect('inside_the_card', board_id, card_id)

        if 'change_cheklistelement_state' in request.POST:
            element_pk = request.POST.get('element')
            checklist_element = CheckListElement.objects.get(pk=element_pk)

            if checklist_element.is_checked == False:
                checklist_element.is_checked = True
                checklist_element.save()
                return redirect('inside_the_card', board_id, card_id)

            checklist_element.is_checked = False
            checklist_element.save()
            return redirect('inside_the_card', board_id, card_id)
        
        if 'change_date' in request.POST:
            date = request.POST.get('date')
            card.expiring_date = date
            card.save()

            return redirect('inside_the_card', board_id, card_id)

    context = {
        'board': board,
        'card': card,
        'comments': comments,
        'marks': marks,
        'checklists': checklists
    }
    return render(request, 'trello_planner/inside_the_card.html', context)


@user_allowed_to_delete_column()
def delete_column(request, board_id, column_id ):
    try:
        column = Column.objects.get(pk=column_id)
        column.delete()

        return redirect('boards', board_id)
    except Column.DoesNotExist:
        return HttpResponseNotFound("<h2>Column not found</h2>")

@user_allowed_to_the_board()
def delete_board(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
        board.delete()

        return redirect('home')
    except Board.DoesNotExist:
        return HttpResponseNotFound("<h2>Board not found</h2>")

@user_allowed_to_the_card()
def delete_card(request, board_id, card_id):
    try:
        card = Card.objects.get(pk=card_id)

        card.delete()
        return redirect('boards', board_id)
    except Card.DoesNotExist:
        return HttpResponseNotFound("<h2>Card not found</h2>")

@user_allowed_to_delete_mark()
def delete_mark(request, board_id, card_id, mark_id):
    try:
        mark = Mark.objects.get(pk=mark_id)

        mark.delete()
        return redirect('inside_the_card', board_id, card_id)
    except Mark.DoesNotExist:
        return HttpResponseNotFound("<h2>Mark not found</h2>")

@user_allowed_to_delete_checklist()
def delete_checklist(request, board_id, card_id, checklist_id):
    try:
        checklist = CheckList.objects.get(pk=checklist_id)

        checklist.delete()
        return redirect('inside_the_card', board_id, card_id)
    except CheckList.DoesNotExist:
        return HttpResponseNotFound("<h2>CheckList not found</h2>")   
