# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    VotingAmendments)
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='votingamendments',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class VotingAmendmentsView(BasicView):
    title = _('Voting amendments')
    name = 'votingamendments'
    behaviors = [VotingAmendments]
    viewid = 'votingamendments'


    def update(self):
        results = self.execute(None)
        return results[0]
        

DEFAULTMAPPING_ACTIONS_VIEWS.update({VotingAmendments:VotingAmendmentsView})
