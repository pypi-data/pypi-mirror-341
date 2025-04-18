from typing import Dict, Any, List
import math
from .vars import current_ontology, current_graph
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from kraph.api.schema import MeasurementKind

def create_linked_expression(expression, graph=None):
    from kraph.api.schema import link_expression

    if graph is None:
        graph = current_graph.get()

    assert graph is not None, "Graph must be set"

    return link_expression(expression=expression, graph=graph)


def s(name, description=None):
    from kraph.api.schema import create_structure_category

    exp = create_structure_category(
        label=name,
        graph=current_graph.get(),
        description=description,
    )
    return exp


def new_entity(name, description=None):
    from kraph.api.schema import create_entity_category

    exp = create_entity_category(
        graph=current_graph.get(),
        label=name,
        description=description,
    )
    return exp


def new_relation(name, description=None):
    from kraph.api.schema import create_relation_category

    exp = create_relation_category(
        label=name,
        graph=current_graph.get(),
        description=description,
    )
    return exp


def new_metric(name, metric_kind, description=None):
    from kraph.api.schema import create_metric_category

    exp = create_metric_category(
        label=name,
        kind=metric_kind,
        graph=current_graph.get(),
        description=description,
    )
    return exp
