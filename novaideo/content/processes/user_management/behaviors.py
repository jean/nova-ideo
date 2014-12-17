# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service

from dace.util import getSite, name_chooser
from dace.objectofcollaboration.principal.util import (
    grant_roles, has_role, get_current)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IPerson
from novaideo.content.token import Token
from novaideo.mail import CONFIRMATION_MESSAGE, CONFIRMATION_SUBJECT
from novaideo import _
from novaideo.core import acces_action


def global_user_processsecurity(process, context):
    if has_role(role=('Admin',)):
        return True

    user = get_current()
    return 'active' in list(getattr(user, 'state', []))


def reg_roles_validation(process, context):
    return has_role(role=('Anonymous',))


class Registration(InfiniteCardinality):
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = reg_roles_validation

    def start(self, context, request, appstruct, **kw):
        person = appstruct['_object_data']
        root = context
        principals = find_service(root, 'principals')
        name = person.first_name + ' ' +person.last_name
        name = name_chooser(name=name)
        principals['users'][name] = person
        grant_roles(person, roles=('Member',))
        grant_roles(person, (('Owner', person),))
        person.state.append('active')
        localizer = request.localizer
        for i in range(root.tokens_mini):
            token = Token(title='Token_'+str(i))
            person.addtoproperty('tokens_ref', token)
            person.addtoproperty('tokens', token)
            token.setproperty('owner', person)

        message = CONFIRMATION_MESSAGE.format(
                    person=person,
                    user_title=localizer.translate(
                                   _(getattr(person, 'user_title', ''))),
                    login_url=request.resource_url(root, '@@login'))
        mailer_send(subject=CONFIRMATION_SUBJECT,
                recipients=[person.email], body=message)

        person.reindex()
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return 'active' in context.state


class Edit(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    title = _('Edit')
    submission_title = _('Save')
    context = IPerson
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        changepassword = appstruct['change_password']['changepassword']
        current_user_password = appstruct['change_password']['currentuserpassword']
        user = get_current()
        if changepassword and user.check_password(current_user_password):
            password = appstruct['change_password']['password']
            context.set_password(password)

        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        context.setproperty('keywords_ref', result)
        context.set_title()
        context.name = name_chooser(name=context.title)
        context.modified_at = datetime.datetime.today()
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def deactivate_roles_validation(process, context):
    return has_role(role=('Admin',))


def deactivate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def deactivate_state_validation(process, context):
    return 'active' in context.state


class Deactivate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    title = _('Deactivate')
    context = IPerson
    roles_validation = deactivate_roles_validation
    processsecurity_validation = deactivate_processsecurity_validation
    state_validation = deactivate_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('active')
        context.state.append('deactivated')
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def activate_roles_validation(process, context):
    return has_role(role=('Admin',))


def activate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def activate_state_validation(process, context):
    return 'deactivated' in context.state


class Activate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    title = _('Activate')
    context = IPerson
    roles_validation = activate_roles_validation
    processsecurity_validation = activate_processsecurity_validation
    state_validation = activate_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('deactivated')
        context.state.append('active')
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seeperson_processsecurity_validation(process, context):
    return True#'active' in context.state


@acces_action()
class SeePerson(InfiniteCardinality):
    title = _('Details')
    context = IPerson
    actionType = ActionType.automatic
    processsecurity_validation = seeperson_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
