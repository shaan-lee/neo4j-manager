"""
manager class about neo4j query
"""
from neo4j import GraphDatabase


class Neo4jManager:
    """
    neo4j driver manager

    args:
        neo4j uri: require, str
        neo4j username: require, str
        neo4j password: require, str
    """

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

    def get_node(
        self,
        conditions: dict,
        label: str = None,
    ):
        """
        get node about match with conditions, label
        when table is empty, find in all of label

        label (str): optional (default to None. if you can identify node only condition, you can keep empty)
        conditions (dict): require (about node property)

        Returns:
            type: EagerResult
        """
        conditions = self.__convert_to_js_object_str(conditions)
        results = self.__execute_query(f"Match (x:{label} {conditions})" "Return x")
        return results

    def add_node(self, conditions: dict, label: str):
        """
        add node about conditions, label

        label (str): require
        conditions (dict): require (about node property)

        Returns:
            type: EagerResult
        """
        conditions = self.__convert_to_js_object_str(conditions)
        results = self.__execute_query(f"Merge (x:{label} {conditions})" "Return x")
        return results

    def delete_node(self, conditions: dict, label: str = None):
        """
        delete node about match with conditions, label

        label (str): optioinal
        conditions (dict): require (about node property)

        Returns:
            NONE
        """
        conditions = self.__convert_to_js_object_str(conditions)
        self.__execute_query(
            f"Match (x:{label} {conditions}) - [r1] -> ()"
            f"Match (x:{label} {conditions}) <- [r2] - ()"
            "Delete r1, r2, x"
        )

    def set_relationship(
        self,
        relationship: str,
        from_condition: dict,
        from_label: str,
        to_condition: dict,
        to_label: str,
    ):
        """
        set relationship each matched node

        relationship (str): require (relationship name to use)

        from_condition (dict): require
        from_label (str): require

        to_condition (dict): require
        to_label (str): require

        Returns:
            type: EagerResult
        """
        from_condition = self.__convert_to_js_object_str(from_condition)
        to_condition = self.__convert_to_js_object_str(to_condition)
        results = self.__execute_query(
            f"""
            Match (from:{from_label} {from_condition})
            Match (to:{to_label} {to_condition})
            With from, to
            Merge r=(from)-[rel:{relationship}]->(to)
            Return r
        """
        )
        return results

    def get_relationed_nodes_from_node(
        self,
        conditions: dict,
        label: str = None,
    ):
        """
        get any relationshiped nodes from match node

        conditions: require
        label: optional

        Returns:
            EagerResult
        """
        conditions = self.__convert_to_js_object_str(conditions)
        results = self.__execute_query(
            f"""
            Match ({label} {conditions}) <--> (r)
            Return r
        """
        )
        return results

    def get_relations(self, relationship=""):
        """
        get all relations about relationship name
        if relationship arg is empty, get all about relationship name

        relathionship: optional, str default to ""

        Returns:
            EagerResult
        """
        if relationship:
            relationship = ":" + relationship
        results = self.__execute_query(
            f"""
            Match r=()-[{relationship}]->()
            Return r
        """
        )
        return results
