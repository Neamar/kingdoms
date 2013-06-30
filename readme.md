Kingdoms
========

![Models](https://github.com/Neamar/kingdoms/blob/master/models.png?raw=true)

Setup
-----
* `git clone git@github.com:Neamar/kingdoms.git` : retrieve the repo
* `cd kingdoms`
* `virtualenv --no-site-packages .v_env` : create a virtual-env for python code
* `source .v_env/bin/activate` : activate the v_env.
* `pip install -r requirements.txt` : install all requirements
* `./manage.py syncdb --noinput && ./manage.py loaddata config/fixtures/sample.json` : creates the DB and load some sample datas

Running
-------
* `./manage.py runserver`

Maintenance
-----------
### Testing
`./manage.py test kingdom mission title internal event`

### Generating models
`./manage.py graph_models kingdom internal title mission event -o models.png`
