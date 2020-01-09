init:
	python3 -m pip install --user pipenv
	pipenv --python 3.7
	pipenv install --dev --skip-lock
	echo "Check the printed version for numpy is 1.16.4" && pipenv run pip list | grep "numpy"
	echo "Check the printed version for torch is 1.2.0" && pipenv run pip list | grep "torch"
	echo "Check the printed version for tensorboard is 1.14.0" && pipenv run pip list | grep "tensorboard"

LIB_LINT = osminfo
RUN_LINT = run_*.py
PYTHON_LINT = $(LIB_LINT) $(RUN_LINT)

lint: linter_version ending flake8 pylint mypy

linter_version:
	pipenv run pip list | grep "flake8"
	pipenv run pip list | grep "pylint"
	pipenv run pip list | grep "mypy"

ending:
	! grep -rHnP --include="*.py" --include="*.json" --include="*.md" --include="*.csv" "\x0D" ${PYTHON_LINT}

flake8:
	pipenv run flake8 ${PYTHON_LINT}

pylint:
	pipenv run pylint ${PYTHON_LINT}

mypy:
	pipenv run mypy ${PYTHON_LINT}

clean:
	rm -rf .mypy_cache/

clean_log:
	rm ./logs/*.log

run_test:
	pipenv run python3 run_test.py

run_crawl_full_TW_grids:
	pipenv run python3 run_crawl_full_TW_grids.py

run_crawl_roadnetwork_TW_grids:
	pipenv run python3 run_crawl_roadnetwork_TW_grids
