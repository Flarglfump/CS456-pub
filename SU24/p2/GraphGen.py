import random
import networkx as nx
import os

def generate_graph(n, d, graph_type):
  if graph_type == "A": # DAG
    G = nx.DiGraph()
    nodes = list(range(n))
    G.add_nodes_from(nodes)
    random.shuffle(nodes)

    for i in range(n):
      for j in range(i + 1, n):
        if random.random() < d / n:
            new_weight = random.randint(-20, 20)
            while new_weight == 0:
              new_weight = random.randint(-20, 20)
            G.add_edge(nodes[i], nodes[j], weight=new_weight)
  
  elif graph_type == "B": # Positive Cycles
    G = nx.gnm_random_graph(n, d * n, directed=True)
    while nx.is_directed_acyclic_graph(G):
      G = nx.gnm_random_graph(n, d * n, directed=True)
    for (u, v) in G.edges():
      new_weight = random.randint(1, 20)
      while new_weight == 0:
        new_weight = random.randint(1, 20)
      G.edges[u, v]['weight'] = new_weight
  
  elif graph_type == "C": # Negative Weights
    G = nx.gnm_random_graph(n, d * n, directed=True)
    if nx.is_directed_acyclic_graph(G):
      G = nx.gnm_random_graph(n, d * n, directed=True)
    for (u, v) in G.edges():
      new_weight = random.randint(-20, 20)
      while new_weight == 0:
        new_weight = random.randint(-20, 20)
      G.edges[u, v]['weight'] = new_weight
  
  return G

def save_graph_to_file(G, filename):
  with open(filename, 'w') as f:
    f.write(f"{len(G.nodes())} {len(G.edges())}\n")
    for u, v, data in G.edges(data=True):
      f.write(f"{u} {v} {data['weight']}\n")

def main():
  node_counts = [200, 800, 1400]
  
  # "A" for DAG, "B" for Positive Cycles, "C" for Negative Weights
  graph_types = ["A", "B", "C"]

  # Create directory to store graphs
  out_dir = "InputGraphs"
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)

  for graph_type in graph_types:
    for n in node_counts:
      densities = [4, int(n**0.5), int(n/2)]
      for d in densities:
        print(f"Generating n={n}, d={d}, Type={graph_type}...")
        G = generate_graph(n, d, graph_type)
        filename = os.path.join(out_dir, f"n{n}_d{d}_Type{graph_type}.edgelist")
        save_graph_to_file(G, filename)
        print(f"Generated {filename}")

if __name__ == "__main__":
  main()
