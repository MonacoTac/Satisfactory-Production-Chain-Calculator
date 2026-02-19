"""
Import/Export functionality for saving and loading calculations.
"""

import json
from typing import Dict, Set, Optional
from datetime import datetime
from dataclasses import asdict

from optimizer.models import (
    ProductionChainResult, MachineNode, Connection, 
    RawResourceRequirement, OptimizationObjective, CalculationStatus
)


def export_result_to_json(result: ProductionChainResult) -> str:
    """
    Export production chain result to JSON string.
    
    Args:
        result: Production chain result
    
    Returns:
        JSON string
    """
    data = {
        "version": "1.0",
        "timestamp": result.timestamp or datetime.now().isoformat(),
        "target": {
            "item_id": result.target_item_id,
            "item_name": result.target_item_name,
            "rate": result.target_rate
        },
        "status": result.status.value,
        "optimization_objective": result.optimization_objective.value,
        "unlocked_recipes": list(result.unlocked_recipes),
        "nodes": [
            {
                "node_id": node.node_id,
                "recipe_id": node.recipe_id,
                "recipe_name": node.recipe_name,
                "machine_type": node.machine_type,
                "item_produced": node.item_produced,
                "item_produced_name": node.item_produced_name,
                "target_rate": node.target_rate,
                "machine_count": node.machine_count,
                "clock_speed": node.clock_speed,
                "power_per_machine": node.power_per_machine,
                "total_power": node.total_power,
                "tier": node.tier,
                "is_alternate": node.is_alternate,
                "inputs": [
                    {
                        "item_id": inp.item_id,
                        "item_name": inp.item_name,
                        "rate": inp.rate
                    }
                    for inp in node.inputs
                ],
                "outputs": [
                    {
                        "item_id": out.item_id,
                        "item_name": out.item_name,
                        "rate": out.rate
                    }
                    for out in node.outputs
                ]
            }
            for node in result.nodes
        ],
        "connections": [
            {
                "connection_id": conn.connection_id,
                "from_node_id": conn.from_node_id,
                "to_node_id": conn.to_node_id,
                "item_id": conn.item_id,
                "item_name": conn.item_name,
                "rate": conn.rate,
                "is_recycling_loop": conn.is_recycling_loop
            }
            for conn in result.connections
        ],
        "raw_resources": [
            {
                "item_id": rr.item_id,
                "item_name": rr.item_name,
                "rate": rr.rate
            }
            for rr in result.raw_resources
        ],
        "summary": {
            "total_machines": result.total_machines,
            "total_power": result.total_power,
            "total_raw_resources": result.total_raw_resources
        },
        "messages": result.messages,
        "warnings": result.warnings,
        "missing_recipes": result.missing_recipes
    }
    
    return json.dumps(data, indent=2)


def import_result_from_json(json_string: str) -> Optional[ProductionChainResult]:
    """
    Import production chain result from JSON string.
    
    Args:
        json_string: JSON string
    
    Returns:
        ProductionChainResult or None if invalid
    """
    try:
        data = json.loads(json_string)
        
        # Parse status and objective
        status = CalculationStatus(data["status"])
        objective = OptimizationObjective(data["optimization_objective"])
        
        # Create result object
        result = ProductionChainResult(
            status=status,
            target_item_id=data["target"]["item_id"],
            target_item_name=data["target"]["item_name"],
            target_rate=data["target"]["rate"],
            unlocked_recipes=set(data["unlocked_recipes"]),
            optimization_objective=objective,
            timestamp=data.get("timestamp")
        )
        
        # Import nodes
        from optimizer.models import ItemFlow
        for node_data in data["nodes"]:
            node = MachineNode(
                node_id=node_data["node_id"],
                recipe_id=node_data["recipe_id"],
                recipe_name=node_data["recipe_name"],
                machine_type=node_data["machine_type"],
                item_produced=node_data["item_produced"],
                item_produced_name=node_data["item_produced_name"],
                target_rate=node_data["target_rate"],
                machine_count=node_data["machine_count"],
                clock_speed=node_data.get("clock_speed", 100.0),
                power_per_machine=node_data["power_per_machine"],
                total_power=node_data["total_power"],
                tier=node_data.get("tier", 0),
                is_alternate=node_data.get("is_alternate", False),
                inputs=[
                    ItemFlow(
                        item_id=inp["item_id"],
                        item_name=inp["item_name"],
                        rate=inp["rate"]
                    )
                    for inp in node_data["inputs"]
                ],
                outputs=[
                    ItemFlow(
                        item_id=out["item_id"],
                        item_name=out["item_name"],
                        rate=out["rate"]
                    )
                    for out in node_data["outputs"]
                ]
            )
            result.nodes.append(node)
        
        # Import connections
        for conn_data in data["connections"]:
            connection = Connection(
                connection_id=conn_data["connection_id"],
                from_node_id=conn_data["from_node_id"],
                to_node_id=conn_data["to_node_id"],
                item_id=conn_data["item_id"],
                item_name=conn_data["item_name"],
                rate=conn_data["rate"],
                is_recycling_loop=conn_data.get("is_recycling_loop", False)
            )
            result.connections.append(connection)
        
        # Import raw resources
        for rr_data in data["raw_resources"]:
            rr = RawResourceRequirement(
                item_id=rr_data["item_id"],
                item_name=rr_data["item_name"],
                rate=rr_data["rate"]
            )
            result.raw_resources.append(rr)
        
        # Import messages
        result.messages = data.get("messages", [])
        result.warnings = data.get("warnings", [])
        result.missing_recipes = data.get("missing_recipes", [])
        
        # Import summary
        summary = data.get("summary", {})
        result.total_machines = summary.get("total_machines", 0)
        result.total_power = summary.get("total_power", 0.0)
        result.total_raw_resources = summary.get("total_raw_resources", 0)
        
        return result
    
    except Exception as e:
        print(f"Error importing JSON: {e}")
        return None


def export_unlocked_recipes(unlocked_recipes: Set[str]) -> str:
    """
    Export unlocked recipes to JSON string.
    
    Args:
        unlocked_recipes: Set of unlocked recipe IDs
    
    Returns:
        JSON string
    """
    data = {
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "unlocked_recipes": list(unlocked_recipes)
    }
    return json.dumps(data, indent=2)


def import_unlocked_recipes(json_string: str) -> Optional[Set[str]]:
    """
    Import unlocked recipes from JSON string.
    
    Args:
        json_string: JSON string
    
    Returns:
        Set of recipe IDs or None if invalid
    """
    try:
        data = json.loads(json_string)
        return set(data["unlocked_recipes"])
    except Exception as e:
        print(f"Error importing unlocked recipes: {e}")
        return None


def create_download_filename(result: ProductionChainResult, extension: str = "json") -> str:
    """
    Create a filename for downloading results.
    
    Args:
        result: Production chain result
        extension: File extension
    
    Returns:
        Filename string
    """
    # Sanitize item name for filename
    item_name = result.target_item_name.replace(" ", "_")
    item_name = "".join(c for c in item_name if c.isalnum() or c == "_")
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"satisfactory_{item_name}_{timestamp}.{extension}"


def export_to_file(result: ProductionChainResult, filepath: str) -> bool:
    """
    Export result to a file.
    
    Args:
        result: Production chain result
        filepath: Path to save file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        json_string = export_result_to_json(result)
        with open(filepath, 'w') as f:
            f.write(json_string)
        return True
    except Exception as e:
        print(f"Error exporting to file: {e}")
        return False


def import_from_file(filepath: str) -> Optional[ProductionChainResult]:
    """
    Import result from a file.
    
    Args:
        filepath: Path to file
    
    Returns:
        ProductionChainResult or None if invalid
    """
    try:
        with open(filepath, 'r') as f:
            json_string = f.read()
        return import_result_from_json(json_string)
    except Exception as e:
        print(f"Error importing from file: {e}")
        return None
