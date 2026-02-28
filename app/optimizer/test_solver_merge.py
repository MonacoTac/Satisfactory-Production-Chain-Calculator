import pytest

from optimizer.solver import calculate_production_chain
from optimizer.objectives import OptimizationObjective


def test_merge_nodes_same_item():
    """Nodes producing the same item should be merged into a single node."""
    # use a complex item so multiple intermediate nodes exist
    result = calculate_production_chain(
        target_item_id="ai_expansion_server",
        target_rate=1,
        unlocked_recipes=set(),
        objective=OptimizationObjective.MINIMIZE_MACHINES,
        allow_locked_preview=True,
    )

    # collect item_ids produced by each node
    produced = [n.item_produced for n in result.nodes]
    # ensure each item only appears once
    assert len(produced) == len(set(produced)), "Duplicate production nodes remain"

    # specifically check a couple of items we know were duplicated before
    items_to_check = ["iron_ingot", "copper_ingot"]
    for item in items_to_check:
        nodes = [n for n in result.nodes if n.item_produced == item]
        assert len(nodes) == 1, f"Item {item} was not merged"


if __name__ == "__main__":
    pytest.main([__file__])
