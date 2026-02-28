"""
Production chain solver - core algorithm for computing optimal production chains.

This implementation supports fractional machine counts and properly aggregates
requirements from multiple branches of the dependency tree. Accurate input/
output ratios are maintained and connections between machines are split
proportionally when an item is produced by multiple nodes.
"""

from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import uuid

from data import satisfactory_db
from optimizer.models import (
    MachineNode, Connection, RawResourceRequirement, ProductionChainResult,
    ItemFlow, OptimizationObjective, CalculationStatus
)
from optimizer.objectives import select_best_recipe


class ProductionChainSolver:
    """Solves production chains for Satisfactory items."""
    
    def __init__(
        self,
        unlocked_recipes: Set[str],
        objective: OptimizationObjective = OptimizationObjective.BALANCED
    ):
        """
        Initialize the solver.
        
        Args:
            unlocked_recipes: Set of unlocked recipe IDs
            objective: Optimization objective
        """
        self.unlocked_recipes = unlocked_recipes
        self.objective = objective
        self.all_items = satisfactory_db.get_all_items()
        self.all_recipes = satisfactory_db.get_all_recipes()
        self.raw_resources = satisfactory_db.get_raw_resources()
        
        # State tracking
        self.nodes: List[MachineNode] = []
        self.connections: List[Connection] = []
        self.raw_requirements: Dict[str, float] = {}  # item_id -> rate
        self.item_production: Dict[str, List[str]] = {}  # item_id -> [node_ids producing it]
        # Note: visited_items tracking removed to allow multiple branches of same item
        self.visited_items: Set[str] = set()  # legacy, unused
        self.processing_stack: List[str] = []  # For cycle detection
        
    def solve(
        self,
        target_item_id: str,
        target_rate: float,
        allow_locked_preview: bool = False
    ) -> ProductionChainResult:
        """
        Solve the production chain for a target item.
        
        Args:
            target_item_id: Item to produce
            target_rate: Desired production rate (items/min)
            allow_locked_preview: If True, temporarily enable locked recipes for preview
        
        Returns:
            ProductionChainResult with the solution
        """
        # Initialize result
        target_item = self.all_items.get(target_item_id)
        if not target_item:
            result = ProductionChainResult(
                status=CalculationStatus.IMPOSSIBLE_RATE,
                target_item_id=target_item_id,
                target_item_name="Unknown",
                target_rate=target_rate,
                optimization_objective=self.objective
            )
            result.add_message(f"Item '{target_item_id}' not found in database.")
            return result
        
        result = ProductionChainResult(
            status=CalculationStatus.SUCCESS,
            target_item_id=target_item_id,
            target_item_name=target_item["name"],
            target_rate=target_rate,
            unlocked_recipes=self.unlocked_recipes.copy(),
            optimization_objective=self.objective,
            timestamp=datetime.now().isoformat()
        )
        
        # Check if target is a raw resource
        if target_item["isRawResource"]:
            self.raw_requirements[target_item_id] = target_rate
            result.raw_resources.append(RawResourceRequirement(
                item_id=target_item_id,
                item_name=target_item["name"],
                rate=target_rate
            ))
            result.add_message(f"{target_item['name']} is a raw resource. Required: {target_rate:.2f}/min")
            result.calculate_summary()
            return result
        
        # Reset state
        self.nodes = []
        self.connections = []
        self.raw_requirements = {}
        self.item_production = {}
        self.processing_stack = []
        
        # Recursively build production chain
        success = self._build_chain(
            item_id=target_item_id,
            required_rate=target_rate,
            allow_locked=allow_locked_preview,
            result=result
        )
        
        if not success:
            if result.missing_recipes:
                result.status = CalculationStatus.INSUFFICIENT_RECIPES
                result.add_message(
                    f"Cannot produce {target_item['name']} - missing recipes. "
                    f"Unlock the following: {', '.join(result.missing_recipes)}"
                )
            else:
                result.status = CalculationStatus.IMPOSSIBLE_RATE
                result.add_message(f"Cannot produce {target_item['name']} at the requested rate.")
        
        # Build result
        result.nodes = self.nodes
        result.connections = self.connections
        result.raw_resources = [
            RawResourceRequirement(
                item_id=item_id,
                item_name=self.all_items[item_id]["name"],
                rate=rate
            )
            for item_id, rate in self.raw_requirements.items()
        ]
        
        # Calculate summary
        result.calculate_summary()
        
        return result
    
    def _build_chain(
        self,
        item_id: str,
        required_rate: float,
        allow_locked: bool,
        result: ProductionChainResult
    ) -> bool:
        """
        Recursively build production chain for an item.
        
        Args:
            item_id: Item to produce
            required_rate: Required production rate
            allow_locked: Allow locked recipes
            result: Result object to populate
        
        Returns:
            True if successful, False otherwise
        """
        item = self.all_items.get(item_id)
        if not item:
            return False
        
        # Check for circular dependency
        if item_id in self.processing_stack:
            # Circular dependency detected - mark as recycling loop
            result.add_warning(f"Circular dependency detected for {item['name']} - recycling loop")
            return True  # Don't fail, just mark it
        
        # Mark as being processed
        self.processing_stack.append(item_id)
        
        # If it's a raw resource, add to requirements
        if item["isRawResource"]:
            if item_id not in self.raw_requirements:
                self.raw_requirements[item_id] = 0
            self.raw_requirements[item_id] += required_rate
            self.processing_stack.remove(item_id)
            return True
        
        # Find recipes that produce this item
        producing_recipes = satisfactory_db.get_recipes_for_item(item_id)
        if not producing_recipes:
            result.add_message(f"No recipes found for {item['name']}")
            self.processing_stack.remove(item_id)
            return False
        
        # Select best recipe
        unlocked_set = None if allow_locked else self.unlocked_recipes
        best_recipe = select_best_recipe(
            recipes=producing_recipes,
            objective=self.objective,
            target_rate=required_rate,
            unlocked_only=not allow_locked,
            unlocked_recipes=unlocked_set
        )
        
        if not best_recipe:
            # No unlocked recipe available
            recipe_names = [r["name"] for r in producing_recipes]
            result.add_missing_recipe(f"{item['name']} (options: {', '.join(recipe_names)})")
            self.processing_stack.remove(item_id)
            return False
        
        # In this dataset the "amount" field is already the per-minute
        # output of a single machine at 100% clock.  Crafting speed is
        # retained for informational purposes but is not used in rate
        # calculations.  This avoids the previous behaviour that blew up
        # throughputs by multiplying twice.
        output_data = next(
            (out for out in best_recipe["outputs"] if out["item"] == item_id),
            best_recipe["outputs"][0]
        )
        output_amount = output_data["amount"]
        output_rate_per_machine = output_amount
        
        # Calculate machines needed as whole units. Building counts are
        # integers; any excess capacity is absorbed by running the machines at
        # a lower clock speed.
        import math
        machines_needed = math.ceil(required_rate / output_rate_per_machine) if output_rate_per_machine > 0 else 0

        # compute clock speed percentage such that machines_needed *
        # output_rate_per_machine * (clock_speed/100) == required_rate
        if machines_needed > 0 and output_rate_per_machine > 0:
            clock_speed = min(100.0, (required_rate / (machines_needed * output_rate_per_machine)) * 100.0)
        else:
            clock_speed = 100.0
        
        # Create machine node with integer count and computed clock speed
        node_id = f"node_{len(self.nodes)}_{item_id}"
        node = MachineNode(
            node_id=node_id,
            recipe_id=best_recipe["id"],
            recipe_name=best_recipe["name"],
            machine_type=best_recipe["machineType"],
            item_produced=item_id,
            item_produced_name=item["name"],
            target_rate=required_rate,
            machine_count=machines_needed,
            clock_speed=clock_speed,
            power_per_machine=best_recipe["powerConsumption"],
            tier=best_recipe["unlockTier"],
            is_alternate=best_recipe["alternateRecipe"]
        )
        
        # Process inputs recursively
        for input_data in best_recipe["inputs"]:
            input_item_id = input_data["item"]
            input_amount = input_data["amount"]
            # database stores input amounts as per-minute rates, no need for crafting_speed
            input_rate_per_machine = input_amount
            total_input_rate = input_rate_per_machine * machines_needed * (clock_speed / 100.0)
            
            # Add to node inputs
            input_item = self.all_items.get(input_item_id)
            node.inputs.append(ItemFlow(
                item_id=input_item_id,
                item_name=input_item["name"] if input_item else input_item_id,
                rate=total_input_rate
            ))
            
            # Recursively build chain for input
            success = self._build_chain(
                item_id=input_item_id,
                required_rate=total_input_rate,
                allow_locked=allow_locked,
                result=result
            )
            
            if not success and not allow_locked:
                self.processing_stack.remove(item_id)
                return False
        
        # Add outputs to node
        for output_data in best_recipe["outputs"]:
            output_item_id = output_data["item"]
            output_amount = output_data["amount"]
            # outputs are already given as per-minute rates in this dataset
            output_rate_per_machine = output_amount
            total_output_rate = output_rate_per_machine * machines_needed * (clock_speed / 100.0)
            
            output_item = self.all_items.get(output_item_id)
            node.outputs.append(ItemFlow(
                item_id=output_item_id,
                item_name=output_item["name"] if output_item else output_item_id,
                rate=total_output_rate
            ))
        
        # Add node
        self.nodes.append(node)
        
        # Track production
        if item_id not in self.item_production:
            self.item_production[item_id] = []
        self.item_production[item_id].append(node_id)
        
        # finished processing this item for this branch
        self.processing_stack.remove(item_id)
        
        return True
    
    def _merge_nodes(self):
        """Combine multiple machine nodes producing the same item into one.

        The user requested that nodes be merged by item regardless of recipe
        or clock speed.  This method aggregates machine counts, target rates,
        power, and flows.  If two nodes use different recipes the merged node
        is marked as "multiple" so that consumers know the detail has been
        lost.
        """
        merged: Dict[str, MachineNode] = {}
        for node in self.nodes:
            key = node.item_produced
            if key not in merged:
                # copy the node to avoid mutating the original
                from copy import deepcopy
                merged[key] = deepcopy(node)
            else:
                m = merged[key]
                prev_rate = m.target_rate
                # combine basic quantities
                m.machine_count += node.machine_count
                m.target_rate += node.target_rate
                # weighted average clock speed by rate
                if m.target_rate > 0:
                    m.clock_speed = (
                        m.clock_speed * prev_rate
                        + node.clock_speed * node.target_rate
                    ) / m.target_rate
                m.total_power += node.total_power
                # merge inputs
                inputs_map = {inp.item_id: inp for inp in m.inputs}
                for inp in node.inputs:
                    if inp.item_id in inputs_map:
                        inputs_map[inp.item_id].rate += inp.rate
                    else:
                        inputs_map[inp.item_id] = inp
                m.inputs = list(inputs_map.values())
                # merge outputs
                outputs_map = {out.item_id: out for out in m.outputs}
                for out in node.outputs:
                    if out.item_id in outputs_map:
                        outputs_map[out.item_id].rate += out.rate
                    else:
                        outputs_map[out.item_id] = out
                m.outputs = list(outputs_map.values())
                # if recipe differs, mark as multiple
                if node.recipe_id != m.recipe_id:
                    m.recipe_id = "multiple"
                    m.recipe_name = "Multiple"
                    m.machine_type = "mixed"
        # rewrite node list and item_production
        self.nodes = list(merged.values())
        self.item_production = {item: [node.node_id] for item, node in merged.items()}

    def _build_connections(self):
        """Build connections between nodes after chain is complete.
        Distribute input rates across multiple producers proportionally
        according to each producer's output rate for that item."""
        connection_id = 0

        # build a mapping of producers for each item with their output rates
        producers: Dict[str, List[Tuple[str, float]]] = {}
        for node in self.nodes:
            for out in node.outputs:
                producers.setdefault(out.item_id, []).append((node.node_id, out.rate))

        # iterate through each consumer node and allocate its inputs
        for node in self.nodes:
            for input_flow in node.inputs:
                prod_list = producers.get(input_flow.item_id, [])
                if not prod_list:
                    continue

                total_prod = sum(rate for _, rate in prod_list)
                # avoid division by zero
                if total_prod <= 0:
                    continue

                # allocate input rate proportionally
                for prod_node_id, prod_rate in prod_list:
                    allocated = input_flow.rate * (prod_rate / total_prod)
                    connection = Connection(
                        connection_id=f"conn_{connection_id}",
                        from_node_id=prod_node_id,
                        to_node_id=node.node_id,
                        item_id=input_flow.item_id,
                        item_name=input_flow.item_name,
                        rate=allocated,
                        is_recycling_loop=False  # TODO: detect actual loops
                    )
                    self.connections.append(connection)
                    connection_id += 1


def calculate_production_chain(
    target_item_id: str,
    target_rate: float,
    unlocked_recipes: Set[str],
    objective: OptimizationObjective = OptimizationObjective.BALANCED,
    allow_locked_preview: bool = False
) -> ProductionChainResult:
    """
    Main entry point for calculating production chain.
    
    Args:
        target_item_id: Target item to produce
        target_rate: Desired production rate (items/min)
        unlocked_recipes: Set of unlocked recipe IDs
        objective: Optimization objective
        allow_locked_preview: If True, show what would be possible with all recipes
    
    Returns:
        ProductionChainResult
    """
    solver = ProductionChainSolver(
        unlocked_recipes=unlocked_recipes,
        objective=objective
    )
    
    result = solver.solve(
        target_item_id=target_item_id,
        target_rate=target_rate,
        allow_locked_preview=allow_locked_preview
    )
    
    # optionally merge similar nodes to reduce clutter
    solver._merge_nodes()
    # make sure the result object also reflects the merged list
    result.nodes = solver.nodes

    # Build connections for visualization using the merged nodes
    solver.connections = []
    solver._build_connections()
    result.connections = solver.connections
    
    return result
