import copy
import json
import matplotlib.pyplot as plt
import networkx as nx
import src.steiner as steiner


def execute_pso_and_graph(max_iteration, swarm_amount, population_size, initial_points):
    font = 'caladea'
    font_size = 10
    plt.rcParams["font.family"] = "caladea"
    edge_color = "#511F29"
    node_color = "#DA536E"
    s = steiner.Steiner(initial_points)
    s.calculate_minimum_euclidean_tree()
    s.calculate_total_tree_weight()
    original_tree = s.tree
    original_edges = [(u, v) for (u, v, d) in original_tree.edges(data=True)]
    vertex_dict = {v: [v[0], v[1]] for v in original_tree.nodes}
    vertex_labels = {v: [float(f'{v[0]:.2f}'), float(f'{v[1]:.2f}')]
                     for v in original_tree.nodes}
    plt.subplot(121)
    plt.title("Original tree", fontsize=font_size)
    nx.draw_networkx_nodes(original_tree, vertex_dict, node_size=350, node_color=node_color)
    nx.draw_networkx_edges(original_tree, vertex_dict, edgelist=original_edges, width=2, edge_color=edge_color)
    nx.draw_networkx_labels(original_tree, vertex_dict, font_size=font_size, font_family=font,
                            labels=vertex_labels)
    original_tree_labels = {key: float(f'{value:.2f}') for key, value in
                            nx.get_edge_attributes(original_tree, "weight").items()}
    nx.draw_networkx_edge_labels(original_tree, vertex_dict, original_tree_labels,
                                 font_size=font_size, font_family=font)

    s.steiner_particle_optimization(max_iteration, swarm_amount, population_size)
    steiner_graph = s.tree
    steiner_tree = nx.minimum_spanning_tree(steiner_graph)
    steiner_tree_edges = [(u, v) for (u, v, d) in steiner_tree.edges(data=True)]
    steiner_vertex_dict = {v: [v[0], v[1]] for v in steiner_tree.nodes}
    steiner_vertex_labels = {v: [float(f'{v[0]:.2f}'), float(f'{v[1]:.2f}')]
                             for v in steiner_tree.nodes}

    plt.subplot(122)
    plt.title("Tree with Steiner points", fontsize=font_size)
    nx.draw_networkx_nodes(steiner_tree, steiner_vertex_dict, node_size=350, node_color=node_color)
    nx.draw_networkx_edges(steiner_tree, steiner_vertex_dict, edgelist=steiner_tree_edges, width=2,
                           edge_color=edge_color)
    nx.draw_networkx_labels(steiner_tree, steiner_vertex_dict, font_size=font_size, font_family=font,
                            labels=steiner_vertex_labels)
    etiquetas_arbol_steiner = {key: float(f'{value:.2f}') for key, value in
                               nx.get_edge_attributes(steiner_tree, "weight").items()}
    nx.draw_networkx_edge_labels(steiner_tree, steiner_vertex_dict, etiquetas_arbol_steiner,
                                 font_size=font_size, font_family=font)
    plt.show()


def original_points_with_steiner_points_graph(original_points, steiner_points, title):
    font_size = 10
    plt.rcParams["font.family"] = "caladea"
    edges_color = "#49817A"
    original_points_color = "#DA536E"
    steiner_color = "#00C9B8"
    steiner_original = steiner.Steiner(original_points.copy())
    steiner_original.calculate_minimum_euclidean_tree()
    steiner_original.calculate_total_tree_weight()
    steiner_steiner = steiner.Steiner(steiner_points.copy())
    steiner_steiner.calculate_minimum_euclidean_tree()
    steiner_act = steiner.Steiner(original_points.copy() + steiner_points.copy())
    steiner_act.calculate_minimum_euclidean_tree()
    tree_act = steiner_act.tree
    edges_act = [(u, v) for (u, v, d) in tree_act.edges(data=True)]
    original_vertex = {v: [v[0], v[1]] for v in steiner_original.tree.nodes}
    steiner_vertex = {v: [v[0], v[1]] for v in steiner_steiner.tree.nodes}
    vertex_act = {v: [v[0], v[1]] for v in tree_act.nodes}
    plt.title(title, fontsize=font_size)
    nx.draw_networkx_nodes(steiner_original.tree, original_vertex, node_size=30, node_color=original_points_color)
    nx.draw_networkx_nodes(steiner_steiner.tree, steiner_vertex, node_size=30, node_color=steiner_color)
    nx.draw_networkx_edges(tree_act, vertex_act, edgelist=edges_act, width=2, edge_color=edges_color)

    plt.show()


def execute_pso_from_file(file_name):
    file = open(file_name)
    data = json.load(file)
    max_iteration = data['max_iteration']
    swarm_amount = data['swarm_amount']
    population_size = data['population_size']
    executions = data["executions"]
    found_points_json = data['found_points']
    original_points = data['original_points']
    s_original = steiner.Steiner(copy.copy(original_points))
    s_original.calculate_minimum_euclidean_tree()
    s_original.calculate_total_tree_weight()
    minimum_weight = s_original.weight
    steiner_points = copy.copy(s_original.points)
    st = steiner.Steiner(original_points.copy())
    for i in range(executions):
        st.set_steiner(original_points.copy())
        st.calculate_minimum_euclidean_tree()
        st.calculate_total_tree_weight()
        st.steiner_particle_optimization(max_iteration, swarm_amount, population_size, len(found_points_json))
        if st.weight < minimum_weight:
            minimum_weight = copy.copy(st.weight)
            steiner_points = st.points.copy()
            print("Improves minimum weight ", steiner_points, minimum_weight)
        st.delete_steiner()
    file_name_without_ext = file_name[0:file_name.rindex('.')]
    new_file = file_name_without_ext + "_results.json"
    new_data = {'original_weight': s_original.weight,
                'improved_weight': minimum_weight,
                'improvement_percentage': 100 - (minimum_weight * 100 / s_original.weight),
                'found_points': steiner_points}
    with open(new_file, 'w') as outfile:
        outfile.write(json.dumps(new_data, indent=2))


if __name__ == '__main__':
    # filename = input()
    file = open('../Examples/decroos-example.json')
    data = json.load(file)
    # execute_pso_and_graph(30, 10, 15, [(-4, 0), (0, 6), (4, 0)])
    max_iteration = data['max_iteration']
    swarm_amount = data['swarm_amount']
    population_size = data['population_size']
    executions = data["executions"]
    found_points_json = data['found_points']
    original_points = data['original_points']

    s_original = steiner.Steiner(copy.copy(original_points))
    s_original.calculate_minimum_euclidean_tree()
    s_original.calculate_total_tree_weight()
    minimum_weight = s_original.weight
    steiner_points = copy.copy(s_original.points)
    # st = steiner.Steiner(original_points.copy())

    # steiner_points = [[20307.81814400283, 3804.0630296756885]]

    # results_bib = "Steiner tree in bibliography"
    # obt_tree = "Obtained tree"
    # or_tree = "Original tree"
    # original_points_with_steiner_points_graph(original_points, steiner_points, obt_tree)    # For plotting
    execute_pso_from_file("../Examples/example-1.json")
    # s = steiner.Steiner(steiner_points + data["found_points"])
    # s.calculate_minimum_euclidean_tree()
    # s.calculate_total_tree_weight()
    # print("Beginning ------> Original weight ", s.weight, " points ", s.points) # For plotting original tree
