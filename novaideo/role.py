# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from dace.objectofcollaboration.principal.role import (
    Collaborator, Role, Administrator, role)


@role(name='Member',
      superiors=[Administrator],
      lowers=[Collaborator])
class Member(Role):
    pass


@role(name='Observer',
      superiors=[Administrator],
      lowers=[Collaborator],
      islocal=True)
class Observer(Role):
    pass


@role(name='Moderator',
      superiors=[Administrator],
      lowers=[Collaborator, Member])
class Moderator(Role):
    pass


@role(name='Examiner',
      superiors=[Administrator],
      lowers=[Collaborator, Member])
class Examiner(Role):
    pass


@role(name='Participant',
      superiors=[Administrator],
      lowers=[Collaborator, Observer],
      islocal=True)
class Participant(Role):
    pass


@role(name='Elector',
      islocal=True)
class Elector(Role):
    pass


@role(name='Certifier',
     superiors=[Administrator],
     lowers=[Collaborator])
class Certifier(Role):
    pass


DEFAULT_ROLES = ['Member']