
import datetime
import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import Schema
from pontus.view import BasicView

from novaideo.content.processes.ballot_processes.rangevoting.behaviors import (
    Vote)
from novaideo.content.proposal import Proposal
from novaideo import _


def define_date_node(schema):
    schema['vote'] = colander.SchemaNode(
            colander.DateTime(),
            widget=deform.widget.DateTimeInputWidget(),
            validator=colander.Range(min=datetime.datetime.today(),
                min_err=_('${val} is earlier than earliest datetime ${min}')),
            title=_('Date')
            )               
    

NODE_DEFINITION = {'date': define_date_node}


class VoteViewStudyReport(BasicView):
    title = _('Ballot report')
    name = 'ballotreport'
    template = 'novaideo:views/ballot_processes/referendum/templates/rangevoting_vote.pt'

    def update(self):
        result = {}
        ballot_report = None
        try:
            ballot_report = list(self.parent.children[1].behaviorinstances.values())[0].process.ballot.report
        except Exception:
            pass

        values = {'context': self.context, 'ballot_report': ballot_report}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class VoteSchema(Schema):

    vote = colander.SchemaNode(colander.String())
    

class VoteFormView(FormView):
    title =  _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    schema = VoteSchema()
    validate_behaviors = False

    def before_update(self):
        ballot_report = None
        vote_type = 'string'
        try:
            ballot_report = list(self.behaviorinstances.values())[0].process.ballot.report
            vote_type = ballot_report.ballottype.subject_type_manager.vote_type
        except Exception:
            pass

        define_node_op = NODE_DEFINITION.get(vote_type, None)
        if define_node_op:
            define_node_op(self.schema)
            



@view_config(
    name='rangevotingvote',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'rangevotingvote'
    viewid = 'rangevotingvote'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/ballot_processes/templates/panel_item.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Vote.get_validator()]

    def get_message(self):
        ballot_report = None
        try:
            ballot_report = list(self.children[1].behaviorinstances.values())[0].process.ballot.report
        except Exception:
            pass

        return ballot_report.ballot.title


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote:VoteViewMultipleView})