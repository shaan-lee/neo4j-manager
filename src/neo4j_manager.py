from neo4j import GraphDatabase


class Neo4jManager:
    def __init__(self, URI, USERNAME, PASSWORD):
        self.URI = URI
        self.AUTH = (USERNAME, PASSWORD)
