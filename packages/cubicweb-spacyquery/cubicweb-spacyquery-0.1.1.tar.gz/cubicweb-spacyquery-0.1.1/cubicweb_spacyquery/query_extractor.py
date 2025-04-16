import networkx as nx

import pandas as pd

tsp = nx.approximation.traveling_salesman_problem


def to_variable(txt):
    return txt.upper()


class QueryExtractor:

    def __init__(self, df, weight_file=None):
        self.df = df
        self.weight_df = None
        if weight_file and weight_file.is_file():
            self.weight_df = pd.read_csv(weight_file, delimiter=";")
        self.graph = nx.Graph()
        for node1, rel, node2 in self.df.values:
            weight = self.compute_weight(node1, rel, node2)
            self.graph.add_edge(node1, node2, title=rel, weight=weight)

    def _get_weight(self, subj, pred, obj):
        selection = self.weight_df[["subj", "pred", "obj"]]
        row = self.weight_df[
            selection.isin({"subj": [subj], "pred": [pred], "obj": [obj]}).all(axis=1)
        ]
        if row.shape and row.shape[0] == 1:
            return row["weight"].iloc[0]

    def compute_weight(self, subj, pred, obj):
        if self.weight_df is None:
            return 1
        weight = self._get_weight(subj, pred, obj)
        if weight is not None:
            return weight
        weight = self._get_weight(subj, pred, "*")
        if weight is not None:
            return weight
        weight = self._get_weight(subj, "*", obj)
        if weight is not None:
            return weight
        weight = self._get_weight("*", pred, obj)
        if weight is not None:
            return weight
        weight = self._get_weight("*", pred, "*")
        if weight is not None:
            return weight
        weight = self._get_weight("*", "*", obj)
        if weight is not None:
            return weight
        return 1

    def get_rel(self, fetype, tetype):
        df = self.df
        try:
            return df[(df["fe"] == fetype) & (df["te"] == tetype)].iloc[0, 1]
        except Exception:
            return df[(df["fe"] == tetype) & (df["te"] == fetype)].iloc[0, 1]

    def get_rel_sub(self, fetype, tetype):
        df = self.df
        try:
            return (df[(df["fe"] == fetype) & (df["te"] == tetype)].iloc[0, 1]), True
        except Exception:
            return (df[(df["fe"] == tetype) & (df["te"] == fetype)].iloc[0, 1]), False

    def get_queries_source_target(self, source, target):
        paths = nx.all_shortest_paths(self.graph, source=source, target=target)
        queries = []
        for path in paths:
            query = []
            for i, node in enumerate(path[:-1]):
                if "#" in node:
                    query.append(" ".join(node.split("#")))
                    continue
                relation = self.get_rel(node, path[i + 1])
                if relation != "attribute":
                    query.append(f"{node} {relation} {path[i+1]}")
                else:
                    query.append(" ".join(path[i + 1].split("#")))
            queries.append(", ".join(query))
        return queries

    def convert_attr_into_rql(self, target_attr, paths):
        definitions = []
        type_to_var = {}
        for attr_type in target_attr:
            descr = attr_type.split("#")
            instance_type, attr_name, expected_value = [None] * 3
            if len(descr) == 2:
                instance_type, attr_name = descr
                attr_code = to_variable(instance_type) + "_" + attr_name.upper()
                type_to_var[attr_type] = attr_code
                definitions.append(f"%({instance_type})s {attr_name} {attr_code}")
            elif len(descr) == 3:
                instance_type, attr_name, expected_value = descr
                self.get_node_var_name(instance_type, type_to_var, definitions)
                definitions.append(
                    f"%({instance_type})s {attr_name} '{expected_value}'"
                )
            elif len(descr) == 4:
                instance_type, attr_name, expected_value, qtype = descr
                self.get_node_var_name(instance_type, type_to_var, definitions)
                if qtype == "I":
                    definitions.append(
                        f"%({instance_type})s {attr_name} ILIKE '{expected_value}'"
                    )
            attr_type = f"{instance_type}#{attr_name}"
            if attr_type in paths:
                paths.remove(attr_type)
        return definitions, type_to_var

    def get_node_var_name(self, node, type_to_var, definitions):
        if node not in type_to_var:
            var_name = to_variable(node)
            definitions.append(f"{var_name} is {node}")
            type_to_var[node] = var_name
        else:
            var_name = type_to_var[node]
        return var_name

    def get_queries(self, target_entity, target_attr):
        target_nodes = target_entity + [
            "#".join(ta.split("#")[:2]) for ta in target_attr
        ]
        if len(target_nodes) == 1:
            (unique_etype,) = target_nodes
            var_name = to_variable(unique_etype)
            return f"Any {var_name} WHERE {var_name} is {unique_etype}"
        paths = tsp(self.graph, nodes=target_nodes, cycle=False)

        query = []
        definitions, type_to_var = self.convert_attr_into_rql(target_attr, paths)
        for i, node in enumerate(paths[:-1]):
            node_obj = paths[i + 1]
            if node == node_obj:
                continue  # XXX could be possible with two different entity of same type
            relation, is_subject = self.get_rel_sub(node, node_obj)
            node_varname = self.get_node_var_name(node, type_to_var, definitions)
            node_obj_varname = self.get_node_var_name(
                node_obj, type_to_var, definitions
            )

            if is_subject:
                sub_path = f"{node_varname} {relation} {node_obj_varname}"
                if sub_path not in query:
                    query.append(sub_path)
            else:
                sub_path = f"{node_obj_varname} {relation} {node_varname}"
                if sub_path not in query:
                    query.append(sub_path)
        if len(paths) == 1:
            (node_obj,) = paths
            node_obj_varname = self.get_node_var_name(
                node_obj, type_to_var, definitions
            )

        definitions = [dd % type_to_var for dd in definitions]
        beg_query = f"Any {', '.join(type_to_var.values())} WHERE "
        if query:
            query_txt = f"{beg_query}{', '.join(definitions)}, {', '.join(query)}"
        else:
            query_txt = f"{beg_query}{', '.join(definitions)}"

        return query_txt
