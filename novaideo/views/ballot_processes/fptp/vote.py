# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.entity import Entity
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import Schema
from pontus.widget import Select2Widget

from novaideo.content.processes.ballot_processes.fptp.behaviors import  Vote
from novaideo.content.proposal import Proposal
from novaideo import _


class VoteViewStudyReport(BasicView):
    title = _('FPTP vote')
    name = 'votefptp'
    template = 'novaideo:views/ballot_processes/fptp/templates/fptp_vote.pt'

    def update(self):
        result = {}
        ballot_report = None
        try:
            voteform_view = self.parent.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            ballot_report = voteform_actions[0].process.ballot.report
        except Exception:
            pass

        values = {'context': self.context, 'ballot_report': ballot_report}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result



def subjects_choice(ballot_report):
    subjects = ballot_report.subjects
    def get_title(ob):
        if isinstance(ob, Entity):
            return ob.title
        else:
            return _(ob)

    values = [(i, get_title(i)) for i in subjects]
    return Select2Widget(values=values)



class CandidatesSchema(Schema):

    elected = colander.SchemaNode(
            colander.String(),
            title=_('Choices'),
            default=[],
        )
    

class VoteFormView(FormView):
    title =  _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    validate_behaviors = False
    schema = CandidatesSchema()

    def before_update(self):
        ballot_report = None
        try:
            vote_actions = list(self.behaviors_instances.values())
            ballot_report = vote_actions[0].process.ballot.report
        except Exception:
            return

        subjects_widget = subjects_choice(ballot_report)
        self.schema.get('elected').widget = subjects_widget
        self.schema.view = self


@view_config(
    name='votefptp',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'votefptp'
    viewid = 'votefptp'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/ballot_processes/templates/panel_item.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Vote.get_validator()]

    def get_message(self):
        ballot_report = None
        try:
            voteform_view = self.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            ballot_report = voteform_actions[0].process.ballot.report
        except Exception:
            pass

        return ballot_report.ballot.title


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote:VoteViewMultipleView})
