Documentation pour le scripting par Internal
=======================
![Internal models](https://github.com/Neamar/kingdoms/blob/master/event/models.png?raw=true)

Vocabulaire des Internals
------------------------
* `recurring` : sera appellé régulièrement (toutes les minutes, toutes les heures ou tous les jours).

* `trigger` : sera appelé (une seule fois !) lorsque certaines conditions deviennent remplies.
<!--
* `Constante` : définie une valeur, utilisée à chaque fois que l'on en a besoin. La seule modification de cette constante met à jours tous les scripts qui l'utilisent.
-->

Où scripter ?
-------------
### Recurring
* `condition` : ce code défini si le kingdom est sujet ou non à ce recurring. Pour annuler ce recurring, il faut renvoyer `param= None`.

*`on_fire` : ce code sera executé lorsque le recurring passera

### Trigger
* `condition` : ce code permet d'ajouter une condition en plus des seuils

* `on_fire`: ce code se exectué lorsque le trigger se déclanchera

Que scripter ?
---------------


Exemples
-------------
### Recurring
#### Augmentation continue de la population

* `condition` : 
```python
# S'il y a au total moins de 10 personnes dans ma cours
if Folk.objects.filter(kingdom=kingdom).count() < 10 :
  param = None
# *on renvoie param=None car on ne veut pas que la population augmente s'il n'y a pas assez de folk
 ```

 * `on_fire` :
 ```python
 #on augmente la population
kingdom.population *=1.1
kingdom.save()
 ```

### Trigger
#### Lancement de l'event Banquet lorsque la pop dépasse 1000
* `condition` : on n'a pas besoin de condition ici.

*`on_fire` : 
# On affect l'event Banquet à ce kingdom
PendingEvent (
  event=Event.objects.get(name="Banquet"),
  kingdom=param,
  text="youppppi"
).save()  # Et on sauvegarde

