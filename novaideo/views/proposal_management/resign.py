from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import  Resign
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='resign',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class ResignView(BasicView):
    title = _('Resign')
    name = 'resign'
    behaviors = [Resign]
    viewid = 'resign'


    def update(self):
        self.execute(None)        
        return self.behaviorinstances.values()[0].redirect(self.context, self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({Resign:ResignView})