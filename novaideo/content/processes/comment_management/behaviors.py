# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the 
Comment management process definition. 
"""
from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.activity import InfiniteCardinality

from novaideo.content.interface import IComment
from novaideo import _


VALIDATOR_BY_CONTEXT = {}


def respond_relation_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.relation_validation.__func__(process, subject)
    except Exception:
        return True


def respond_roles_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.roles_validation.__func__(process, subject)
    except Exception:
        return True


def respond_processsecurity_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.processsecurity_validation.__func__(process, subject)
    except Exception:
        return True


def respond_state_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.state_validation.__func__(process, subject)
    except Exception:
        return True


class Respond(InfiniteCardinality):
    title = _('Replay')
    access_controled = True
    context = IComment
    relation_validation = respond_relation_validation
    roles_validation = respond_roles_validation
    processsecurity_validation = respond_processsecurity_validation
    state_validation = respond_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        return {'newcontext': comment.subject}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], '@@index'))


#TODO behaviors