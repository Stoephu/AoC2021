# %%
from typing import AsyncGenerator


class Node:
    def __init__(self, rule, insert):
        self.rule = rule
        self.insert = insert
        self.left_node : Node = None
        self.right_node: Node = None
    
    def left_node_name(self):
        if self.left_node:
            return f'LeftNode: {self.left_node.rule}'
        return (self.rule[0],self.insert)
        
    def right_node_name(self):
        if self.right_node:
            return f'RightNode: {self.right_node.rule}'
        return (self.insert, self.rule[1])

    def __str__(self) -> str:
        return f'Node: {self.rule} -> {self.insert} | {self.left_node_name()}; {self.right_node_name()}'

# %%
inp =  [line.strip() for line in open('../inputs/Day14.txt')]
template = inp[0]
rulesstring = inp[2:]
# %%
rules = {}
for row in rulesstring:
    splitrow = row.split()
    key = tuple(splitrow[0])
    rules[key] = splitrow[-1], Node(key, splitrow[-1])
# %%
for _, values in rules.items():
    insert, node = values
    node.left_node = rules.get(node.left_node_name())[1]
    node.right_node = rules.get(node.right_node_name())[1]

# %%
class Runner:
    def __init__(self, age, maxage, letter_counts, current_node) -> None:
        self.age = age
        self.maxage = maxage
        self.letter_counts = letter_counts
        self.current_node = current_node
        self.next_nodes = []
    
    def run(self):
        if self.current_node and self.age < self.maxage:
            self.letter_counts[self.current_node.insert] = 1 + self.letter_counts.get(self.current_node.insert, 0)
            self.next_nodes.append((self.age + 1, self.current_node.left_node))
            self.current_node = self.current_node.right_node
            self.age += 1
            return True
        else:
            if len(self.next_nodes) > 0:
                self.age, self.current_node = self.next_nodes.pop()
                return True
            else:
                print('Done')
                return False
    
    def __str__(self) -> str:
        return f'RunnerState age:{self.age}; {self.current_node} {self.letter_counts}'
# %%
letter_counts = {}
for i in range(len(template) - 1):
    gene = template[i], template[i+1]
    print(f'New Runner on {gene=}')
    letter_counts[gene[0]] = 1 + letter_counts.get(gene[0], 0)
    letter_counts[gene[1]] = 1 + letter_counts.get(gene[1], 0)
    runner = Runner(0,10,letter_counts,rules[gene][1])
    while True:
        if not runner.run():
            break
# %%
max_letter, max_value = (k:=max(letter_counts, key= letter_counts.get), letter_counts[k])
print(max_letter, max_value)
min_letter, min_value = (k:=min(letter_counts, key= letter_counts.get), letter_counts[k])
print(min_letter, min_value)
print(f'Result {max_value-min_value}')
# %%
"""
# %%
letter_counts = {}
for i in range(len(template) - 1):
    gene = template[i], template[i+1]
    print(f'New Runner on {gene=}')
    letter_counts[gene[0]] = 1 + letter_counts.get(gene[0], 0)
    letter_counts[gene[1]] = 1 + letter_counts.get(gene[1], 0)
    runner = Runner(0,40,letter_counts,rules[gene][1])
    while True:
        if not runner.run():
            break

max_letter, max_value = (k:=max(letter_counts, key= letter_counts.get), letter_counts[k])
print(max_letter, max_value)
min_letter, min_value = (k:=min(letter_counts, key= letter_counts.get), letter_counts[k])
print(min_letter, min_value)
print(f'Result {max_value-min_value}')
"""
# %%

shortcuts = {}
next_nodes=[]
# shortcut
# rule: (startAge, endAge, Node)
rule, value =  list(rules.items())[0]
_, node = value
shortcuts[rule] = 0
next_nodes.extend([(node.left_node,1),(node.right_node,1)])
while next_nodes:
    node, step = next_nodes.pop()
    if not node.rule in shortcuts:
        shortcuts[node.rule] = step
        next_nodes.extend([(node.left_node,1+step),(node.right_node,1+step)])
    else:
        if shortcuts[node.rule] > step:
            shortcuts[node.rule] = step
# %%
