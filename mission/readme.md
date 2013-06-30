Documentation pour le scripting par Mission
=======================
![Mission models](https://github.com/Neamar/kingdoms/blob/master/mission/models.png?raw=true)

Vocabulaire des missions
------------------------

Où scripter ?
-------------
### Depuis une mission
* `on_init` : ce code sera exécuté lorsqu'une mission sera créée pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours. Pour annuler cette mission, il faut renvoyer `status= "la raison de l'erreur"`.
* `on_start` : ce code sera exécuté lorsque la mission démarre pour un joueur donné (au clic sur le bouton "débuter la mission"). Le paramètre `param` contiendra la `PendingMission` en cours.
* `on_resolution` : ce code sera exécuté lorsque la mission esr résolue pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours.
* `target_list` : définit la liste des kingdom cibles

### Sur une grille
* `condition`: ce code définit les conditions de validité pour qu'une personne puisse appartenir à la liste. Pour empêcher l'affectation, renvoyer `status="la raison de l'erreur"`.


Que scripter ?
---------------


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
	husband = folks[0].folk
	wife = folks[1].folk

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
  status="Seul une femme peut être la mariée."
```

### Le kamikaze
Utilise le système de `target`.

`on_resolution` :
```python
# Le kamikaze meurt (probablement dans d'atroces souffrances)
folks[0].folk.die()

# Le kingdom visé perd en population.
target.population -= 20
target.save()
```
