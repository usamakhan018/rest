from django.http import HttpResponse

def ajax_required(f):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_active and request.user.is_authenticated:
			return HttpResponse('either your account is not activated or you are not logged in.')
			if not request.is_ajax():
				return HttpResponse('request method not allowed')
	
		return f(request, *args, **kwargs)
	wrapper.__doc__ = f.__doc__
	wrapper.__name__ = f.__name__
	return wrapper

	return f(request, *args, **kwargs)

# def ajax_required(f):
# 	def wrap(request, *args, **kwargs):
# 		if not request.is_ajax():
# 		return HttpResponseBadRequest()
# 	return f(request, *args, **kwargs)
# 	wrap.__doc__=f.__doc__
# 	wrap.__name__=f.__name__
# 	return wrap