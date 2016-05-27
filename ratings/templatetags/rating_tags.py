from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Score, Vote

register = template.Library()

class BaseRatingNode(template.Node):
	'''
	Deze base helper klasse wordt gebruikt voor de get_rating_* template tags
	'''

	def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, rating=None):
		if ctype is None and object_expr is None:
			raise template.TemplateSyntaxError(
    			"Comment nodes must be given either a literal object or a ctype and object pk."
    			)

		self.as_varname = as_varname
		self.ctype = ctype
		self.object_pk_expr = object_pk_expr
		self.object_expr = object_expr
		self.rating = rating

	@classmethod
	def handle_token(cls, parser, token):

		tokens = token.split_contents()

		if tokens[1] != 'for':
			raise template.TemplateSyntaxError('Tweede argument in %r tag moet "for" zijn' % tokens[0])


		if len(tokens) == 5:
			if tokens[3] != 'as':
				raise template.TemplateSyntaxError('Vierde argument in %r tag moet "as" zijn' % tokens[0])

			return cls(
				object_expr=parser.compile_filter(tokens[2]),
				as_varname=tokens[4]
				)

		else:
			raise template.TemplateSyntaxError('voorlopig aanvaard tim enkel deze setup, kan nog aangepast worden')

	def render(self, context):
		qs = self.get_queryset(context)
		context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
		return ''

	def get_context_value_from_queryset(self, context, qs):
		"""Subclasses should override this."""
		raise NotImplementedError


@register.simple_tag
def get_rating_form(parser, token):

	pass

@register.simple_tag
def votes_count(obj):
	'''
	Deze template tag retourneert het totaal aantal gebruikers dat een stem heeft
	uitgebracht op dit object

	Gebruik {% votes_count <obj> %}
	'''

	count = Vote.objects.filter(
		object_id=obj.pk,
		content_type=ContentType.objects.get_for_model(obj),
	).exclude(overall_rating=0).count()

	return count

@register.simple_tag
def overall_rating(obj):
	'''
	Deze template tag retourneert de overall score van een object

	Gebruik {% overall_rating obj as var %}
	'''

	try:
		ct = ContentType.objects.get_for_model(obj)

		score = Score.objects.get(
			object_id=obj.pk,
			content_type=ct,
		).score or 0

	except Vote.DoesNotExist:
		score = 0

	return score

@register.simple_tag
def user_rating(user, obj):
	'''
	Deze template tag retourneert de score die een gebruiker heeft uitgebracht op het object

	Gebruik {% user-rating user obj %}
	'''

	return user_rating_value(user, obj)

def user_rating_value(user, obj):
	try:
		ct = ContentType.objects.get_for_model(obj)

		score = Vote.objects.get(
			object_id=obj.pk,
			content_type=ct,
			user=user
		).score

	except Vote.DoesNotExist:

		score = 0

	return score