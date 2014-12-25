# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role, get_current, has_any_roles)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from novaideo.content.interface import INovaIdeoApplication, IProposal
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import acces_action


@acces_action()
class Search(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    actionType = ActionType.automatic

    def start(self, context, request, appstruct, **kw):
        content_types = appstruct['content_types']
        text = appstruct['text_to_search']
        return {'content_types': content_types,
                'text': text}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(
                  request.resource_url(root, 
                        query={'text_to_search': kw['text'],
                               'content_types': ",".join(kw['content_types'])}))


def seemy_roles_validation(process, context):
    return has_role(role=('Member',))


def seemyc_processsecurity_validation(process, context):
    user = get_current()
    contents = [o for o in getattr(user, 'contents', []) \
                if not('archived' in o.state)]
    return contents and global_user_processsecurity(process, context)

class SeeMyContents(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemyc_processsecurity_validation

    def contents_nb(self):
        user = get_current()
        return len([o for o in getattr(user, 'contents', []) \
                    if not('archived' in o.state)])

    def start(self, context, request, appstruct, **kw):
        return {}

def seemys_processsecurity_validation(process, context):
    user = get_current()
    selections = [o for o in getattr(user, 'selections', []) \
                  if not('archived' in o.state)]
    return selections and global_user_processsecurity(process, context)


class SeeMySelections(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemys_processsecurity_validation

    def contents_nb(self):
        user = get_current()
        return len([o for o in getattr(user, 'selections', []) \
                    if not('archived' in o.state)])

    def start(self, context, request, appstruct, **kw):
        return {}


def seemypa_processsecurity_validation(process, context):
    user = get_current()
    return getattr(user, 'participations', []) and \
                   global_user_processsecurity(process, context)


class SeeMyParticipations(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemypa_processsecurity_validation


    def contents_nb(self):
        user = get_current()
        return len(getattr(user, 'participations', []))

    def start(self, context, request, appstruct, **kw):
        return {}


def seemysu_processsecurity_validation(process, context):
    user = get_current()
    supports = [o for o in getattr(user, 'supports', []) \
                if not('archived' in o.state)]
    return supports and global_user_processsecurity(process, context)


class SeeMySupports(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemysu_processsecurity_validation

    def contents_nb(self):
        user = get_current()
        len_supports = len([o for o in getattr(user, 'supports', []) \
                            if not('archived' in o.state)])
        return str(len_supports)+'/'+str(len(getattr(user, 'tokens_ref', [])))

    def start(self, context, request, appstruct, **kw):
        return {}


def seeproposal_processsecurity_validation(process, context):
    return not ('draft' in context.state) or \
           has_role(role=('Owner', context))
           

@acces_action()
class SeeProposal(InfiniteCardinality):
    title = _('Details')
    context = IProposal
    actionType = ActionType.automatic
    processsecurity_validation = seeproposal_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors
