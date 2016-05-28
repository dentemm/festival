from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text

from ..models import Score, Vote
from ..forms import VoteForm

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

	def get_queryset(self, context):
		ctype, object_id = self.get_target_ctype_pk(context)
		if not object_id:
		    return Vote.objects.none()

		qs = Vote.objects.filter(
		    content_type=ctype,
		    object_id=smart_text(object_id),
		)

		# The is_public and is_removed fields are implementation details of the
		# built-in comment model's spam filtering system, so they might not
		# be present on a custom comment model subclass. If they exist, we
		# should filter on them.
		field_names = [f.name for f in Vote._meta.fields]
		if 'is_public' in field_names:
		    qs = qs.filter(is_public=True)
		if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
		    qs = qs.filter(is_removed=False)
		if 'user' in field_names:
		    qs = qs.select_related('user')
		return qs

	def get_target_ctype_pk(self, context):
		if self.object_expr:
			try:
				obj = self.object_expr.resolve(context)
			except template.VariableDoesNotExist:
				return None, None
			return ContentType.objects.get_for_model(obj), obj.pk
		else:
			return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)


	def get_context_value_from_queryset(self, context, qs):
		"""Subclasses should override this."""
		raise NotImplementedError


class RatingCountNode(BaseRatingNode):
	'''
	Insert a count of rating objects into the context.
	'''

	def get_context_value_from_queryset(self, context, qs):
		return qs.count()


class RatingFormNode(BaseRatingNode):
	'''
	Deze template tag voegt het form toe aan de context
	'''

	def get_form(self, context):
		obj = self.get_object(context)

		print('template tag get_form: obj= %s' % obj)

		if obj:
			return VoteForm(obj)

		else:
			return None

	def get_object(self, context):

		print('template tag: %s ' % self)

		if self.object_expr:

			print(self.object_expr)

			try:
				return self.object_expr.resolve(context)

			except template.VariableDoesNotExist:
				return None

		else:
			object_id = self.object_expr.resolve(context, ignore_failures=True)

			return self.ctype.get_object_for_this_type(pk=object_id)

	def render(self, context):

		context[self.as_varname] = self.get_form(context)
		return ''


@register.tag
def get_rating_count(parser, token):

	return RatingCountNode.handle_token(parser, token)


@register.tag
def get_vote_form(parser, token):
    """
    Get a (new) form object to post a new comment.
    Syntax::
        {% get_comment_form for [object] as [varname] %}
        {% get_comment_form for [app].[model] [object_id] as [varname] %}
    """
    return RatingFormNode.handle_token(parser, token)



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