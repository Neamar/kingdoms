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

#### Ajouter une claim
* `kingdom.add_claim(kingdom)` : ajoute une claim avec le `kingdom` défini


### depuis un objet `Folk`
#### Faire mourir quelqu'un
* `folk.die()` : Tue la personne

#### Ajouter un trait à une personne
* `folk.add_quality(name)`: ajoute le trait name à la personne

Exemple
-------------
###ajout d'un trait et diminution d'un attribut
####On dispose déjà d'un objet folk
```python
folk.add_quality("avare")      #/!\Le nom est sensible à la casse. avare =/= Avare.
#on diminue la loyalty de 15
folk.loyalty -= 15 
#on augmente la diplomacie de 2
folk.diplomacy += 2 
# on fixe le scholarship à 10
folk.scholarship = 10 
folk.save()
```

### ajout d'un message
####on dispose déjà d'un objet Kingdom
```pyton
#ajoute un message d'une certainte prorité
kingdom.message("vous avez perdu la partie", Message.NUCLEAR)
#ajoute un message sans priorité (celle ci sera alors une INFORMATION)
kingdom.message("t'es nul")
```

###creation d'une claim entre kingdom
####on dispose déjà d'un objet kingdom
```python
kingdom.add_claim(autre_kingdom)    #le kingdoms que l'on avait avant est l'attaquant, celui passé en paramètre est l'attaqué
```