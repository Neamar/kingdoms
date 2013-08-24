Documentation pour le scripting par Mission
=======================
![Mission models](https://github.com/Neamar/kingdoms/blob/master/mission/models.png?raw=true)

Vocabulaire des missions
------------------------
Une `mission` représente une tâche attribuée à un groupe de personne.
Les missions peuvent contenir une ou plusieurs `grilles`, pouvant chacune contenir une ou plusieurs personnes.
Une mission peut-être démarrée par le joueur, et avoir des effets.
Une mission peut prendre en paramètre une cible (un `Kingdom`) ou une valeur.
Certaines missions sont annulables, d'autres non.

Le joueur peut créer autant de `PendingMission` qu'il le souhaite. Une `PendingMission` correspond à une instance d'une mission donnée : par exemple, on peut imaginer une mission mariage constituée de deux grilles (une pour l'homme à marier, une pour la femme en face). Le joueur peut lancer deux `PendingMission` de la mission mariage, ce qui lui permet de célebrer plusieurs mariages en même temps s'il le souhaite.

Pour créer une `PendingMission` de lui-même (sans la subir automatiquement par un évènement donc), le joueur doit disposer d'un objet `AvailableMission` associé, qui agit comme un "générateur" de `PendingMission`

Pour résumer : la `Mission` correspond à l'object contenant le script.
L'`AvailableMission` permet de créer des `PendingMission`.
Les `PendingMission` sont les missions visibles à l'instant t par l'utilisateur.

Enfin, les `équipes` sont des missions un peu spéciales, qui ne peuvent pas être lancées. Il s'agit plutôt de "groupes de travail" autour d'un sujet donné.

Les affectations d'une personnes dans une mission sont stockées dans des objets `PendingMissionAffectation`. Une même personne ne peut être que dans une seule mission à la fois !


Où scripter ?
-------------
### Depuis une mission
* `on_init` : ce code sera exécuté lorsqu'une mission sera créée pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours. Pour annuler cette mission, il faut renvoyer `status= "la raison de l'erreur"`.
* `on_cancel` : ce code sera exécuté lorsque la mission est annulée, soit par timeout, soit par demande explicite de l'utilisateur.
* `on_start` : ce code sera exécuté lorsque la mission démarre pour un joueur donné (au clic sur le bouton "débuter la mission"). Le paramètre `param` contiendra la `PendingMission` en cours. Pour annuler le démarrage d'une mission, il suffit de spécifier le paramètre `status="la raison de l'erreur"`.
* `on_resolution` : ce code sera exécuté lorsque la mission esr résolue pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours.
* `target_list` : définit la liste des kingdom ciblables

### Sur une grille
* `condition`: ce code définit les conditions de validité pour qu'une personne puisse appartenir à la liste. Pour empêcher l'affectation, renvoyer `status="la raison de l'erreur"`.


Que scripter ?
---------------
Scriptez les objets missions !

Les `PendingMission` sont des objets de contexte, au même titre que les `PendingEvent` ou les `Kingdoms`. Il est donc possible de stocker des valeurs *sur* un object `PendingMission`, pour les récupérer plus tard (par exemple au moment du `on_start` pour utilisation ultérieure dans `on_resolution`).

Exemples
-------------
### Le défi du Chevalier Noir

`on_resolution` :
```python
# Récupération des personnes affectées à la mission
if len(folks) == 0:
	# Si personne n'est affecté à la mission (la taille de la liste = 0),l'argent du kingdom est divisé par 2
	kingdom.money = kingdom.money / 2
else:
	# Sinon, si la personne affectée a plus de 5 de combat, le kingdom gagne 500, si la personne est trop faible, le kingdom perd 50.
	if folks[0].folk.fight > 5: #folks[0] : on prend la première personne de la liste des affectés
		kingdom.money += 500
	else:
		kingdom.money -= 50

# Ne surtout pas oublier d'appeler save(), sinon aucun enregistrement n'est effectué. 
kingdom.save()
```

Pour la grille, supposons qu'il faut un unique homme pour affronter le Chevalier Noir.

`condition` :
```python
if param.sex != Folk.MALE:
	# Si la personne est une femme, on définit status avec un message d'erreur.
	status="Seul un homme peut affronter le chevalier noir !"
```

### Le mariage

`on_resolution` :
```python
if len(folks) == 2:
	husband = grids['mari'][0]
	wife = grids['femme'][0]

	husband.spouse = wife
	husband.save()

	wife.spouse = husband
	wife.save()
```

Il faut deux grilles : le mari et la femme.

`condition` :
```python
if param.sex != Folk.MALE:
  status="Seul un homme peut être le marié."
```

`condition` :
```python
if param.sex != Folk.FEMALE:
  status="Seule une femme peut être la mariée."
```

### Le kamikaze
Utilise le système de `target`.

`target_list` :
```python
# Les kamikazes ne ciblent que les royaumes riches et développés
param = Kingdom.objects.filter(population>100, money>1000)
```

`on_resolution` :
```python
# Le kamikaze meurt (probablement dans d'atroces souffrances)
folks[0].folk.die()

# Le kingdom visé perd en population.
target.population -= 20
target.save()
```
