Documentation pour le scripting par Mission
=======================
![Mission models](https://github.com/Neamar/kingdoms/blob/master/mission/models.png?raw=true)

Vocabulaire des missions
------------------------

Où scripter ?
-------------
### Depuis une mission
* `on_init` : ce code sera exécuté lorsqu'une mission sera créée pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours. Pour annuler cette mission, il faut renvoyer `status= "la raison de l'erreur"`.
* `on_start`
* `on_resolution`
* `target_list`

### Sur une grille
* `condition`


Que scripter ?
---------------


Exemples
-------------
