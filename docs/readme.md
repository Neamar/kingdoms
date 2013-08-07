 Documentation des royaumes
===========================
Le code de `Kingdoms` permet de générer une multitude de jeux dans des univers variés.

> [Comment installer Kingdoms ?](../readme.md) La page d'accueil du projet sur Github contient un guide pour les techos qui veulent déployer Kingdoms sur leur serveur. Si vous rejoignez un projet existant, cela ne vous concerne pas.

## Bienvenue !

Vous venez de rejoindre un projet `Kingdoms`, félicitations.

Rendez-vous maintenant sur la page `/admin`, puis connectez-vous avec l'identifiant que l'on a dû vous communiquer précédemment.

L'interface qui s'affiche maintenant dépend des droits qui vous ont été conférés. Pour ce guide, nous allons partir du principe que vous êtes "super-utilisateur" et que vous bénéficiez donc de tous les droits.

Vous devriez donc voir de nombreux liens. Tous ne vous intéressent pas, mais vous apprendrez à les découvrir dans les pages qui suivent.

Baladez-vous un peu (en évitant de tout supprimer !) pour vous familiariser avec l'interface : consultation, modification, suppression...
Prenez aussi note des "actions" : cliquez par exemple, dans le tableau "Internal", sur "Recurring", sélectionnez un objet et cliquez sur la liste déroulante d'actions : vous verrez apparaître une option de déclenchement.

## Scripter, c'est quoi ?
Scripter consiste à coder des fonctionnalités et des comportements dans l'univers du jeu.
Il s'agit d'une forme particulière (simplifiée sur certains points) de programmation.
Le scripting nécessite un minimum de connaissance en code (au minimum conditions, tableaux et boucles).
Il se réalise en [Python](http://www.python.org/).

## Que scripter, où et avec quelles fonctions ?
Liens vers la documentation pour le scripting :
* [Kingdom](kingdom.md) : `kingdom`, `folk`...
* [Internal](internal.md) : `trigger`, `recurring`...
* [Event](event.md) : `event`, `event_action`, `pending_event`
* [Mission](mission.md) : `mission`, `pending_mission`

### Et ensuite ?
* [Bargain](bargain.md) : non nécessaire sauf pour le scripting de très haut niveau
* [Reporting](reporting.md) : pour data-miner les joueurs, trouver des bugs ou optimiser.

## Où trouver plus de ressources pour le scripting ?
Le moteur de script tourne avec Django. Il est donc conseillé d'aller faire un tour [sur cette page](https://docs.djangoproject.com/en/dev/topics/db/queries/) une fois les fondamentaux acquis, pour mieux comprendre le fonctionnement des requêtes et pouvoir optimiser les accès à la base de données afin d'avoir un jeu rapide et réactif.

Il peut aussi être utile de découvrir Python plus en profondeur afin de mieux utiliser les mécanismes disponibles (compréhension de listes, fonctions builtin...)

Enfin, pour aller plus loin, rien ne vaut... [le code en lui-même](https://github.com/Neamar/kingdoms) !

Pour plus de détails, n'hésitez pas à contacter le responsable de Kingdoms : [neamar@neamar.fr](mailto:neamar@neamar.fr)

Bon code.
