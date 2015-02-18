# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.processinstance.activity import ActionType
from pontus.view import BasicView

from novaideo.content.processes.novaideo_file_management.behaviors import (
    SeeFile)
from novaideo.core import  FileEntity
from novaideo.utilities.util import get_actions_navbar, navbar_body_getter


@view_config(
    name='seefile',
    context=FileEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeFileView(BasicView):
    title = ''
    name = 'seefile'
    behaviors = [SeeFile]
    template = 'novaideo:views/novaideo_file_management/templates/see_file.pt'
    viewid = 'seefile'

    def update(self):
        self.execute(None)
        result = {}
        def actions_getter():
            return [a for a in self.context.actions \
                   if a.action.actionType != ActionType.automatic]

        actions_navbar = get_actions_navbar(actions_getter, self.request,
                            ['global-action', 'text-action', 'admin-action'])
        actions_navbar['global-action'].extend(
                                          actions_navbar.pop('admin-action'))
        isactive = actions_navbar['modal-action']['isactive']
        messages = actions_navbar['modal-action']['messages']
        resources = actions_navbar['modal-action']['resources']
        values = {'object': self.context,
                  'navbar_body': navbar_body_getter(self, actions_navbar)}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result.update(resources)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeFile:SeeFileView})