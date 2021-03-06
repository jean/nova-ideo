# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import (
    PresentProposal)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.mail import (
    PRESENTATION_PROPOSAL_MESSAGE, 
    PRESENTATION_PROPOSAL_SUBJECT)
from novaideo.views.idea_management.present_idea import (
    PresentIdeaView, 
    PresentIdeaSchema, 
    SentToView as IdeaSentToView)


class SentToView(IdeaSentToView):
    validators = [PresentProposal.get_validator()]
    template = 'novaideo:views/proposal_management/templates/sent_to.pt'


@colander.deferred
def default_subject(node, kw):
    context = node.bindings['context']
    return PRESENTATION_PROPOSAL_SUBJECT.format(subject_title=context.title)


@colander.deferred
def default_message(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    localizer = request.localizer
    url = request.resource_url(context, "@@index")
    user = get_current()
    return PRESENTATION_PROPOSAL_MESSAGE.format(
                recipient_title='',
                recipient_first_name='',
                recipient_last_name='',
                subject_url=url,
                subject_title=getattr(context, 'title', context.name),
                my_title=localizer.translate(_(getattr(user, 'user_title',''))),
                my_first_name=getattr(user, 'first_name', user.name),
                my_last_name=getattr(user, 'last_name',''),
                novaideo_title=request.root.title
                 )


class PresentProposalSchema(PresentIdeaSchema):

    subject =  colander.SchemaNode(
        colander.String(),
        default=default_subject,
        title=_('Subject'),
        )

    message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        default=default_message,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )


class PresentProposalFormView(FormView):

    title = _('Submit the proposal to others')
    schema = select(PresentProposalSchema(), 
                   ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentProposal]
    formid = 'formpresentproposalform'
    name = 'presentproposalform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='controled-form', 
                                              activable=True,
                                              button_css_class="pull-right",
                                              picto_css_class="glyphicon glyphicon-envelope",
                                              button_title=_("Present"))
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='presentproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PresentProposalView(PresentIdeaView):
    title = _('Submit the proposal to others')
    description = _('Submit the proposal to others')
    name = 'presentproposal'
    views = (SentToView, PresentProposalFormView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({PresentProposal:PresentProposalView})
