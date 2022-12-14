from django.contrib import admin

from .models import Board, Column, CheckList, Mark, Comment, Card

class BoardAdmin(admin.ModelAdmin):
    pass

class ColumnAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    pass

class CheckListAdmin(admin.ModelAdmin):
    pass


admin.site.register(Board, BoardAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Mark)
admin.site.register(Comment)
