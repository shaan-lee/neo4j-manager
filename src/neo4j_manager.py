from neo4j import GraphDatabase


class Neo4jManager:
    def __init__(self, URI, USERNAME, PASSWORD):
        self.URI = URI
        self.AUTH = (USERNAME, PASSWORD)

    def __execute_query(self, query):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            result = driver.execute_query(query)
        return result

    def __convert_to_js_object_str(self, dict):
        return_str = "{"
        for key in dict:
            if return_str != "{":
                return_str += ","
            return_str += key
            return_str += ":"
            if isinstance(dict[key], str):
                return_str += f"'{dict[key]}'"
            else:
                return_str += f"'{dict[key]}'"
        return_str += "}"
        return return_str

    def get_node(self, node_values):
        node_values["values"] = self.__convert_to_js_object_str(
            node_values.get("values")
        )
        results = self.__execute_query(
            "Match (x:%(table)s %(values)s)" "Return x" % node_values
        )
        return results

    def add_node(self, node_values):
        node_values["values"] = self.__convert_to_js_object_str(
            node_values.get("values")
        )
        results = self.__execute_query(
            "Merge (x:%(table)s %(values)s)" "Return x" % node_values
        )
        return results

    def set_relationship(self, from_node_values, relationship, to_node_values):
        from_node_values["values"] = self.__convert_to_js_object_str(
            from_node_values.get("values")
        )
        to_node_values["values"] = self.__convert_to_js_object_str(
            to_node_values.get("values")
        )
        from_match_query = "Match (from:%(table)s %(values)s)" % from_node_values
        to_match_query = "Match (to:%(table)s %(values)s)" % to_node_values
        set_relationship_query = "Merge (from) - [rel:%s] -> (to)" % relationship
        results = self.__execute_query(
            f"""
            {from_match_query}
            {to_match_query}
            {set_relationship_query}
            Return rel
        """
        )
        return results
