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

def TraverseGraphNodes(graph_nodes=[]):
    graph_list = list()
    visited = set()
    root_nodes_array = list(filter(lambda node: len(node.parents) == 0, graph_nodes))
    for root_node in root_nodes_array:
        graph_list.append(root_node)
        visited.add(root_node)
    child_nodes = WalkGraphNodes(visited, root_nodes_array)
    graph_list.extend(child_nodes)
    visited.update(set(child_nodes))
    return graph_list

def WalkGraphNodes(visited=set(), nodes_with_children=[]):
    child_nodes = list()
    for node in nodes_with_children:
        valid_nodes_array = list(filter(lambda filtered_node: filtered_node not in visited, node.children))
        for valid_node in valid_nodes_array:
            visited.add(valid_node)
            located_child_nodes = WalkGraphNodes(visited, [valid_node])
            child_nodes.extend(located_child_nodes)
    
    return child_nodes
    
        