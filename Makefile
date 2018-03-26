default: venv

.PHONY: venv
venv:
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade -r requirements.txt


.PHONY: run
run:
	venv/bin/uwsgi --ini uwsgi.ini


.PHONY: clean
clean:
	rm -rf venv
