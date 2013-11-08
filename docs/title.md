Documentation pour le scripting par Title
=======================
![Title models](https://github.com/Neamar/kingdoms/blob/master/title/models.png?raw=true)

Vocabulaire des Title
------------------------

Où scripter ?
-------------
* `Condition` : ce code définit les conditions de validité pour qu'une personne puisse avoir ce titre. Pour empêcher l'affectation, renvoyer `status="la raison de l'erreur"`.

* `on affect` : ce code sera executé lorsqu'on affecte le titre à une personne.

* `on defect` : ce code sera executé lorsqu'on enlève le titre à une personne.

* `on_unlock` : ce code sera executé lorsqu'on débloque le titre à un kingdom.


Exemples
-------------
### Le chef de guerre

* `Condition` :
```python
# Il faut que le chef soit un homme
if folk.sex == Folk.FEMALE :
  status = "le chef doit être un homme"
```

* `on affect` :
```python
# La loyauté du promu augmente
folk.loyalty += 20
folk.save()

# Le prestige augmente
kingdom.prestige += 5
kingdom.save()
```

* `on deffect` : 
```python
# La loyauté diminue
folk.loyalty -= 30
folk.save()

# Le prestige diminue
kingdom.prestige -= 5
kingdom.save()
```

* `on_unlock` :
```python
kingdom.message("Vous pouvez désormais nommer le chef de guerre.")
kingdom.unlock_mission("piller_des_villages_et_violer_les_femmes")
```
