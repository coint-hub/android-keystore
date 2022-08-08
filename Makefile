setup: venv
	venv/bin/pip install --upgrade pip==22.2.2
	venv/bin/pip install -e .

venv:
	nix-shell -p python310 --run 'python3 -m venv venv'


clean:
	rm -f keystore.jks keystore.properties
