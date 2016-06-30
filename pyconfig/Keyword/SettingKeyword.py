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

from . import Constants
from . import BaseKeyword

class SettingKeyword(BaseKeyword.BaseKeyword):
	
	def __init__(self):
		self.uses_if = False
		self.uses_for = False
		
		self.inherits = False
		
		self.substitutes = False
		self.substitution_variable_name = 'CONFIGURATION'
		
		self.configuration_values = {}
		self.default_value = ''
		
		self.build_setting_name = ''
	
	def consume(self, parsed_item=[]):
		if parsed_item[0] == Constants._setting:
			self.build_setting_name = parsed_item[1]
			modifiers = parsed_item[2]
			configurations = parsed_item[3]
			
			if len(modifiers):
				if modifiers[0] == Constants._use:
					self.substitutes = True
					self.substitution_variable_name = modifiers[1]
				if modifiers[0] == Constants._inherits \
					or (len(modifiers) == 3 and modifiers[2] == Constants._inherits):
						self.inherits = True
			
			keywords_used = list()
			for setting_configuration in configurations:
				keywords_used.append(setting_configuration[0])
			
			keyword_used = set(keywords_used)
			if len(keyword_used) > 1:
				raise ValueError('More than one type of assignment was used for the build setting "%s"' % self.build_setting_name)
			
			used_keyword_in_assignemnt = next(iter(keyword_used))
			self.uses_if = (used_keyword_in_assignemnt == Constants._if)
			self.uses_for = (used_keyword_in_assignemnt == Constants._for)
				
			for setting_configuration in configurations:
				configuration_type = setting_configuration[0]
				
				if configuration_type == Constants._for:
					configuration_name = setting_configuration[1]
					value = ''
					if len(setting_configuration) == 3:
						value = setting_configuration[2]
					if configuration_name != Constants._specialCase:
						self.configuration_values[configuration_name] = ' '.join(value)
					else:
						self.default_value = ' '.join(value)
				
				if configuration_type == Constants._if:
					conditions = setting_configuration[1]
					assignment_value = setting_configuration[2]
					conditional_key_value_list = list()
					for condition in conditions:
						conditional_key_value_list.append('='.join(condition))
					conditional_key_value_string = ','.join(conditional_key_value_list)
					self.configuration_values[conditional_key_value_string] = assignment_value

	def serializeInheritedValues(self):
		serialize_string = ''
		if self.inherits:
			serialize_string += '$(inherited) '
		return serialize_string

	def serialize(self):
		serialize_string = ''
		if self.uses_for:
			for key, value in self.configuration_values.items():
				serialize_string += self.build_setting_name
				if len(self.configuration_values.keys()) > 1:
					serialize_string += '_'+key
				serialize_string += ' = '
				serialize_string += self.serializeInheritedValues()
				serialize_string += value+'\n'
			serialize_string += self.build_setting_name+' = '
			serialize_string += self.serializeInheritedValues()
			keys = self.configuration_values.keys()
			if (len(keys) > 1) or (len(keys) and keys[0] != Constants._specialCase):
				serialize_string += '$('+self.build_setting_name+'_$('+self.substitution_variable_name+'))'
				if len(self.default_value):
					serialize_string += ' '
			serialize_string += self.default_value
			serialize_string +='\n'
		
		if self.uses_if:
			for key, value in self.configuration_values.items():
				serialize_string += self.build_setting_name+'['+key+']'+' = '
				serialize_string += self.serializeInheritedValues()
				serialize_string += value+'\n'
		return serialize_string