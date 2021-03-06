# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    CorrectItem)
from novaideo.content.correction import Correction
from novaideo import _


@view_config(
    name='correctitem',
    context=Correction,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CorrectItemView(BasicView):
    title = _('Correct')
    name = 'correctitem'
    template = 'novaideo:views/proposal_management/templates/correction_text.pt'
    behaviors = [CorrectItem]
    viewid = 'correctitem'

    def update(self):
        item = self.params('item')
        vote = self.params('vote')
        content = self.params('content')
        self.execute({'item':item, 'vote':vote, 'content':content})
        result = {}
        user = get_current()
        values = {
                'title': self.context.get_adapted_title(get_current()), 
                'text': self.context.get_adapted_text(get_current()),
                'description': self.context.get_adapted_description(user),
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result
        

DEFAULTMAPPING_ACTIONS_VIEWS.update({CorrectItem:CorrectItemView})
