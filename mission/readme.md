Documentation pour le scripting par Mission
=======================

Vocabulaire des missions

Où scripter ?
-------------
### Depuis une mission
* `on_init` : ce code sera exécuté lorsqu'une mission sera créée pour un joueur donné. Le paramètre `param` contiendra la 


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


### Depuis un objet `Folk`
#### Faire mourir quelqu'un
* `folk.die()` : tue la personne

#### Ajouter un trait à une personne
* `folk.add_quality(name)`: ajoute le trait `name` à la personne, puis retourne le trait ou `None` si l'affectation a échouée (par exemple, traits incompatibles)

Exemples
-------------
### Ajout d'un message
On dispose déjà d'un objet Kingdom (disponible par défaut dans tous les scripts).

```python
# Ajout d'un message très important
kingdom.message("Vous avez perdu le jeu.", Message.NUCLEAR)

# Ajout d'un message rapide
kingdom.message("T'es nul !\nEt en plus tu pues.")
```

### Ajout d'un trait et modification des attributs
On dispose déjà d'un objet folk.

```python
# Ajouter le trait avare, qu'on suppose créé auparavant.
folk.add_quality("avare")      # /!\Le nom est sensible à la casse. avare =/= Avare.
# On diminue la loyauté de 15
folk.loyalty -= 15 
# On augmente la diplomatie de 2
folk.diplomacy += 2 
# On fixe l'érudition à 10
folk.scholarship = 10

# Ne surtout pas oublier d'appeler save(), sinon aucun enregistrement n'est effectué. 
folk.save()
```

### Création d'une claim entre kingdom
On dispose déjà d'un objet Kingdom (disponible par défaut dans tous les scripts).

```python
# Récupérer le kingdom ennemi
foe = Kingdom.objects.get(name="michael")

# Ajouter une claim du kingdom actuel vers l'ennemi
kingdom.add_claim(foe)    # Dorénavant, kingdom pourra attaquer foe.
```
