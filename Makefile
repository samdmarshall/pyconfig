INSTALLED_FILES_RECORD := ./installed_files.txt

PYTHON2_CMD := python
PYTHON3_CMD := python3
TOX_CMD := tox

PYTHON2 := $(shell command -v $(PYTHON2_CMD) 2> /dev/null)
PYTHON3 := $(shell command -v $(PYTHON3_CMD) 2> /dev/null)
TOX := $(shell command -v $(TOX_CMD) 2> /dev/null)

check:
	@type $(PYTHON2_CMD) >/dev/null 2>&1 || echo "Please install Python 2"
	@type $(PYTHON3_CMD) >/dev/null 2>&1 || echo "Please install Python 3"
	@type $(TOX_CMD) >/dev/null 2>&1 || echo "Please install tox"

clean: check
	@echo "Removing existing installation..."
	@touch $(INSTALLED_FILES_RECORD)
	@cat $(INSTALLED_FILES_RECORD) | xargs rm -rf
	@rm -rdf ./pyconfig.egg-info
	@rm -rdf ./build
	@rm -rdf ./dist
	@rm -rdf ./.tox
	@rm -rdf ./tests/__pycache__
	@rm -rdf .coverage
	@rm -rdf ./htmlcov
	@find . -name "*.pyc" -print0 | xargs -0 rm -rdf
	
	
build2: clean
	$(PYTHON2) ./setup.py install --user --record $(INSTALLED_FILES_RECORD)
	
build3: clean
	$(PYTHON3) ./setup.py install --record $(INSTALLED_FILES_RECORD)

test:
	$(TOX)
ifdef CIRCLE_BRANCH
ifeq ($(CIRCLE_BRANCH),develop)
	codeclimate-test-reporter --token 1b415a3f064b44dcefd71011b2d1208eca337c51017a7059b3c60cf31e21f026
endif
endif

