import operator

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text
from django.forms import formset_factory

from ..models import Score, Vote
from ..forms import VoteForm, BaseVoteFormSet

from home.models import FestivalPage

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

		#print('tokentim: %s' % token)

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

class RatingFormsetNode(template.Node):
	'''
	Deze template tag wordt gebruikt om een formset aan de context toe te voegen. De formset bestaat uit
	alle beoordeelbare kenmerken van een festival
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

		#print('tokentim: %s' % token)

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

	def get_formset(self, context):

		festival = self.get_object(context)

		print('festival: %s' % festival)

		if festival: 

			rateable_attributes = festival.rateable_attributes.all()
			num_attributes = len(rateable_attributes)

			VoteFormSet = formset_factory(VoteForm, formset=BaseVoteFormSet, extra=num_attributes)

			formset = VoteFormSet(instances=rateable_attributes)

			return formset		


	def get_object(self, context):

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

		context[self.as_varname] = self.get_formset(context)
		return ''

class RatingFormNode(BaseRatingNode):
	'''
	Deze template tag voegt het form toe aan de context
	'''

	def get_form(self, context):
		obj = self.get_object(context)

		if obj:
			return VoteForm(obj)

		else:
			return None

	def get_object(self, context):

		if self.object_expr:

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

class RatingOverviewNode(template.Node):
	'''
	Deze Node klasse wordt door de render_ratings template tag gebruikt om de details ratings
	voor een festival te renderen. Hierbij worden alle kenmerken geretourneerd
	'''

	def __init__(self, ctype=None, object_pk_expr=None, object_expr=None):
		if ctype is None and object_expr is None:
			raise template.TemplateSyntaxError(
				"Comment nodes must be given either a literal object or a ctype and object pk."
				)

		self.ctype = ctype
		self.object_pk_expr = object_pk_expr
		self.object_expr = object_expr

	@classmethod
	def handle_token(cls, parser, token):

		tokens = token.split_contents()

		if tokens[1] != 'for':
			raise template.TemplateSyntaxError('Tweede argument in %r tag moet "for" zijn' % tokens[0])

		if len(tokens) == 3:
			return cls(object_expr=parser.compile_filter(tokens[2]))

		else:
			raise template.TemplateSyntaxError('voorlopig aanvaard tim enkel deze setup, kan nog aangepast worden')

	def get_target_ctype_pk(self, context):
		if self.object_expr:
			try:
				obj = self.object_expr.resolve(context)
			except template.VariableDoesNotExist:
				return None, None
			return ContentType.objects.get_for_model(obj), obj.pk
		else:
			return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

	def get_object(self, context):
		if self.object_expr:
			try:
				return self.object_expr.resolve(context)
			except template.VariableDoesNotExist:
				return None

	def render(self, context):
		ctype, object_pk = self.get_target_ctype_pk(context)

		if object_pk: 
			template = 'ratings/rating_overview.html'

		festival = self.get_object(context)

		attributes = festival.rateable_attributes

		print(attributes)

		context_dict = context.flatten()


		print('render is being called!')

		return ''

@register.tag
def get_rating_count(parser, token):

	return RatingCountNode.handle_token(parser, token)


@register.tag
def get_vote_form(parser, token):
    """
    Get a (new) form object to post a new comment.
    Syntax::
        {% get_vote_form for [object] as [varname] %}
        {% get_vote_form for [app].[model] [object_id] as [varname] %}
    """
    return RatingFormNode.handle_token(parser, token)


@register.tag
def get_vote_formset(parser, token):
    """
    Get a (new) formset object to post a new comment.
    Syntax::
        {% get_vote_formset for [object] as [varname] %}
        {% get_vote_formset for [app].[model] [object_id] as [varname] %}
    """
    return RatingFormsetNode.handle_token(parser, token)


@register.tag
def render_ratings(parser, token):
	'''
	Deze template tag retourneert het de template die aangeeft wat de user ratings voor het
	gegeven festival zijn. Enkel festivals worden aanvaard als parameter

	Gebruik {% votes_count <obj> %}
	'''

	return RatingOverviewNode.handle_token(parser, token)

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
		).score or -1

	except Score.DoesNotExist:
		score = -1

	score = int(round(score))

	return score

@register.simple_tag
def overall_score(obj):

	try:
		ct = ContentType.objects.get_for_model(obj)

		score = Score.objects.get(
			object_id=obj.pk,
			content_type=ct,
		).score or -1

	except Score.DoesNotExist:
		score = -1

	return score

@register.simple_tag
def user_rating_value(user, obj):
	'''
	Deze template tag retourneert de score die een gebruiker heeft uitgebracht op het object

	Gebruik {% user_rating_value user obj %}
	'''

	print('user rating')

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

		return 0

	return int(round(score))


@register.simple_tag
def excellent_rating(obj):
	'''
	Deze template tag retourneert het percentage excellente scores voor een gegeven festival
	Gebruik {% excellent_rating obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		score = Score.objects.get(object_id=obj.pk, content_type=ct)

	except Score.DoesNotExist:

		return '0%'

	return score.excellent_score

@register.simple_tag
def good_rating(obj):
	'''
	Deze template tag retourneert het percentage goede scores voor een gegeven festival
	Gebruik {% good_rating obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		score = Score.objects.get(object_id=obj.pk, content_type=ct)

	except Score.DoesNotExist:

		return '0%'

	return score.good_score

@register.simple_tag
def average_rating(obj):
	'''
	Deze template tag retourneert het percentage gemiddelde scores voor een gegeven festival
	Gebruik {% average_rating obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		score = Score.objects.get(object_id=obj.pk, content_type=ct)

	except Score.DoesNotExist:

		return '0%'

	return score.average_score

@register.simple_tag
def bad_rating(obj):
	'''
	Deze template tag retourneert het percentage slechte scores voor een gegeven festival
	Gebruik {% bad_rating obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		score = Score.objects.get(object_id=obj.pk, content_type=ct)

	except Score.DoesNotExist:

		return '0%'

	return score.bad_score

@register.simple_tag
def top_scores(obj):
	'''
	Deze template tag retourneert enkel de scores van vier best beoordeelde kenmerken van gegeven een festival
	'''

	all_scores = []


	for attr in obj.rateable_attributes.all():

		ct = ContentType.objects.get_for_model(attr)

		try:
			score = Score.objects.get(object_id=attr.pk, content_type=ct)

		except: 
			return ''

		all_scores.append({'attribute': attr.rateable_attribute.name, 'score': int(round(score.score * 2))})

	# sorteer all_scores volgens hun score
	all_scores.sort(key=operator.itemgetter('score'), reverse=True)
	# behoud enkel de eerste vier items, deze hebben dus de beste score 
	all_scores = all_scores[0:4]

	print('test %s' % all_scores)

	return all_scores


@register.simple_tag
def user_rating(user, obj):
	'''
	Deze template tag retourneert geeft aan of een gebruiker een rating heeft uitgebracht op een gegeven festival
	Gebruik {% user_rating user obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)

	try:
		Vote.objects.get(object_id=obj.pk, content_type=ct, user=user)

	except Vote.DoesNotExist:

		return False

	return True

@register.simple_tag
def ratings(obj):
	'''
	Deze template tag retourneert alle votes voor een gegeven festival
	Gebruik {% ratings obj %}
	'''

	ct = ContentType.objects.get_for_model(obj)
	try:
		return Score.objects.get(
			content_type=ct,
			object_id=obj.pk,
			).votes.all()

	except Score.DoesNotExist:
		return []

@register.simple_tag
def total_votes():

	ct = ContentType.objects.get_for_model(FestivalPage)

	return Score.objects.filter(content_type=ct).count()

