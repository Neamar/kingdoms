Documentation pour le scripting par Mission
=======================
![Mission models](https://github.com/Neamar/kingdoms/blob/master/mission/models.png?raw=true)

Vocabulaire des missions
------------------------

Où scripter ?
-------------
### Depuis une mission
* `on_init` : ce code sera exécuté lorsqu'une mission sera créée pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours. Pour annuler cette mission, il faut renvoyer `status= "la raison de l'erreur"`.
* `on_start` : ce code sera éxécuté lorsque la mission démarre pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours.
* `on_resolution` : ce code sera éxécuté lorsque la mission esr résolue pour un joueur donné. Le paramètre `param` contiendra la `PendingMission` en cours.
* `target_list` : définie la liste des kingdom cibles

### Sur une grille
* `lenght` : le nombre de personne maximum pouvant prendre part à la mission
* `condition`: ce code définie les conditions de validité pour qu'une personne puisse appartenir à la liste


Que scripter ?
---------------


Exemples
-------------
### Exemple complet de la mission du défi du Chevalier Noir
####Création de la mission

`on_init` : le chevalier Noir tue 2 paysans pour vous provoquer à son arrivée :
```python
# On récupère notre kingdom
kingdom = param.kingdom
# On diminue notre population de 2
kingdom.population -= 2
# Ne surtout pas oublier d'appeler save(), sinon aucun enregistrement n'est effectué. 
kingdom.save() 
```

`on_start` vide: pas besoin de code ici

`on_resolution` :
```python
# Récurépation des personnes affecté à la mission
affected = param.folk_set.all()
# Récupération des paramètres du kingdom
kingdom = param.kingdom
# Si personne n'est affecté à la mission (la taille de la liste = 0),l'argent du kingdom est divisé par 2
if len(affected) == 0:
  kingdom.money = kingdom.money / 2
else:
# Sinon, si la personne affecté à plus de 5 de combat, le kingdom gagne 500, si la personne est trop faible, le kingdom perd 50
  if affected[0].folk.fight > 5: #affected[0] : on prend la première personne de la liste des effectés
    kingdom.money += 500
  else:
    kingdom.money -= 50

# Ne surtout pas oublier d'appeler save(), sinon aucun enregistrement n'est effectué. 
kingdom.save()
```

####Création de la grille
Supposons qu'il faut un homme pour affronter le Chelavier Noir
`lenght` : mettons 1, le Chevalier Noir exige un duel
`condition`:
```python
if param.sex == "f":
	status="must be a male"
# Si la personne est une femme, on définie un statut (un message d'erreur). Un statut non modifié signifie que la condition est remplie.
```