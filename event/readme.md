Documentation pour le scripting par Event
=======================
![Event models](https://github.com/Neamar/kingdoms/blob/master/event/models.png?raw=true)

Vocabulaire des évènements
------------------------

Où scripter ?
-------------
### Depuis un event
* `condition` : ce code determine les conditions pour que l'event puisse apparaître
* `on_fire` : ce code est executé lorque l'event est déclanché

## Depuis un event action
*`on_fire` : ce code est executé lorsque le joueur choisi cette action

Que scripter ?
---------------


Exemples
-------------
### Epidemie
#### L'évènement
* `condition` :
```python
#si le royaume est trop riche, il dispose des conditions sanitaire suffisante pour en être exempté
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

#### Les solutions
# On choisit de mettre en quarantaine tous les malades
* `on_fire` :
```python
# On a quand même quelques pertes, mais on en a sauvé pas mal !
kingdom.population *= 1.5
kingdom.save()
```

# On choisit de les laisser mourrir
* `on_fire`:
```python
# C'est assez dramatique !
kingdom.population /= 2
kingdom.save()
```

#On choisit de faire appel à un medecin
* `on_fire` : 
```python
#On crée une nouvelle PendingMission
PendingMission(
	mission=Mission.objects.get(slug="recherche_medecin"),
	kingdom=kingdom,
).save()
```
