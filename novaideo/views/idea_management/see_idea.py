# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.idea_management.behaviors import  SeeIdea
from novaideo.content.idea import Idea
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import get_actions_navbar, navbar_body_getter
from novaideo import _
from .present_idea import PresentIdeaView
from .comment_idea import CommentIdeaView
from .compare_idea import CompareIdeaView


_marker = object()


class DetailIdeaView(BasicView):
    title = _('Details')
    name = 'seeIdea'
    behaviors = [SeeIdea]
    template = 'novaideo:views/idea_management/templates/see_idea.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'seeidea'
    validate_behaviors = False

    def _cant_publish_alert(self, actions):
        #duplicated_text = getattr(getattr(self.context, 
        #                                  'originalentity', _marker),
        #                         'text', '')
        if 'to work' in self.context.state:
            return not any(a.action.behavior_id == 'publish' for a in actions)

        return False

    def update(self):
        self.execute(None) 
        user = get_current()
        files = getattr(self.context, 'attached_files', [])
        files_urls = []
        for file in files:
            files_urls.append({'title':file.title, 
                               'url':file.url(self.request)})

        def actions_getter():
            return [a for a in self.context.actions \
                   if getattr(a.action, 'style', '') == 'button']

        actions_navbar = get_actions_navbar(actions_getter, self.request,
                                ['global-action', 'text-action'])
        global_actions = actions_navbar['global-action']
        isactive = actions_navbar['modal-action']['isactive']
        messages = actions_navbar['modal-action']['messages']
        resources = actions_navbar['modal-action']['resources']
        result = {}
        values = {
                'idea': self.context,
                'state': get_states_mapping(user, self.context,
                                            self.context.state[0]),
                'current_user': user,
                'files': files_urls,
                'cant_publish': self._cant_publish_alert(global_actions),
                'navbar_body': navbar_body_getter(self, actions_navbar)
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result.update(resources)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class SeeIdeaActionsView(MultipleView):
    title = _('actions')
    name = 'seeiactionsdea'
    template = 'novaideo:views/idea_management/templates/panel_group.pt'
    views = (PresentIdeaView, CompareIdeaView, CommentIdeaView)

    def _activate(self, items):
        pass


@view_config(
    name='seeidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeIdeaView(MultipleView):
    title = ''
    name = 'seeidea'
    template = 'novaideo:views/templates/simple_mergedmultipleview.pt'
    views = (DetailIdeaView, SeeIdeaActionsView)
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/compare_idea.js',
                                'novaideo:static/js/comment.js']}
    validators = [SeeIdea.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeIdea:SeeIdeaView})