venv:
	python3 -m venv .venv

install: venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@test -f config.yml || cp config_example.yml config.yml

run:
	.venv/bin/python -m app.main