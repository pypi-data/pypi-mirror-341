from typing import List
from fluss_next.api.schema import NodeFragment, EdgeFragment, DiagramFragment
from fluss_next.traits import Edge


def find_connected_edges(
    node: NodeFragment, diagram: DiagramFragment
) -> List[EdgeFragment]:
    con_edges = []

    for el in diagram.elements:
        if isinstance(el, Edge):
            if el.source == node.id:
                con_edges.append(el)

    return con_edges
