from django import http
from django.conf import settings
from django.shortcuts import render
from django.utils.html import escape
from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.template.loader import render_to_string

from django_comments import signals

from .forms import CommentFormWithTitle



class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """

    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})
# Create your views here.


@csrf_protect
@require_POST
def custom_submit(request, next=None, using=None):

	print('custom submit!')

	data = request.POST.copy()

	print('data: %s' % data)

	if request.user.is_authenticated():
	    if not data.get('name', ''):
	        data["name"] = request.user.get_username()
	    if not data.get('email', ''):
	        data["email"] = request.user.email

	ctype = data.get("content_type")
	object_pk = data.get("object_pk")
	user = request.user

	print('hier dan wel?')

	try:
	    model = apps.get_model(*ctype.split(".", 1))
	    target = model._default_manager.using(using).get(pk=object_pk)

	except TypeError:

	    print('error1')

	    return CommentPostBadRequest(
	        "Invalid content_type value: %r" % escape(ctype))
	except AttributeError:

	    print('error2')

	    return CommentPostBadRequest(
	        "The given content-type %r does not resolve to a valid model." % escape(ctype))

	except ObjectDoesNotExist:
	    print('error3')
	    return CommentPostBadRequest(
	        "No object matching content-type %r and object PK %r exists." % (
	            escape(ctype), escape(object_pk)))
	except (ValueError, ValidationError) as e:
	    print('error3')
	    return CommentPostBadRequest(
	        "Attempting go get content-type %r and object PK %r exists raised %s" % (
	            escape(ctype), escape(object_pk), e.__class__.__name__))

	print('form komt eraan')

	form = CommentFormWithTitle(target, data=data)

	print('form done')

	# Check security information
	if form.security_errors():
	    return CommentPostBadRequest(
	        "The comment form failed security verification: %s" % escape(str(form.security_errors())))

	comment = form.get_comment_object()

	if request.user.is_authenticated():
	    comment.user = request.user

	# Signal that the comment is about to be saved
	responses = signals.comment_will_be_posted.send(
	    sender=comment.__class__,
	    comment=comment,
	    request=request
	)

	for (receiver, response) in responses:
	    if response is False:
	        return CommentPostBadRequest(
	            "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

	comment.save()
	signals.comment_was_posted.send(
	    sender=comment.__class__,
	    comment=comment,
	    request=request
	)

	my_dict = 	{	
					'comment_title': 	comment.title,
					'comment':			comment.comment
				}

	return JsonResponse(my_dict)

