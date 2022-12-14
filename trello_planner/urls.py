from django.urls import path
from .views import home, inside_the_board, inside_the_card, delete_column, delete_board


urlpatterns = [
    path('', home, name='home'),
    path('board/<int:id>', inside_the_board, name='boards'),
    path('board/delete/<int:id>', delete_board, name='delete_board'),
    path('board/<int:board_id>/card/<int:card_id>', inside_the_card, name='inside_the_card'),
    path('board/<int:board_id>/delete/column/<int:column_id>', delete_column, name='delete_column'),
    
]