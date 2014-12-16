# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.events import subscriber

from substanced.event import RootAdded
from substanced.util import find_service

from novaideo.core import FileEntity
from novaideo.utilities.util import send_alert_new_content
from novaideo.event import ObjectPublished


@subscriber(RootAdded)
def mysubscriber(event):
    """Add the novaideo catalog when the root is added."""
    root = event.object
    catalogs = find_service(root, 'catalogs')
    catalogs.add_catalog('novaideo')
    ml_file = FileEntity()
    ml_file.__name__ = 'ml_file'
    root.addtoproperty('files', ml_file)
    root.ml_file = ml_file
    terms_of_use = FileEntity()
    terms_of_use.__name__ = 'terms_of_use'
    root.addtoproperty('files', terms_of_use)
    root.terms_of_use = terms_of_use
    #registry = get_current_registry()
    #settings = registry.settings
    #login = settings.get('ineus.initial_login')
    #password = settings.get('ineus.initial_password')
    #admin = Person(password=password, email=login)
    #admin.__name__ = 'ineus_admin'
    #principals = find_service(root, 'principals')
    #principals['users'][admin.__name__] = admin
    #grant_roles(user=admin, roles=('Admin',))


@subscriber(ObjectPublished)
def mysubscriber_object_published(event):
    published_object = event.object
    send_alert_new_content(published_object)