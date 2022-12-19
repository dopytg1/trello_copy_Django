from django.core.exceptions import PermissionDenied

from .models import Board


def user_allowed_to_the_board():
	def decorator(view_func):
		def wrapper_func(request, board_id, *args, **kwargs):
			if request.user in Board.objects.get(pk=board_id).user_id.all():
				return view_func(request, board_id, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator


def user_allowed_to_the_card():
	def decorator(view_func):
		def wrapper_func(request, board_id, card_id, *args, **kwargs):
			if request.user in Board.objects.get(pk=board_id).user_id.all():
				return view_func(request, board_id, card_id, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator

def user_allowed_to_delete_column():
	def decorator(view_func):
		def wrapper_func(request, board_id, column_id, *args, **kwargs):
			if request.user in Board.objects.get(pk=board_id).user_id.all():
				return view_func(request, board_id, column_id, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator

def user_allowed_to_delete_mark():
	def decorator(view_func):
		def wrapper_func(request, board_id, card_id, mark_id, *args, **kwargs):
			if request.user in Board.objects.get(pk=board_id).user_id.all():
				return view_func(request, board_id, card_id, mark_id, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator

def user_allowed_to_delete_checklist():
	def decorator(view_func):
		def wrapper_func(request, board_id, card_id, checklist_id, *args, **kwargs):
			if request.user in Board.objects.get(pk=board_id).user_id.all():
				return view_func(request, board_id, card_id, checklist_id, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator

