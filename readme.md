Kingdoms
========
`Kingdoms` is a browser game implemented in 8 days by a small core-team of 7 persons.
The core code (this repo) is abstracted to allow the creation of many games on the same engine.

Everything runs around the notion of Kingdom, your realm as a player. You need to increase your prestige by doing missions, nominating people to important positions and handling events happening in and out of your reach while interacting and fighting the other player.

As you cann see, this mechanic is pretty abstract; Every deployment of this game is a story of it's own, whit great gameplay and roleplay immersion.

Documentation
-------------
For the docs, [see this link](docs/readme.md).

Models
------
Just for the fun of displaying a huge graph.

![Models](https://github.com/Neamar/kingdoms/blob/master/models.png?raw=true)

Setup 
-----
> This setup is mainly intended for the engine-coder.
> If you've never played a Kingdoms game before, you should really try it. Although the code is heavily documented and pretty simple to understand, core concepts of the games lies in its scripting engine; making this engine-code quite abstract to starts with.

* `git clone git@github.com:Neamar/kingdoms.git` : retrieve the repo
* `cd kingdoms`
* `virtualenv --no-site-packages .v_env` : create a virtual-env for python code
* `source .v_env/bin/activate` : activate the v_env.
* `pip install -r requirements.txt` : install all requirements
* `./manage.py syncdb --noinput` : create DB
* `./manage.py migrate` : migrate DB
* `./manage.py loaddata config/fixtures/sample.json` : load some sample datas
* `./manage.py createsuperuser` to create the root user. You can also skip this test and connect yourself as `neamar`, password `arf`.

Running
-------
* `./manage.py runserver`
* Access `http://127.0.0.1:8000` with your browser. The admin is on `http://127.0.0.1:8000/admin/`.

Maintenance
-----------
### Testing
`./manage.py test kingdom mission title internal event bargain`

### Generating models
Enable `django_extensions` in `config/settings.py`, then `./graph.sh`.

Code Status
-----------

[![Travis Status](https://api.travis-ci.org/Neamar/kingdoms.png)](https://travis-ci.org/Neamar/kingdoms)

For any questions, ask on contact@neamar.fr
