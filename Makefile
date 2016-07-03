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

# Variables

# path to installation record that gets written when performing:
# - make build2
# - make build3

INSTALLED_FILES_RECORD := ./installed_files.txt

# names of the executables that are used as a part of this project

PYTHON2_CMD := python
PYTHON3_CMD := python3
TOX_CMD := tox
COVERAGE_CMD := coverage
DANGER_CMD := danger
GEM_CMD := gem
FIND_CMD := find
RM_CMD := rm
WHICH_CMD := which
XARGS_CMD := xargs
PRINTF_CMD := printf
TOUCH_CMD := touch
CP_CMD := cp
CAT_CMD := cat
PIP_CMD := pip
CCTREPORTER_CMD := codeclimate-test-reporter

PYPARSING := pyparsing
TOX_PYENV := tox-pyenv

# invoke the specific executable command

PYTHON2 := $(shell command -v $(PYTHON2_CMD) 2> /dev/null)
PYTHON3 := $(shell command -v $(PYTHON3_CMD) 2> /dev/null)
TOX := $(shell command -v $(TOX_CMD) 2> /dev/null)
COVERAGE := $(shell command -v $(COVERAGE_CMD) 2> /dev/null)
DANGER := $(shell command -v $(DANGER_CMD) 2> /dev/null)
GEM := $(shell command -v $(GEM_CMD) 2> /dev/null)
FIND := $(shell command -v $(FIND_CMD) 2> /dev/null)
RM := $(shell command -v $(RM_CMD) 2> /dev/null)
WHICH := $(shell command -v $(WHICH_CMD) 2> /dev/null)
XARGS := $(shell command -v $(XARGS_CMD) 2> /dev/null)
PRINTF := $(shell command -v $(PRINTF_CMD) 2> /dev/null)
TOUCH := $(shell command -v $(TOUCH_CMD) 2> /dev/null)
CP := $(shell command -v $(CP_CMD) 2> /dev/null)
CAT := $(shell command -v $(CAT_CMD) 2> /dev/null)
PIP := $(shell command -v $(PIP_CMD) 2> /dev/null)
CCTREPORTER := $(shell command -v $(CCTREPORTER_CMD) 2> /dev/null)

# Targets

# --- 

checkfor = @$(PRINTF) "Checking for $1..."; \
if [ -z `$(WHICH) $1` ]; then \
$(PRINTF) " no\n"; \
exit 1;\
else \
$(PRINTF) " yes\n"; \
fi

check:
	$(call checkfor,$(WHICH_CMD))
	$(call checkfor,$(CAT_CMD))
	$(call checkfor,$(CP_CMD))
	$(call checkfor,$(TOUCH_CMD))
	$(call checkfor,$(FIND_CMD))
	$(call checkfor,$(XARGS_CMD))
	$(call checkfor,$(RM_CMD))
	$(call checkfor,$(PYTHON2_CMD))
	$(call checkfor,$(PYTHON3_CMD))
	$(call checkfor,$(PIP_CMD))
	$(call checkfor,$(TOX_CMD))
	$(call checkfor,$(COVERAGE_CMD))
	$(call checkfor,$(GEM_CMD))
	$(call checkfor,$(DANGER_CMD))
	@echo "============================"

# --- 

pipinstall = @pip install $1 --user
geminstall = @gem install $1 --user

install-deps: 
	$(call checkfor,$(PYTHON2_CMD))
	$(call checkfor,$(PIP_CMD))
	$(call pipinstall,$(COVERAGE_CMD))
	$(call pipinstall,$(TOX_CMD))
	$(call pipinstall,$(PYPARSING))
	$(call pipinstall,$(TOX_PYENV))
	$(call pipinstall,$(CCTREPORTER_CMD))
	$(call checkfor,$(GEM_CMD))
	$(call geminstall,$(DANGER_CMD))

# --- 

# this is for installing any tools that we don't already have
install-tools: check
	@$(PRINTF) "Installing git hooks..."
	@$(PYTHON) ./tools/hooks-config.py
	@$(PRINTF) " done!\n"

# --- 

removeall=$(RM) -rdf
cleanlocation = @$(FIND) $1 $2 -print0 | $(XARGS) -0 $(removeall)
clean: check
	@$(PRINTF) "Removing existing installation...\n"
	@$(TOUCH) $(INSTALLED_FILES_RECORD)
	@$(CAT) $(INSTALLED_FILES_RECORD) | $(XARGS) $(removeall)
	@$(removeall) ./pyconfig.egg-info
	@$(removeall) ./build
	@$(removeall) ./dist
	@$(removeall) ./.tox
	@$(removeall) .coverage
	@$(removeall) ./htmlcov
	$(call cleanlocation, ., -name "*.pyc")
	$(call cleanlocation, ., -name "__pycache__" -type d)
	$(call cleanlocation, ./tests, -name "*.xcconfig" -and -not -name "*_output.xcconfig")
	@echo "============================"
	
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
	$(CCTREPORTER) --token $(value CIRCLECI_CODECLIMATE_TOKEN)
endif
endif

# --- 

report: check
	$(COVERAGE) report
	$(COVERAGE) html
ifdef CIRCLE_ARTIFACTS
	$(CP) -r ./htmlcov $(CIRCLE_ARTIFACTS)
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