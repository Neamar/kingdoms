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

Que scripter ?
---------------
#### Définir une variable pour un texte :
Depuis n'importe quel script du module (`condition`, et les deux `on_fire`) :
```python
# On peut stocker un entier (0, 1, 50),
# une chaîne de caractères (taille maximale de 500 caractères)
# ou un object de la base, par exemple un Folk ou un Kingdom.
param.set_value("variable_name", "variable_value")
```

#### Récupérer une variable
Depuis n'importe quel script du module (`condition`, et les deux `on_fire`) :
```python
param.get_value("variable_name")
```
Attention, la variable doit forcément exister.


#### Créer un nouveau PendingEvent en gardant les variables
Depuis un `pendingEvent` ou un `pendingEventAction` :
```python
pe = param.next_event("slug_new_event")
pe.start()
```

Exemples
-------------
### Épidemie
#### L'évènement
* `condition` :

```python
# Si le royaume est trop riche, il dispose des conditions sanitaires suffisantes pour en être exempté.
if param.money > 100:
	status="trop riche"
```

* `on_fire` :

```python
kingdom.population /= 1.5
# La population diminue dès le début
kingdom.save()
# On n'oublie pas de sauvegarder
```


#### Les résolutions
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
* `on_fire` : 

```python
# On crée une nouvelle PendingMission
kingdom.create_pending_mission("recherche_medecin")
```

### Lancer un évènement dans un futur programmé
```python
pe = kingdom.create_pending_event("event_slug")
pe.started=datetime.now() + timedelta(days=5) # On peut aussi utiliser hours, minutes, months
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
# Retourne un PendingEvent .save(), mais pas encore .start()
# Exemple :
kingdom.start_pending_event("slug")
```

### Méthode 4 : À NE PAS UTILISER.

```python
# Cette méthode est lourde, trop longue à taper et utilise des APIs qui n'ont pas forcément de raisons d'être exposées (le started=None)
# Utilité : aucune ! Si vous en voyez dans les scripts, n'hésitez pas à remplacer avec une forme plus moderne.
# Exemple :
PendingEvent(event=Event.objects.get(slug="slug"), kingdom=kingdom, started=None) # À NE PLUS UTILISER
```
