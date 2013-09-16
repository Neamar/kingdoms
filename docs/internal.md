Documentation pour le scripting par Internal
=======================
![Internal models](https://github.com/Neamar/kingdoms/blob/master/event/models.png?raw=true)

Vocabulaire des Internals
------------------------
* `recurring` : sera appellé régulièrement (toutes les minutes, toutes les heures ou tous les jours).

* `trigger` : sera appelé (une seule fois par royaume !) lorsque certaines conditions sont remplies.

* `constant` : définit une valeur utilisable dans n'importe quel environnement de script. Les constantes sont à utiliser plutôt que de marquer un chiffre "brut" dans le code.

* `function` : définit une fonction utilisable dans n'importe quel environnement de script.

Où scripter ?
-------------
### Recurring
* `kingdoms` : ce code renvoie une liste d'objets `Kingdoms` sur lesquels le recurring devra s'appliquer.

* `on_fire` : ce code sera executé à intervalle régulier sur chacun des royaumes renvoyés par `kingdoms`.

### Trigger
* `condition` : ce code permet d'ajouter une condition, en plus des seuils sur `prestige`, `population` et `money`.

* `on_fire`: ce code sera executé au déclenchement du trigger.

### Function
* `on_fire` : ce code sera executé a l'appel de la fonction.


Exemples
-------------
### Recurring
#### Augmentation continue de la population
Réalisons un recurring qui augmente la population lorsqu'il y a plus de 10 personnes dans la cour.
* `condition` : 

```python
# S'il y a au total moins de 10 personnes dans ma cour
if folks.count() < 10:
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
kingdom.start_pending_event("banquet")
```

### Constantes
Pour accèder à une constante depuis un code :

```python
if folk.age() <= C.MAJORITY:
  status = "Tu es trop jeune pour participer !"
```

Bien que cela ne soit pas obligatoire, par convention, il est préférable de nommer la constante en majuscule.

### Functions
#### Fonction calculant la somme des statistiques d'un folk
* `on_fire` :
```python
# la valeur contenue dans param est la valeur que l'on souhaite retourner
param = folk.fight + folk.plot + folk.scholarship + folk.diplomacy
```

Appel de la fonction :
```python
somme = call_function("somme_stats_folk", folk=le_folk_a_calculer)
# OU, version plus courte :
somme = f("somme_stats_folk", folk=le_folk_a_calculer)
```
