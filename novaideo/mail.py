# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

""" The contents of e-mails"""

PORTAL_SIGNATURE = """Cordialement,
                                                                                
La Plateforme {novaideo_title}
"""
PORTAL_PRESENTATION = u"""{novaideo_title} est une plateforme participative qui permet à tout membre d'initier des idées pouvant être utilisées dans des propositions améliorées par des groupes de travail. Une fois améliorées, ces propositions peuvent être soumises à l'appréciation des membres et faire l'objet d'une décision d'un comité d'examen.

"""

PRESENTATION_IDEA_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter l'idée « {subject_title} » figurant sur la plateforme {novaideo_title} sous {subject_url} .""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE

PRESENTATION_IDEA_SUBJECT = u"""« {subject_title} »""" 


CONFIRMATION_SUBJECT = u"""Confirmation de votre inscription sur la plateforme {novaideo_title}"""

CONFIRMATION_MESSAGE = u"""
Bonjour et bienvenue,

Vous êtes dorénavant inscrit sur la plateforme {novaideo_title}. L'accès à la plateforme se fait sous {login_url}. Une fois connecté avec votre identifiant (votre courriel) et votre mot de passe, vous pourrez noter une idée, accéder à vos éléments et intervenir sur une idée ou une proposition.

""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter la proposition « {subject_title} » figurant sur la plateforme {novaideo_title} sous {subject_url}.""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_SUBJECT = u"""« {subject_title} »""" 


PRESENTATION_AMENDMENT_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter l'amendement « {subject_title} » figurant sur la plateforme {novaideo_title} sous {subject_url}.

""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_SUBJECT = u"""« {subject_title} »"""


AMENDABLE_SUBJECT = u"""Début du cycle d'amélioration de la proposition « {subject_title} »"""


AMENDABLE_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Les participants au groupe de travail sur la proposition « {subject_title} » ont voté à la majorité pour l'amélioration de la proposition.

Un cycle d'amélioration commence, il comprend : la relecture de la proposition, son amélioration sous forme d'amendements, le vote sur ces amendements et le vote pour soumettre la proposition améliorée à l'appréciation des autres membres de la plateforme ou au contraire recommencer un nouveau cycle d'amélioration.

La fin de ce cycle d'amélioration est fixée au {duration}.

""" + PORTAL_SIGNATURE


PROOFREADING_SUBJECT = u"""Début du cycle d'amélioration de la proposition « {subject_title} »"""


PROOFREADING_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Les participants au groupe de travail sur la proposition « {subject_title} » ont voté à la majorité pour l'amélioration de la proposition.

Un cycle d'amélioration commence, il comprend : la relecture de la proposition, son amélioration sous forme d'amendements, le vote sur ces amendements et le vote pour soumettre la proposition améliorée à l'appréciation des autres membres de la plateforme ou au contraire recommencer un nouveau cycle d'amélioration.

La fin de ce cycle d'amélioration est fixée au {duration}.

""" + PORTAL_SIGNATURE


ALERT_SUBJECT = u"""Aucun amendement sur la proposition « {subject_title} »"""

ALERT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Alors que le cycle d'amélioration est terminé, aucun amendement n'a été soumis pour la proposition « {subject_title} » qui se trouve sous {subject_url}. Vous allez devoir procéder au vote pour soumettre la proposition en l'état ou pour commencer un nouveau cycle d'amélioration. 

""" + PORTAL_SIGNATURE

RESULT_VOTE_AMENDMENT_SUBJECT = u"""Les résultats du vote sur les amendements liés à la proposition « {subject_title} » """

RESULT_VOTE_AMENDMENT_MESSAGE = u"""
<div>
Bonjour {recipient_title} {recipient_last_name},

{message_result}
</div>
""" + PORTAL_SIGNATURE


PUBLISHPROPOSAL_SUBJECT = u"""Décision de soumettre en l'état la proposition « {subject_title} » à l'appréciation des membres de la plateforme"""

PUBLISHPROPOSAL_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Le groupe de travail sur la proposition « {subject_title} » qui se trouve sous {subject_url} a voté contre l'amélioration de la proposition.

En conséquence, la proposition est soumise en l'état à l'appréciation des membres de la plateforme. Chaque membre peut dorénavant soutenir ou s'opposer à la proposition.

""" + PORTAL_SIGNATURE


VOTINGPUBLICATION_SUBJECT = u"""Début des votes pour soumettre en l'état la proposition « {subject_title} » """

VOTINGPUBLICATION_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Les votes pour soumettre en l'état la proposition « {subject_title} » qui se trouve sous {subject_url} ont commencé. Merci de prendre part aux votes.

""" + PORTAL_SIGNATURE


VOTINGAMENDMENTS_SUBJECT = u"""Début des votes sur les amendements portant sur la proposition « {subject_title} »"""

VOTINGAMENDMENTS_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Les votes sur les amendements portant sur la proposition « {subject_title} » qui se trouve sous {subject_url} ont commencé. Merci de prendre part aux votes.

""" + PORTAL_SIGNATURE

WITHDRAW_SUBJECT = u"""Désinscription de la liste d'attente concernant la proposition « {subject_title} »"""

WITHDRAW_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Pour information, vous ne faites plus partie de la liste d'attente du groupe de travail de la proposition « {subject_title} » qui se trouve sous {subject_url}. 

""" + PORTAL_SIGNATURE

PARTICIPATE_SUBJECT = u"""Participation au groupe de travail sur la proposition « {subject_title} » """

PARTICIPATE_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Pour information, vous faites partie du groupe de travail sur la proposition {subject_title} qui se trouve sous {subject_url}. Dès que le groupe de travail a atteint trois participants, vous pourrez participer aux votes pour soumettre la proposition en l'état ou au contraire commencer un cycle d'amélioration.

""" + PORTAL_SIGNATURE

RESIGN_SUBJECT = u"""Démission du groupe de travail sur la proposition « {subject_title} » """

RESIGN_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous avez décidé de quitter le groupe de travail sur la proposition « {subject_title} » qui se trouve sous {subject_url}. S'il est ouvert, vous pourrez décider de le rejoindre de nouveau en cliquant sur l'action "Participer".

""" + PORTAL_SIGNATURE

WATINGLIST_SUBJECT = u"""Participation au groupe de travail sur la proposition « {subject_title} »"""

WATINGLIST_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Pour information, vous faites partie de la liste d'attente du groupe de travail sur la proposition « {subject_title} » qui se trouve sous {subject_url}. Si le groupe de travail atteint moins de 12 personnes et si le ne vous faites pas partie de plus de 5 groupes de travail, vous y serez immédiatement ajouté en tant que participant. 

""" + PORTAL_SIGNATURE


NEWCONTENT_SUBJECT = u"""Un contenu vient d'être publié"""


NEWCONTENT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

{subject_type} « {subject_title} » qui contient un des mots clés faisant partie de vos centres d'intérêt vient d'être publiée. Vous pouvez la consulter sous {subject_url}

"""+ PORTAL_SIGNATURE


PROPOSALREMOVED_SUBJECT = u"""Suppression de la proposition « {subject_title} »"""

PROPOSALREMOVED_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

La proposition « {subject_title} » viens d'être supprimée par les modérateurs pour le motif suivant.
{explanation}

"""+ PORTAL_SIGNATURE 

RESETPW_SUBJECT = u"""Votre nouveau mot de passe sur la plateforme {novaideo_title}"""


RESETPW_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous avez oublié votre mot de passe sur la plateforme {novaideo_title} et vous souhaitez en utiliser un nouveau, merci de cliquer sur {reseturl} et de saisir votre nouveau mot de passe.

"""+ PORTAL_SIGNATURE
