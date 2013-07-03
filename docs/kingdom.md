Documentation pour le scripting par Kingdom
=======================
![Kingdom models](https://github.com/Neamar/kingdoms/blob/master/kingdom/models.png?raw=true)

Vocabulaire des kingdoms
-----------------------
Un `kingdom` représente la dynastie d'un joueur : sa richesse, son prestige, sa population... il s'agit de l'objet central du jeu.

Les `folk` correspondent aux personnes de la cour d'un `kingdom`. Ils ont des attributs (strength, loyalty) qui les caractérisent, ainsi que des relations avec d'autres personnes : père, mère et époux.
Ils disposent aussi d'une liste de traits. Ces `quality` déterminent la personnalité du bonhomme.

Ce module définit aussi les `message`, qui correspondent à des logs d'importance variée, et les `modal_message` qui permettent d'afficher une boite de dialogue à l'utilisateur.

Enfin, les `claims` permettent de définir des relations entre les royaumes pour les guerres.

Où scripter ?
-------------
Aucun script par ici.


Que scripter ?
---------------

### Depuis un objet `Kingdom`
#### Ajouter un message

* `kingdom.message("message")` : ajoute un message pour le royaume spécifié.
* `kingdom.message("message", level)` : ajoute un message pour le royaume spécifié, du niveau indiqué par `level` (peut être `Message.TRIVIAL`, `Message.INFORMATION`, `Message.WARNING`, `Message.IMPORTANT` ou `Message.NUCLEAR`).


#### Ajouter un message modal
* `kingdom.modal_message(name, description)` : ajoute un message "modal" pour le royaume spécifié

#### Ajouter une claim
* `kingdom.add_claim(kingdom)` : ajoute une claim avec le `kingdom` défini

#### Connaitre la personne qui a un certain titre
* `kingdom.get_folk_in_title("title")` : renvoie le folk le la personne ayant ce titre. Si personne ne l'a, renvoie None

#### Débloquer un AvailableTitle
* `kingdom.unlock_title("title")` : débloque le titre(un string) (s'il ne l'était pas avant) et retourne ce titre (l'objet)

#### Savoir si un kingdom à une claim vers un autre kingdom
* `kingdom.offended_set.filter(kingdom=kingdom_cible).exists()`


### Depuis un objet `Folk`
#### Faire mourir quelqu'un
* `folk.die()` : tue la personne (et enregistre sa mort, pas besoin de `.save()`)

#### Ajouter un trait à une personne
* `folk.add_quality("quality")`: ajoute le trait `name` à la personne, puis retourne le trait ou `None` si l'affectation a échouée (par exemple, traits incompatibles)

#### Savoir si une personne a un certaint trait
* `folk.has_quality("quality")` : renvoie True si la personne a le trait sinon renvoie False

#### Connaitre l'age d'une personne
* `folk.age()`: renvoie l'age de la personne en années

#### Ajouter un titre à quelqu'un
* `folk.add_title("available_title")



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
