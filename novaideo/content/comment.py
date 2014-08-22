import colander
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import CompositeMultipleProperty, SharedUniqueProperty
from dace.util import getSite
from pontus.core import VisualisableElementSchema
from pontus.widget import SequenceWidget, FileWidget, Select2Widget
from pontus.file import ObjectData, File
from pontus.schema import Schema, omit

from .interface import IComment
from novaideo.core import Commentable
from novaideo import _


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.comment_intentions)
    values = [(i, i) for i in intentions ]
    return Select2Widget(values=values)


def context_is_a_comment(context, request):
    return request.registry.content.istype(context, 'comment')


class CommentSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_comment,
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        )


@content(
    'comment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IComment)
class Comment(Commentable):
    name = renamer()
    author = SharedUniqueProperty('author')

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def subject(self):
        if not isinstance(self.__parent__, Comment):
            return self.__parent__
        else:
            return self.__parent__.subject 


class AddCommentSchema(Schema):

    comment = omit(CommentSchema(factory=Comment,
                                 editable=True,
                                 name=_('Comment')), ['_csrf_token_'])
