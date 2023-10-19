"""
manager class about neo4j query
"""
from neo4j import GraphDatabase


class Neo4jManager:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.auth = (username, password)
        self.driver = GraphDatabase.driver(uri=self.uri, auth=self.auth)

    def __execute_query(self, query):
        result = self.driver.execute_query(query)
        return result

    def __convert_to_js_object_str(self, target_dict):
        return_str = "{"
        for key in target_dict:
            if return_str != "{":
                return_str += ","
            return_str += key
            return_str += ":"
            if isinstance(target_dict[key], str):
                return_str += f"'{target_dict[key]}'"
            else:
                return_str += f"'{target_dict[key]}'"
        return_str += "}"
        return return_str

    def get_node(self, node_values):
        """
        get node match with given node_values

        node_values (dict):
            table: require
            values: require (about node condition or data)

        Returns:
            type: EagerResult
        """
        node_values["values"] = self.__convert_to_js_object_str(
            node_values.get("values")
        )
        results = self.__execute_query(
            f"Match (x:{node_values.get('table')} {node_values.get('values')})"
            "Return x"
        )
        # "Match (x:%(table)s %(values)s)" "Return x" % node_values
        return results

    def add_node(self, node_values):
        """
        add node with node_values

        node_values (dict):
            table: require
            values: require (about node condition or data)

        Returns:
            type: EagerResult
        """
        node_values["values"] = self.__convert_to_js_object_str(
            node_values.get("values")
        )
        results = self.__execute_query(
            f"Merge (x:{node_values.get('table')} {node_values.get('values')})"
            "Return x"
        )
        return results

    def set_relationship(self, from_node_values, to_node_values, relationship):
        """
        set relationship each matched node

        from_node_values (dict):
            having relationship node values
            table: require
            values: require (about node condition or data)

        to_node_values (dict):
            target relationship node values
            table: require
            values: require (about node condition or data)

        relationship (str): require (relationship name to use)

        Returns:
            type: EagerResult


        """
        from_node_values["values"] = self.__convert_to_js_object_str(
            from_node_values.get("values")
        )
        to_node_values["values"] = self.__convert_to_js_object_str(
            to_node_values.get("values")
        )
        results = self.__execute_query(
            f"""
            Match (from:{from_node_values.get('table')} {from_node_values.get('values')})
            Match (to:{to_node_values.get('table')} {to_node_values.get('values')})
            Merge r=(from)-[rel:{relationship}]->(to)
            Return r
        """
        )
        return results
