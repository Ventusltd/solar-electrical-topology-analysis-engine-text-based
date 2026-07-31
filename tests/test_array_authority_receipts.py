from array_engine import reference_24_by_30_build
from array_routing import (
    ModuleTerminalLayout,
    RoutingConfig,
    routing_payload,
)
from array_topology import topology_payload


def test_topology_payload_contains_the_equipment_graph() -> None:
    build = reference_24_by_30_build()
    payload = topology_payload(build.topology)

    assert len(payload["equipment_nodes"]) == 74
    assert len(payload["equipment_edges"]) == 120
    assert payload["node_count"] == build.topology.node_count
    assert payload["edge_count"] == build.topology.edge_count


def test_routing_payload_contains_terminal_evidence_metadata() -> None:
    build = reference_24_by_30_build(
        routing_config=RoutingConfig(
            terminal_layout=ModuleTerminalLayout(
                evidence_class="measured",
                source_reference="field-survey-001",
            )
        )
    )
    payload = routing_payload(build.routing)

    terminal_layout = payload["routing_config"]["terminal_layout"]
    assert terminal_layout["evidence_class"] == "measured"
    assert terminal_layout["source_reference"] == "field-survey-001"
