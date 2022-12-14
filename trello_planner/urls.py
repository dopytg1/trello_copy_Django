from django.urls import path
from .views import (
    home, inside_the_board, inside_the_card, 
    delete_column, delete_board, delete_card, 
    delete_mark, delete_checklist
    )


urlpatterns = [
    path('', home, name='home'),
    path('board/<int:board_id>', inside_the_board, name='boards'),
    path('board/<int:board_id>/card/<int:card_id>', inside_the_card, name='inside_the_card'),

    path('board/delete/<int:board_id>', delete_board, name='delete_board'),
    path('board/<int:board_id>/delete/column/<int:column_id>', delete_column, name='delete_column'),
    path('board/<int:board_id>/delete/card/<int:card_id>', delete_card, name='delete_card'),
    path('board/<int:board_id>/card/<int:card_id>/delete/mark/<int:mark_id>', delete_mark, name='delete_mark'),
    path('board/<int:board_id>/card/<int:card_id>/delete/checklist/<int:checklist_id>', delete_checklist, name='delete_checklist'),
]