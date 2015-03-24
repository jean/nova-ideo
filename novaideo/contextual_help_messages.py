
from webob.multidict import NoVars
from pyramid.threadlocal import get_current_request

from dace.objectofcollaboration.principal.util import Anonymous, has_role

from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.proposal import Proposal
from novaideo.content.person import Person
from novaideo.content.idea import Idea
from novaideo.content.amendment import Amendment



def homepage_search(context, user):
    request = get_current_request()
    return not isinstance(request.POST, NoVars) or request.GET


def homepage_condition(context, user):
    return isinstance(user, Anonymous) and \
           not homepage_search(context, user)


def homepage_connected_condition(context, user):
    return not isinstance(user, Anonymous) and \
           not homepage_search(context, user)



def proposal_first_vote(context, user):
    return context.creator and getattr(context.creator, 'iteration', 1) == 1


def proposal_proofreading_started(context, user):
    corrections_in_process = [c for c in context.corrections \
                              if 'in process' in c.state]
    return corrections_in_process and \
           not(corrections_in_process[0].author is user)


def proposal_proofreading_started_owner(context, user):
    corrections_in_process = [c for c in context.corrections \
                              if 'in process' in c.state]
    return corrections_in_process and \
           corrections_in_process[0].author is user


def proposal_proofreading_not_started(context, user):
    corrections_in_process = [c for c in context.corrections \
                              if 'in process' in c.state]
    return not corrections_in_process


def amendment_draft_explanation(context, user):
    return 'draft' in context.state and \
           'explanation' in context.state 


def amendment_draft(context, user):
    return 'draft' in context.state and \
           'explanation' not in context.state 


CONTEXTUAL_HELP_MESSAGES = {
	(NovaIdeoApplication, 'any', ''): [
	   (homepage_condition, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/homepage_message.pt', 1),
	   (homepage_connected_condition, 'novaideo:views/templates/panels/'
	   	           'contextual_help_messages/homepage_connected_message.pt', 1),
	   (homepage_search, 'novaideo:views/templates/panels/'
	   	           'contextual_help_messages/homepage_search.pt', 2),
	   ],

	(NovaIdeoApplication, 'any', 'seemycontents'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemyparticipations'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemyselections'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemysupports'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'createidea'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/create_idea.pt', 1)],

	(Proposal, 'draft', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_draft.pt', 1)],

	(Proposal, 'amendable', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_amendable.pt', 1)],

	(Proposal, 'amendable', 'improveproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_improve.pt', 1)],

	(Proposal, 'any', 'editproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/edit_proposal.pt', 1)],

	(Proposal, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_sub_helps.pt', 2)],

	(Proposal, 'open to a working group', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_open_to_a_working_group.pt', 1)],

	(Proposal, 'proofreading', 'correctproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_proofreading_edit.pt', 1)],

	(Proposal, 'votes for publishing', 'index'): [
	   (proposal_first_vote, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_first_vote.pt', 1)],

	(Proposal, 'proofreading', 'index'): [
	   (proposal_proofreading_not_started, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_proofreading_not_started.pt', 1),
	   (proposal_proofreading_started_owner, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_proofreading_started_owner.pt', 1),
	   (proposal_proofreading_started, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_proofreading_started.pt', 1)],

	(Amendment, 'draft', 'index'): [
	   (amendment_draft, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_draft.pt', 1),
	   (amendment_draft_explanation, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_draft_explanation.pt', 1)],

	(Amendment, 'draft', 'submitamendment'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_prepare.pt', 1)],

	(Amendment, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_sub_helps.pt', 2)],

	(Person, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/person_index.pt', 1)],

	(Idea, 'to work', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_to_work.pt', 1)],
	   
	(Idea, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_sub_helps.pt', 2)],

        (Idea, 'to work', 'editidea'): [
           (None, 'novaideo:views/templates/panels/'
                          'contextual_help_messages/idea_to_work_edit.pt', 1)],

	(Idea, 'archived', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_archived.pt', 1)],

	(Idea, 'published', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_published.pt', 1)],

	(Idea, 'any', 'duplicateidea'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/duplicate_idea.pt', 1)],

	(Idea, 'any', 'publishasproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/transform_idea.pt', 1)],

}

