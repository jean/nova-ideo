# -*- coding: utf8 -*-
import datetime
from datetime import timedelta
from pyramid.httpexceptions import HTTPFound

from dace.util import (
    getSite,
    getBusinessAction,
    copy,
    find_entities)
from dace.objectofcollaboration.principal.util import has_any_roles, grant_roles, get_current, revoke_roles
from dace.processinstance.activity import InfiniteCardinality, ActionType, LimitedCardinality, ElementaryAction

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IProposal, ICorrelableEntity
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import PRESENTATION_PROPOSAL_MESSAGE, PRESENTATION_PROPOSAL_SUBJECT
from novaideo import _
from novaideo.content.proposal import Proposal
from ..comment_management.behaviors import validation_by_context
from novaideo.core import acces_action
from novaideo.content.correlation import Correlation
from novaideo.content.idea import Idea
from novaideo.content.amendment import Amendment
from novaideo.content.working_group import WorkingGroup
from novaideo.content.ballot import Ballot
from novaideo.content.processes.idea_management.behaviors import PresentIdea, Associate as AssociateIdea


try:
      basestring
except NameError:
      basestring = str


def createproposal_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def createproposal_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class CreateProposal(ElementaryAction):
    context = INovaIdeoApplication
    roles_validation = createproposal_roles_validation
    processsecurity_validation = createproposal_processsecurity_validation

    def _associate(self, related_ideas, proposal):
        root = getSite()
        datas = {'author': get_current(),
                 'source': proposal,
                 'comment': '',
                 'intention': 'Creation'}
        for idea in related_ideas:
            correlation = Correlation()
            datas['targets'] = [idea]
            correlation.set_data(datas)
            correlation.tags.extend(['related_proposals', 'related_ideas'])
            correlation.type = 1
            root.addtoproperty('correlations', correlation)
            proposal.text = getattr(proposal, 'text', '') + '<div>'+idea.text+'</div>'

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        related_ideas = appstruct.pop('related_ideas')
        
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        proposal = appstruct['_object_data']
        root.addtoproperty('proposals', proposal)
        proposal.setproperty('keywords_ref', result)
        proposal.state.append('draft')
        grant_roles(roles=(('Owner', proposal), ))
        grant_roles(roles=(('Participant', proposal), ))
        proposal.setproperty('author', get_current())
        self.process.execution_context.add_created_entity('proposal', proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        if related_ideas:
            self._associate(related_ideas, proposal)

        self.newcontext = proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def submit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def submit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def submit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def submit_state_validation(process, context):
    return "draft" in context.state


class SubmitProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = submit_relation_validation
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation


    def start(self, context, request, appstruct, **kw):
        context.state.remove('draft')
        root = getSite()
        if root.participants_mini > 1:
            context.state.append('open to a working group')
        else:
            context.state.append('votes for publishing')
        
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

def duplicate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           not ('draft' in context.state)


class DuplicateProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_proposal = copy(context)
        copy_of_proposal.created_at = datetime.datetime.today()
        copy_of_proposal.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        copy_of_proposal.set_data(appstruct)
        root.addtoproperty('proposals', copy_of_proposal)
        copy_of_proposal.setproperty('originalentity', context)
        copy_of_proposal.state = ['draft']
        copy_of_proposal.setproperty('author', get_current())
        grant_roles(roles=(('Owner', copy_of_proposal), ))
        self.newcontext = copy_of_proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def edit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def edit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return "draft" in context.state


class EditProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        context.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        datas = {'keywords_ref': result}
        context.set_data(datas)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

def pub_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')

def pub_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),)) #System

def pub_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'votes for publishing' in context.state


class PublishProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    roles_validation = pub_roles_validation
    relation_validation = pub_relation_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO wg desactive, members vide...
        context.state.remove('votes for publishing')
        context.state.append('published')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def comm_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return  not('draft' in context.state)


class CommentProposal(InfiniteCardinality):
    isSequential = False
    context = IProposal
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def edita_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def edita_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def edita_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           context.amendments


class EditAmendments(InfiniteCardinality):
    isSequential = False
    context = IProposal
    relation_validation = edita_relation_validation
    roles_validation = edita_roles_validation
    processsecurity_validation = edita_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def present_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return not ('draft' in context.state) #TODO ?


class PresentProposal(PresentIdea):
    context = IProposal
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


def associate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def associate_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def associate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           (has_any_roles(roles=(('Owner', context),)) or \
           (has_any_roles(roles=('Member',)) and not ('draft' in context.state)))

class Associate(AssociateIdea):
    context = IProposal
    processsecurity_validation = associate_processsecurity_validation
    roles_validation = associate_roles_validation
    relation_validation = associate_relation_validation


def improve_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def improve_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def improve_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def improve_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class ImproveProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = improve_relation_validation
    roles_validation = improve_roles_validation
    processsecurity_validation = improve_processsecurity_validation
    state_validation = improve_state_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        data = {}
        data['title'] = appstruct['title']
        data['text'] = appstruct['text']
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        data['keywords_ref'] = result
        data['description'] = appstruct['description']
        data['comment'] = appstruct['confirmation']['comment']
        data['intention'] = appstruct['confirmation']['intention']
        not_identified = appstruct['confirmation']['replaced_idea']['not_identified']
        new_idea = appstruct['confirmation']['idea_of_replacement']['new_idea']
        amendment = Amendment()
        self.newcontext = amendment
        if not not_identified:
            data['replaced_idea'] = appstruct['confirmation']['replaced_idea']['replaced_idea']

        if not new_idea:
            data['idea_of_replacement'] = appstruct['confirmation']['idea_of_replacement']['idea_of_replacement']
        else:
            newidea = Idea(title='Idea for '+context.title)
            root.addtoproperty('ideas', newidea)
            newidea.state.append('to work')
            grant_roles(roles=(('Owner', newidea), ))
            newidea.setproperty('author', get_current())
            data['idea_of_replacement'] = newidea
            self.newcontext = newidea

        amendment.set_data(data)
        context.addtoproperty('amendments', amendment)
        amendment.state.append('draft')
        grant_roles(roles=(('Owner', amendment), ))
        amendment.setproperty('author', get_current())
        return True

    def redirect(self, context, request, **kw):
        if isinstance(self.newcontext, Amendment):
            return HTTPFound(request.resource_url(context, "@@index"))
        else:
            return HTTPFound(request.resource_url(self.newcontext, "@@editidea"))


def correct_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def correct_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def correct_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def correct_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class CorrectProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = correct_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class AddParagraph(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = correct_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def decision_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def decision_roles_validation(process, context):
     #has_first_decision = hasattr(process, 'first_decision')
     #return (has_first_decision and has_any_roles(roles=(('Participant', context),))) or \
     #       (has_first_decision and has_any_roles(roles=('System',)))
    return has_any_roles(roles=('Member',))


def decision_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class VotingPublication(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = decision_relation_validation
    roles_validation = decision_roles_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('amendable')
        context.state.append('votes for publishing')
        return True


    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdraw_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def withdraw_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def withdraw_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and user in context.working_group.wating_list


def withdraw_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state


class Withdraw(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = withdraw_relation_validation
    roles_validation = withdraw_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation
    state_validation = withdraw_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        wg = context.working_group
        wg.delproperty('wating_list', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def resign_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def resign_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def resign_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def resign_state_validation(process, context):
    return  'amendable' in context.state or 'open to a working group' in context.state #TODO


class Resign(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = resign_relation_validation
    roles_validation = resign_roles_validation
    processsecurity_validation = resign_processsecurity_validation
    state_validation = resign_state_validation

    def _get_next_user(self, users, root):
        for user in users:
            if 'active' in user.state and len(user.working_groups) < root.participations_maxi:
                return user

        return None 

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        wg.delproperty('members', user)
        revoke_roles(user, (('Participant', context),))
        if wg.wating_list:
            next_user = self._get_next_user(wg.wating_list, root)
            if next_user is not None:
                wg.delproperty('wating_list', next_user)
                wg.addtoproperty('members', next_user)
                grant_roles(next_user, (('Participant', context),))
                #TODO send mail to next_user

        participants = wg.members
        len_participants = len(participants)
        if len_participants < root.participants_mini:
            context.state = ['open to a working group']
            wg.state = ['deactivated']

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def participate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def participate_roles_validation(process, context):
    return has_any_roles(roles=('Member',)) and not has_any_roles(roles=(('Participant', context),))


def participate_processsecurity_validation(process, context):
    user = get_current()
    root = getSite()
    return global_user_processsecurity(process, context) and \
           not(user in context.working_group.wating_list) and \
           len(user.working_groups) < root.participations_maxi 


def participate_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state or 'open to a working group' in context.state


class Participate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = participate_relation_validation
    roles_validation = participate_roles_validation
    processsecurity_validation = participate_processsecurity_validation
    state_validation = participate_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        participants = wg.members
        len_participants = len(participants)
        if len_participants < root.participants_maxi:
            wg.addtoproperty('members', user)
            grant_roles(user, (('Participant', context),))
            if (len_participants+1) == root.participants_mini:
                context.state = [] #remove('open to a working group')
                wg.state = ['active']
                if not hasattr(self.process, 'first_decision'):
                    self.process.first_decision = True

                context.state.append('amendable')
        else:
            wg.addtoproperty('wating_list', user)
 
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def va_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def va_roles_validation(process, context):
    #return has_any_roles(roles=('System',))
    return has_any_roles(roles=('Member',))


def va_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class VotingAmendments(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = va_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('amendable')
        context.state.append('votes for amendments')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def ar_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'votes for amendments' in context.state


class AmendmentsResult(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = ar_state_validation

    def start(self, context, request, appstruct, **kw):
        result = set()
        for ballot in self.process.amendments_ballots:
            result.update(ballot.report.get_electeds())

        #TODO merg result
        context.state.remove('votes for amendments')
        context.state.append('amendable')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def ta_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'votes for publishing' in context.state


class Amendable(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = ta_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('votes for publishing')
        context.state.append('amendable')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors

validation_by_context[Proposal] = CommentProposal
