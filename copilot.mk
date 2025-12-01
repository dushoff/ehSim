
# Makefile
PY=python3

.PHONY: run test clean

run:
	$(PY) src/cli.py --beta 3 --pop 100000 --report 10 20 30 --out data/out.json

run-inf:
	$(PY) src/cli.py --beta 3 --pop 100000 --report inf --out data/out_inf.json

test:
	$(PY) -m pytest -q

clean:
	rm -f data/*.json

