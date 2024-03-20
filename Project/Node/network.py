class Network:

    # Initialize a set to store node addresses
    def __init__(self):
        self.nodes = set()
    
    # Add a node to the network
    def register_node(self, address):
        self.nodes.add(address)

    # Remove a node from the network
    def remove_node(self, address):
        self.nodes.discard(address)

    # Print a list of all the nodes in the network
    def get_nodes(self):
        return list(self.nodes)