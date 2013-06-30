Documentation pour le scripting par Kingdom
=======================

Où scripter ?
-------------
Aucun script par ici.


Que scripter ?
---------------

### Depuis un objet `Kingdom`
#### Ajouter un message

* `kingdom.message(content)` : ajoute un message pour le royaume spécifié.
* `kingdom.message(content, level)` : ajoute un message pour le royaume spécifié, du niveau indiqué par `level` (peut être `Message.TRIVIAL`, `Message.INFORMATION`, `Message.WARNING`, `Message.IMPORTANT` ou `Message.NUCLEAR`).


#### Ajouter un message modal
* `kingdom.modal_message(name, description)` : ajoute un message "modal" pour le royaume spécifié
