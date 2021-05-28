setup: venv
	venv/bin/pip install --upgrade pip==21.1.2
	venv/bin/pip install -e .

venv:
	python3.9 -m venv venv


clean:
	rm -f keystore.jks keystore.properties
