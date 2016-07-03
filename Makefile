# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pyconfig
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
# 
# 3. Neither the name of Samantha Marshall nor the names of its contributors may 
# be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
# OF THE POSSIBILITY OF SUCH DAMAGE.

INSTALLED_FILES_RECORD := ./installed_files.txt

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

# --- 

install-tools:
	@echo "Installing git hooks..."
	@python ./tools/hooks-config.py
	@echo "Installing danger via ruby-gems..."
	@$(GEM) install danger --user

# --- 

check: 
	@type $(PYTHON2_CMD) >/dev/null 2>&1 || echo "Please install Python 2"
	@type $(PYTHON3_CMD) >/dev/null 2>&1 || echo "Please install Python 3"
	@type $(TOX_CMD) >/dev/null 2>&1 || echo "Please install tox"
	@type $(COVERAGE_CMD) >/dev/null 2>&1 || echo "Please install coverage"
	@type $(DANGER_CMD) >/dev/null 2>&1 || echo "Please install danger"
	@type $(GEM_CMD) >/dev/null 2>&1 || echo "Please install ruby-gems"

# --- 

clean: check
	@echo "Removing existing installation..."
	@touch $(INSTALLED_FILES_RECORD)
	@cat $(INSTALLED_FILES_RECORD) | xargs rm -rf
	@rm -rdf ./pyconfig.egg-info
	@rm -rdf ./build
	@rm -rdf ./dist
	@rm -rdf ./.tox
	@rm -rdf .coverage
	@rm -rdf ./htmlcov
	@find . -name "*.pyc" -print0 | xargs -0 rm -rdf
	@find . -name "__pycache__" -type d -print0 | xargs -0 rm -rdf
	@find ./tests -name "*.xcconfig" -and -not -name "*_output.xcconfig" -print0 | xargs -0 rm -rdf
	
# --- 
	
build2: clean
	$(PYTHON2) ./setup.py install --user --record $(INSTALLED_FILES_RECORD)
	
# --- 
	
build3: clean
	$(PYTHON3) ./setup.py install --record $(INSTALLED_FILES_RECORD)

# --- 

test: check
	$(TOX)
ifdef CIRCLE_BRANCH
ifeq ($(CIRCLE_BRANCH),develop)
	codeclimate-test-reporter --token $(value CIRCLECI_CODECLIMATE_TOKEN)
endif
endif

# --- 

report: check
	$(COVERAGE) report
	$(COVERAGE) html
ifdef CIRCLE_ARTIFACTS
	cp -r ./htmlcov $(CIRCLE_ARTIFACTS)
endif 

# --- 

danger: check
ifdef CIRCLECI_DANGER_GITHUB_API_TOKEN
	@export DANGER_GITHUB_API_TOKEN=$(value CIRCLECI_DANGER_GITHUB_API_TOKEN)
	$(DANGER)
else
	$(DANGER) local --verbose
endif
	
# --- 

ci: test report danger