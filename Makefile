INSTALLED_FILES_RECORD := ./installed_files.txt
DANGER_GITHUB_API_TOKEN := 5e94e727bcc91e7ff681e2995af2a0c4961404de

PYTHON2_CMD := python
PYTHON3_CMD := python3
TOX_CMD := tox
COVERAGE_CMD := coverage
DANGER_CMD := danger
GEM_CMD := gem

PYTHON2 := $(shell command -v $(PYTHON2_CMD) 2> /dev/null)
PYTHON3 := $(shell command -v $(PYTHON3_CMD) 2> /dev/null)
TOX := $(shell command -v $(TOX_CMD) 2> /dev/null)
COVERAGE := $(shell command -v $(COVERAGE_CMD) 2> /dev/null)
DANGER := $(shell command -v $(DANGER_CMD) 2> /dev/null)
GEM := $(shell command -v $(GEM_CMD) 2> /dev/null)

install-tools:
	@echo "Installing git hooks..."
	@python ./tools/hooks-config.py
	@echo "Installing danger via ruby-gems..."
	@$(GEM) install danger --user

check: 
	@type $(PYTHON2_CMD) >/dev/null 2>&1 || echo "Please install Python 2"
	@type $(PYTHON3_CMD) >/dev/null 2>&1 || echo "Please install Python 3"
	@type $(TOX_CMD) >/dev/null 2>&1 || echo "Please install tox"
	@type $(COVERAGE_CMD) >/dev/null 2>&1 || echo "Please install coverage"
	@type $(DANGER_CMD) >/dev/null 2>&1 || echo "Please install danger"
	@type $(GEM_CMD) >/dev/null 2>&1 || echo "Please install ruby-gems"

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
	@find . -name "__pycache__" -type d -print0 | xargs -0 rm -rdf
	@find ./tests -name "*.xcconfig" -and -not -name "*_output.xcconfig" -print0 | xargs -0 rm -rdf
	
	
build2: clean
	$(PYTHON2) ./setup.py install --user --record $(INSTALLED_FILES_RECORD)
	
build3: clean
	$(PYTHON3) ./setup.py install --record $(INSTALLED_FILES_RECORD)

test: check
	$(TOX)
ifdef CIRCLE_BRANCH
ifeq ($(CIRCLE_BRANCH),develop)
	codeclimate-test-reporter --token 1b415a3f064b44dcefd71011b2d1208eca337c51017a7059b3c60cf31e21f026
endif
endif

report: check
	$(COVERAGE) report
	$(COVERAGE) html
ifdef CIRCLE_ARTIFACTS
	cp -r ./htmlcov $(CIRCLE_ARTIFACTS)
endif 

danger: check
	@echo "DANGER_GITHUB_API_TOKEN=$(value DANGER_GITHUB_API_TOKEN)"
ifdef CIRCLE_BUILD_NUM
	$(DANGER)
else
	$(DANGER) local --verbose
endif
	
	
ci: test report danger