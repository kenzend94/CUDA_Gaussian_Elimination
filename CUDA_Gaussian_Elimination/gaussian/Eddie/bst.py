'''
Project BDD 
Chandler Welch
2023.12.18
'''

import graphviz


class BDDNode:
    def __init__(self, variable, low, high):
        self.variable = variable
        self.low = low
        self.high = high
    def __str__(self) -> str:
        
        return str(self.variable)
    def __repr__(self) -> str:
        return str(self.variable)
        

class BDD:
    def __init__(self):
        self.root = None
        self.unique_table = {}
        self.terminal_nodes = {0: BDDNode(0, None, None), 1: BDDNode(1, None, None)}

    def make_node(self, variable, low, high):
        # Apply reduction rules
        if low == high:
            return low

        # Check for existing node
        key = (variable, low, high)
        if key in self.unique_table:
            return self.unique_table[key]

        # Create new node
        new_node = BDDNode(variable, low, high)
        self.unique_table[key] = new_node
        return new_node

    def evaluate(self, node, assignment):
        if node in self.terminal_nodes.values():
            return int(node == self.terminal_nodes[1])

        if assignment[node.variable]:
            return self.evaluate(node.high, assignment)
        else:
            return self.evaluate(node.low, assignment)
        ################# FIX THIS NOT RETURN A LIST


    def find(self, value=None, node=None, ordered=None):
        '''Return a list with the data items in order of inorder traversal.'''
        if ordered is None and node is None:
            if value in self.terminal_nodes.values():
            
                return value
            elif value in '01':
                node = self.terminal_nodes[int(value)]
                return node
            if self.root is None:
                node = value
                return node
            node = self.root
            ordered = []
        if node is None:
            return None

        ordered = self.inorder()
        for i in ordered:
            if i.variable == value:
                return i
            
        return None

        # Check if the current node is the target
        '''if node.variable == value:
            return node'''

        # Search in left and right children
        #left_search = self.find(value, node=node.low)
        #right_search = self.find(value, node=node.high)

        #return left_search or right_search

        #return ordered
    @staticmethod
    def bdd_and(bdd1, bdd2):
        bdd1.terminal_nodes[1] = bdd2.root
        bdd1.terminal_nodes[0] = bdd2.terminal_nodes[0]
        bdd2.root = bdd1.root
        return bdd2


    def inorder(self, node=None, ordered=None):
        '''Return a list with the data items in order of inorder traversal.'''
        if ordered is None and node is None:
            node = self.root
            if self.root is None:
                return ['1','0']
            ordered = []
        if node.high is not None:
            self.inorder(node.high, ordered=ordered)
        ordered.append(node)
        if node.low is not None:
            self.inorder(node.low, ordered=ordered)
        return ordered

    def create_dotfile(self):
        """ This function will create a DOT file for the tree.  
        Args:
            tree_data (BST): A Binary Search Tree.
        """
        global NODE_COUNT
        NODE_COUNT = -1
        graph = graphviz.Digraph(name='digraph', format='png')
        graph.graph_attr = {'bgcolor':'black', 'textcolor':'white'}
        NODE_COUNT=2
        self.node_1 = graph.node('Node 1', label='1', color='white', fontcolor='white', shape='square')
        self.node_0 = graph.node('Node 0', label='0', color='white', fontcolor='white', shape='square')
        self.walk_tree_print_df(self.root, graph)
        temp = graph.render('BDDtree').replace('\\', '/')
        #graph.save('tree.png')
        """dotfile = open("tree.dot", "w")
      dotfile.write("digraph G {\n")
      dotfile.write(f"{self.walk_tree_print_df(self.root, dotfile)}\n")
      dotfile.write("}")
      dotfile.close()  """  
        
    #@staticmethod    
    def walk_tree_print_df(self,node, graph):

        """ This function will walk the tree and print the nodes to a DOT file
        Args:
            node: Node from BST
            dotfile (File Object): DOT file describing the tree
        Returns:
            String: Unique node identifier for visualization.
        """
        global NODE_COUNT
        if node is None:
            return None
        
          
        # name node with unique id
        
        if not (node in self.terminal_nodes.values()):
            NODE_COUNT += 1
            node_name = f'Node {NODE_COUNT}'
            tempNode = graph.node(node_name, label=node.variable, color='white', fontcolor='white')
              
        if node in self.terminal_nodes.values():
                value = int(node == self.terminal_nodes[1])
                '''if value:
                    graph.edge(node_name, self.node_1, style='dotted', fontcolor='white')
                else:
                    graph.edge(node_name, self.node_0, style='dotted', fontcolor='white')'''
                return f'Node {value}'
        
        #graph.node(tempNode)
        #dotfile.write(f"{node_name} [label = \"{node_name}\n{node.variable}\"]\n")
        # print edges to children
        # traverse left subtree
        
        left = self.walk_tree_print_df(node.low, graph)
        
        if left is not None:
            #print(left.value, left.variable)
            

            graph.edge(node_name, left, style='dashed', color='white')
            #dotfile.write(f"{node_name} -> {left}\n")
        # traverse right subtree
        right = self.walk_tree_print_df(node.high, graph)
        if right is not None:
            '''if right in self.terminal_nodes.values():
                print('here')
                value = int(left == self.terminal_nodes[1])
                if value:
                    graph.edge(node_name, self.node_1, fontcolor='white')
                else:
                    graph.edge(node_name, self.node_0, fontcolor='white')
                return node_name'''
            graph.edge(node_name, right, color='white')
            #dotfile.write(f"{node_name} -> {right}\n")
        return node_name


'''# Example Usage
bdd = BDD()
# Create nodes and add them to the BDD
# Note: '0' and '1' are used as indices for terminal nodes
node_a = bdd.make_node('a', bdd.terminal_nodes[0], bdd.terminal_nodes[1])
node_b = bdd.make_node('b', bdd.terminal_nodes[0], node_a)

# Evaluate the BDD for a particular assignment
assignment = {'a': True, 'b': True}
result = bdd.evaluate(node_b, assignment)
print(result)'''

if __name__ == '__main__':
    # Example Usage
    bdd1 = BDD()
    bdd2 = BDD()
    new_bdd = BDD()
    # Create nodes and add them to the BDD
    # Note: '0' and '1' are used as indices for terminal nodes

    function = "a+bc+!a!b"
    node_c = bdd2.make_node('c', bdd2.terminal_nodes[0], bdd2.terminal_nodes[1])
    node_d = bdd2.make_node('d', bdd2.terminal_nodes[0], node_c)
    node_e = bdd2.make_node('e', node_d, node_c)
    node_f = bdd2.make_node('f', bdd2.terminal_nodes[1], node_e)
    node_g = bdd2.make_node('g', node_f, node_d)

    
    bdd2.root = node_g
    node_a = bdd1.make_node('a', bdd1.terminal_nodes[0], bdd1.terminal_nodes[1])
    node_b = bdd1.make_node('b', bdd1.terminal_nodes[0], node_a)
    bdd1.root = node_a

    new_bdd = BDD.bdd_and(bdd1,bdd2)

    print(bdd2.inorder())
    # Evaluate the BDD for a particular assignment
    assignment = {'a': True, 'b': True}
    assignment2 = {'c': False, 'd':True, 'e': False, 'f':True, 'g': False, 'h':True, 'i': False, 'j':True,}
    #result = bdd.evaluate(node_b, assignment)
    result2 = bdd2.evaluate(node_g, assignment2)
    #print(result, result2)

    print(new_bdd.inorder())
