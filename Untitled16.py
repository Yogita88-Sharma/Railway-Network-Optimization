#!/usr/bin/env python
# coding: utf-8

# # Railway Network Optimization: Streamlining Routes with Graph and Algorithms🌸

# In[ ]:


import networkx as nx
import matplotlib.pyplot as plt
import os

def create_graph(num_stations):
    G = nx.DiGraph()

    for i in range(num_stations):
        for j in range(i + 1, num_stations):
            try:
                distance_input = input(f"Enter distance between station {i + 1} and {j + 1} (press Enter to skip): 🙂 ")
                if distance_input == '':
                    continue  # Skip this edge if the user pressed Enter without entering a distance
                distance = int(distance_input)
            except ValueError:
                print("Invalid input. Please enter a valid integer. 🤔 ")
                continue  # Retry this iteration to get a valid input

            G.add_edge(i, j, weight=distance)

    draw_graph(G, title="Directed Railway Network ")  # Show the directed graph after taking input distances
    return G

def draw_graph(G, title="Directed Railway Network "):
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    node_labels = {i: i + 1 for i in G.nodes()}  # Label nodes starting from 1
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="red", font_size=10, font_color="black", labels=node_labels, connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(title)
    plt.show()

def dijkstra_shortest_path(G, source, destination):
    shortest_path = nx.shortest_path(G, source=source, target=destination, weight='weight')
    shortest_path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]

    G_shortest = G.edge_subgraph(shortest_path_edges)
    draw_graph(G_shortest, title="Shortest Path ")
    return shortest_path

def kruskal_minimum_spanning_tree(G):
    mst_edges = nx.minimum_spanning_edges(G.to_undirected(), algorithm='kruskal', data=False)
    mst_edges_list = list(mst_edges)

    G_mst = G.edge_subgraph(mst_edges_list)
    draw_graph(G_mst, title="Minimum Spanning Tree ❄️ ")
    return mst_edges_list

def visualize_centrality(G):
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

    # Scale centrality measures for better visualization
    scaled_degree_centrality = [3000 * val for val in degree_centrality.values()]
    scaled_betweenness_centrality = [3000 * val for val in betweenness_centrality.values()]

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=scaled_degree_centrality, node_color="skyblue", font_size=10, font_color="black", labels={i: i + 1 for i in G.nodes()})
    nx.draw_networkx_nodes(G, pos, node_size=scaled_betweenness_centrality, node_color="salmon", alpha=0.5)

    plt.title("Centrality Visualization")
    plt.show()

def export_graph(G, filename):
    nx.write_gpickle(G, filename)
    print(f"Graph saved to {filename}")

def import_graph(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return None

    try:
        G = nx.read_gpickle(filename)
        draw_graph(G, title="Imported Graph")
        return G
    except Exception as e:
        print(f"Error: Failed to import graph from '{filename}'.")
        print(f"Exception: {e}")
        return None

def main():
    num_stations = int(input("Enter the number of stations: 🙂 "))
    G = create_graph(num_stations)

    while True:
        print("\nOptions:")
        print("1. Find Shortest Path using Dijkstra's Algorithm 🟢 ")
        print("2. Cover Every Station with Shortest Path using Kruskal's Algorithm 🟡")
        print("3. Visualize Centrality Measures 🔄")
        print("4. Export Graph 📤")
        print("5. Import Graph 📥")
        print("6. Exit ⛔")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            try:
                source = int(input("Enter the source station: ⛳ ")) - 1
                destination = int(input("Enter the destination station: ⛳ ")) - 1
                if source < 0 or source >= num_stations or destination < 0 or destination >= num_stations:
                    print("Invalid source or destination. Please enter valid node indices.")
                    continue
            except ValueError:
                print("Invalid input. Please enter valid integers for source and destination.")
                continue

            shortest_path = dijkstra_shortest_path(G, source, destination)
            print(f"Shortest Path: {shortest_path}")

            cover_all = input("Do you want to cover every station? (Yes/No): ").lower()
            if cover_all == 'yes':
                mst_edges = kruskal_minimum_spanning_tree(G)
                print(f"Minimum Spanning Tree Edges: {mst_edges}")

        elif choice == '2':
            mst_edges = kruskal_minimum_spanning_tree(G)
            print(f"Minimum Spanning Tree Edges: {mst_edges}")

            destination_to_source = input("Do you want to go from destination to source? (Yes/No): ").lower()
            if destination_to_source == 'yes':
                reversed_mst_edges = [(edge[1], edge[0]) for edge in mst_edges]
                reversed_mst_edges.sort()
                draw_graph(G.edge_subgraph(reversed_mst_edges), title="Reversed Minimum Spanning Tree")

        elif choice == '3':
            visualize_centrality(G)

        elif choice == '4':
            filename = input("Enter the filename to save the graph: ")
            export_graph(G, filename)

        elif choice == '5':
            filename = input("Enter the filename to import the graph: ")
            G = import_graph(filename)

        elif choice == '6':
            print("Exiting the program. Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()


# In[ ]:




