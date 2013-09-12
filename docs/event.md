Documentation pour le scripting par Event
=======================
![Event models](https://github.com/Neamar/kingdoms/blob/master/event/models.png?raw=true)

Vocabulaire des évènements
------------------------

Où scripter ?
-------------
### Depuis un event
* `condition` : ce code détermine les conditions pour que l'event puisse apparaître
* `on_fire` : ce code est executé lorque l'event est déclanché

## Depuis un event action
* `on_fire` : ce code est executé lorsque le joueur choisit cette action
* `condition` : ce code détermine les conditions pour que le bouton associé à l'event action puisse apparaître

Que scripter ?
---------------
#### Définir une variable pour un texte :
Depuis n'importe quel script du module (les deux `condition`, et les deux `on_fire`) :
```python
# On peut stocker un entier (0, 1, 50),
# une chaîne de caractères (taille maximale de 500 caractères)
# ou un objet de la base, par exemple un Folk ou un Kingdom.
param.set_value("variable_name", "variable_value")
```

#### Récupérer une variable
Depuis n'importe quel script du module (les deux `condition`, et les deux `on_fire`) :
```python
param.get_value("variable_name")
```
Si la variable n'existe pas, `get_value` retourne `None`. Il est possible de modifier cette valeur par défaut en passant un second argument, par exemple `param.get_value("variable_name", False)`.


#### Créer un nouveau PendingEvent en gardant les variables
Depuis un `PendingEvent` ou un `PendingEventAction` :

```python
pe = param.next_event("slug_new_event")
pe.start()
```

Ce code transfère toutes les variables sur le `PendingEvent` actuel vers le nouveau `PendingEvent`.

#### Créer un nouveau PendingEvent en ajoutant les variables
Depuis n'importe quel script (y compris en dehors du module `event`) :

```python
pe = kingdom.create_pending_event("slug_new_event")
pe.set_value("variable_name", "variable_value")
pe.start()
```

#### Créer un nouveau PendingEvent sans ajouter ni garder de variables
Depuis n'importe quel script (y compris en dehors du module `event`) :

```python
kingdom.start_pending_event("slug")
```

Cette fonction lance directement un nouveau `PendingEvent`. Il n'y a pas besoin d'appeler `.start()`, cependant il n'est pas possible de définir des variables.

Exemples
-------------
### Épidemie
Réalisons un évènement Épidémie, qui ne frappe que les royaumes pauvres et diminue la population.

#### L'évènement
* `condition` :

```python
# Si le royaume est trop riche, il dispose des conditions sanitaires suffisantes pour être épargné
if kingdom.money > 100:
	status="trop riche"
```
Le fait de renvoyer un `status` (n'importe quelle valeur différente de `ok`) suffit à annuler l'évènement.

* `on_fire` :
Ce code est exécuté si la condition ne modifie pas le `status`.

```python
kingdom.population /= 1.5
# La population diminue
kingdom.save()
# On n'oublie pas de sauvegarder, sinon l'objet n'est pas enregistré en base de données.
```

#### Les actions
On définit autant d'actions que l'on souhaite afficher de boutons.
##### On choisit de mettre en quarantaine tous les malades

* `on_fire` :

```python
# On a quand même quelques pertes, mais on en a sauvé pas mal !
kingdom.population *= 1.5
kingdom.save()
```

##### On choisit de les laisser mourir
* `on_fire` :

```python
# C'est assez dramatique !
kingdom.population /= 2
kingdom.save()
```

##### On choisit de faire appel à un medecin
* `condition` : 
```python
if kingdom.get_folk_in_title("cure") is None:
	status = "il n'y pas a de medecin" # Cette option ne s'affichera pas dans les choix
```

* `on_fire` : 

```python
# On crée une nouvelle PendingMission
kingdom.create_pending_mission("recherche_medecin")
```

### Lancer un évènement dans un futur programmé
```python
pe = kingdom.create_pending_event("event_slug")
pe.started = datetime.now() + timedelta(days=5) # On peut aussi utiliser hours, minutes, months...
pe.save()

# La condition sur l'évènement sera déclenchée au moment programmé.
```

### Stocker des valeurs pour le nouvel évènement
```python
pe = kingdom.create_pending_event("event_slug")

# du code... par exemple, stocker une variable qui sera utile pour le futur évènement.
pe.set_value("foo", "bar")

pe.start() # L'évènement démarre maintenant !
```

Récapitulatif des méthodes pour créer un `PendingEvent`
-------------------------------------------------------

### Méthode 1 : créer et faire suivre les paramètres.

```python
# Utilité : dupliquer des paramètres vers un nouveau PendingEvent.
# Méthode uniquement accessible depuis un PendingEvent ou un PendingEventAction.
# Retourne un PendingEvent .save(), avec les valeurs précédentes, mais pas encore .start()
# Exemple :
pe = param.next_event("slug")
pe.start()
```

### Méthode 2 : créer pour ajouter des paramètres.

```python
# Utilité : créer un PendingEvent et y ajouter des paramètres.
# Méthode accessible depuis n'importe quel objet Kingdom.
# Retourne un PendingEvent .save(), mais pas encore .start()
# Exemple :
pe = kingdom.create_pending_event("slug")
pe.set_value("foo", "bar")
pe.start()
```

### Méthode 3 : créer directement.
```python
# Utilité : lancer directement un PendingEvent sans paramètres.
# Méthode accessible depuis n'importe quel objet Kingdom.
# Retourne un PendingEvent .save() et .start()
# Exemple :
kingdom.start_pending_event("slug")
```
