# Doing what?
- this repository does managing neo4j cypher query to use easy

# How to use?
- you can use easy like below code
### usecase
```
    from src.neo4j_manager import Neo4jManager

    manager = Neo4jManager(
        <your neo4j workspace uri>,
        <your neo4j workspace username>,
        <your neo4j workspace password>,
    )

    node = manager.get_node(node_values={"table": "User", "values": {"name": "test"}})

```
### Return value
- EagerResult