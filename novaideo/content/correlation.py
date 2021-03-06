# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from zope.interface import implementer
from persistent.list import PersistentList

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import SharedUniqueProperty, SharedMultipleProperty
from dace.util import find_entities, getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.core import VisualisableElementSchema
from pontus.widget import Select2Widget
from pontus.file import Object as ObjectType

from .interface import ICorrelation, ICorrelableEntity
from novaideo.core import Commentable, can_access
from novaideo import _


class CorrelationType:
    weak = 0
    solid = 1


@colander.deferred
def targets_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    values = []
    entities = find_entities([ICorrelableEntity], 
        states=('archived',), not_any=True)
    values = [(i, i.title) for i in entities \
              if can_access(user, i, request, root)] #i.actions
    values.remove((context, context.title))
    values = sorted(values, key=lambda p: p[1])
    return Select2Widget(values=values, multiple=True, min_len=1)


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.correlation_intentions)
    values = [(i, i) for i in intentions ]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


def context_is_a_correlation(context, request):
    return request.registry.content.istype(context, 'correlation')


class CorrelationSchema(VisualisableElementSchema):
    """Schema for correlation"""

    name = NameSchemaNode(
        editing=context_is_a_correlation,
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=500),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_("Message")
        )

    targets = colander.SchemaNode(
        ObjectType(),
        widget=targets_choice,
        validator = colander.Length(min=1),
        title=_('Targets'),
        )


@content(
    'correlation',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICorrelation)
class Correlation(Commentable):
    """Correlation class"""
    name = renamer()
    source = SharedUniqueProperty('source', 'source_correlations')
    targets = SharedMultipleProperty('targets', 'target_correlations')
    author = SharedUniqueProperty('author')

    def __init__(self, **kwargs):
        super(Correlation, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.type = CorrelationType.weak
        self.tags = PersistentList()

    @property
    def ends(self):
        """Return the ends of the correlation"""
        result = list(self.targets)
        result .append(self.source) 
        return result
