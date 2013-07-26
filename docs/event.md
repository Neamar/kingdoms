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
Depuis un `pending_event` :
```python
new_pe = param.next_event("slug_new_event")
new_pe.start()
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
# On choisit de mettre en quarantaine tous les malades

#### Les solutions
* `on_fire` :

```python
# On a quand même quelques pertes, mais on en a sauvé pas mal !
kingdom.population *= 1.5
kingdom.save()
```

# On choisit de les laisser mourir
* `on_fire` :

```python
# C'est assez dramatique !
kingdom.population /= 2
kingdom.save()
```

# On choisit de faire appel à un medecin
* `on_fire` : 

```python
# On crée une nouvelle PendingMission
PendingMission(
	mission=Mission.objects.get(slug="recherche_medecin"),
	kingdom=kingdom,
).save()
```

### Lancer un évènement dans un futur programmé
```python
PendingEvent(
	event=Event.objects.get(slug="le slug"),
	kingdom=kingdom,
	started=datetime.now() + timedelta(days=5) # On peut aussi utiliser hours, minutes, months
	).save()

# La condition sur l'évènement sera déclenchée au moment programmé.
```

### Stocker des valeurs pour le nouvel évènement
```python
pe = PendingEvent(
	event=Event.objects.get(slug="le slug"),
	kingdom=kingdom,
	started=None # le pending event ne démarre pas maintenant
	).save()

# du code... par exemple, stocker une variable qui sera utile pour le futur évènement.

pe.start() # La mission démarre maintenant !
```
