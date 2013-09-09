Documentation pour le scripting par Internal
=======================
![Internal models](https://github.com/Neamar/kingdoms/blob/master/event/models.png?raw=true)

Vocabulaire des Internals
------------------------
* `recurring` : sera appellé régulièrement (toutes les minutes, toutes les heures ou tous les jours).

* `trigger` : sera appelé (une seule fois par royaume !) lorsque certaines conditions sont remplies.

* `Constant` : définit une valeur utilisable dans n'importe quel environnement de script. Les constantes sont à utiliser plutôt que de marquer un chiffre "brut" dans le code.


Où scripter ?
-------------
### Recurring
* `condition` : ce code définit si le `kingdom` doit se voir appliquer le `in_fire`. Pour annuler ce recurring, il faut renvoyer `param= None`.

* `on_fire` : ce code sera executé à intervalle régulier, si la condition s'applique.

### Trigger
* `condition` : ce code permet d'ajouter une condition, en plus des seuils sur `prestige`, `population` et `money`.

* `on_fire`: ce code sera executé au déclenchement du trigger.

Que scripter ?
---------------


Exemples
-------------
### Recurring
#### Augmentation continue de la population

* `condition` : 

```python
# S'il y a au total moins de 10 personnes dans ma cour
if Folk.objects.filter(kingdom=kingdom).count() < 10:
	# On renvoie un status car on ne veut pas que la population augmente s'il n'y a pas assez de folk
	status = "not_enough_people"
```

 * `on_fire` :

```python
# On augmente la population
kingdom.population *= 1.1
kingdom.save()
 ```

### Trigger
#### Lancement de l'évènement Banquet lorsque la population dépasse 1 000
* `condition` : pas nécessaire, la limite est dans `population_threshold`.

* `on_fire` : 

```python
# On affecte l'event Banquet au Kingdom
PendingEvent(
  event=Event.objects.get(slug="banquet"),
  kingdom=param,
).save()
```

### Constantes
Pour accèder à une constante depuis un code :

```python
if folk.age() <= C("MAJORITY"):
  status = "Tu es trop jeune pour participer !"
```

Bien que cela ne soit pas obligatoire, par convention, il est préférable de nommer la constante en majuscule.
