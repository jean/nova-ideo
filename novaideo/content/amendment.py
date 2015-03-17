# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer
from persistent.dict import PersistentDict

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite, get_obj
from dace.descriptors import SharedUniqueProperty

from pontus.widget import (
    RichTextWidget, 
    SimpleMappingWidget,
    AjaxSelect2Widget)
from pontus.core import VisualisableElementSchema
from pontus.schema import Schema, select

from .interface import IAmendment
from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    Commentable,
    PresentableEntity,
    DuplicableEntity)
from novaideo import _
from novaideo.views.widget import ( 
    AddIdeaWidget, 
    LimitedTextAreaWidget)
from novaideo.content.idea import Idea, IdeaSchema


@colander.deferred
def add_new_idea_widget(node, kw):
    request = node.bindings['request']
    root = getSite()
    url = request.resource_url(root, '@@ideasmanagement')
    return AddIdeaWidget(url=url, item_css_class='new-idea-form hide-bloc')


@colander.deferred
def relatedideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    used_ideas = context.get_used_ideas()
    root = getSite()
    ideas = list(context.proposal.related_ideas.keys())
    ideas.extend(used_ideas)
    ideas = set(ideas)
    values = [(i, i.title) for i in ideas]
    ajax_url = request.resource_url(root, '@@search', 
                                    query={'op':'find_entities', 
                                           'content_types':['Idea']
                                           }
                               )
    return AjaxSelect2Widget(values=values,
                        ajax_url=ajax_url,
                        css_class="search-idea-form",
                        multiple=True)


class RelatedExplanationSchema(Schema):
    """Schema for related explanation"""

    relatedexplanation = colander.SchemaNode(
        colander.Integer(),
        title=_('Apply the same intention'),
        description=_('Choose the intention to apply'),
        missing=None
        )


class NewIdeaSchema(Schema):


    new_idea = select(IdeaSchema(factory=Idea, 
                                 editable=True,
                                 omit=['keywords'], 
                                 widget=SimpleMappingWidget()),
                      ['title',
                       'text',
                       'keywords'])


class IntentionItemSchema(Schema):
    """Schema for Intention item"""

    comment = colander.SchemaNode(
        colander.String(),
        title= _('Explanation'),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=300),
        )

    related_ideas = colander.SchemaNode(
        colander.Set(),
        widget=relatedideas_choice,
        title=_('Related ideas'),
        description=_('Choose related ideas.'),
        missing=[],
        default=[],
        )

    add_new_idea = NewIdeaSchema(widget=add_new_idea_widget)


class Intention(object):
    """Intention class"""

    schema = IntentionItemSchema
    parameters = ['comment', 'related_ideas']

    @classmethod
    def get_explanation_data(cls, args):
        """Return the value of the intention"""

        result = {}
        for (k, value) in args.items():
            if k in cls.parameters:
                try:
                    if isinstance(value, list):
                        listvalue = []
                        for val in value:
                            obj = get_obj(int(val), True)
                            if obj is None :
                                raise Exception()
 
                            listvalue.append(obj)

                        result[k] = listvalue

                    else:
                        obj = get_obj(int(value), True)
                        if obj is None :
                            raise Exception()
                       
                        result[k] = obj

                except Exception:
                    result[k] = value

        return result

    @classmethod
    def get_explanation_ideas(cls, args):
        """Return all related ideas"""
        data = cls.get_explanation_data(args)
        result = data['related_ideas']
        return result

    @classmethod
    def get_explanation_default_data(cls, args):
        """Return related ideas"""
        data = cls.get_explanation_data(args)
        data['related_ideas'] = data.pop('related_ideas')
        return data

    @classmethod
    def eq(cls, intention1, intention2):
        """Return True if intention1 has a relation with intention2"""
        if intention1['comment'] != intention2['comment']:
            return False

        related_ideas1 = list(intention1['related_ideas'])
        related_ideas2 = list(intention2['related_ideas'])
        related_ideas_eq = (len(related_ideas1) == len(related_ideas2)) and \
                     all((e in related_ideas2) for e in related_ideas1)
        if not related_ideas_eq:
            return False

        return True

    @classmethod
    def get_intention(cls, view):
        """Return the value of the intention from the view"""

        result = {}
        for param in cls.parameters:
            value = view.params(param)
            if value is None:
                value = []

            result[param] = value

        return result


class IntentionSchema(Schema):
    """Schema for Intention"""

    relatedexplanation = RelatedExplanationSchema(
                         widget=SimpleMappingWidget(
                                  css_class="explanations-bloc")
                         )

    intention = IntentionItemSchema(
                widget=SimpleMappingWidget(
                       css_class="intention-bloc")
                )


def context_is_a_amendment(context, request):
    return request.registry.content.istype(context, 'amendment')


class AmendmentSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for Amendment"""

    name = NameSchemaNode(
        editing=context_is_a_amendment,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=300),
        title=_("Abstract")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text")
        )


@content(
    'amendment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IAmendment)
class Amendment(Commentable,
                CorrelableEntity,
                SearchableEntity,
                DuplicableEntity,
                PresentableEntity):
    """Amendment class"""

    name = renamer()
    result_template = 'novaideo:views/templates/amendment_result.pt'
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'amendments')

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.explanations = PersistentDict()
        self.set_data(kwargs)

   # @region.cache_on_arguments() 
    def get_used_ideas(self):
        """Return used ideas"""

        result = []
        if not hasattr(self, 'explanations'):
            return result

        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                          Intention.get_explanation_ideas(
                             explanation['intention'])
                          )
                except Exception:
                    pass

        return list(set(result))

    @property
    def related_ideas(self):
        """Return added ideas"""

        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                        Intention.get_explanation_data(
                            explanation['intention'])['related_ideas']
                        )
                except Exception:
                    pass

        return list(set(result))

    @property
    def explanation(self):
        """Return all comments"""

        result = []
        values = sorted(list(self.explanations.values()),
                        key=lambda e: e['oid'])
        for explanation in values:
            if explanation['intention'] is not None:
                try:
                    result.append(
                        '<p>'+(Intention.get_explanation_data(
                            explanation['intention'])['comment'])+'</p>'
                        )
                except Exception:
                    pass

        if result:
            return '<div>'+"\n".join(list(set(result)))+'</div>'
    
        return ''

