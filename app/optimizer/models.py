"""
Data models for the production chain optimizer.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum


class OptimizationObjective(Enum):
    """Optimization priorities."""
    MINIMIZE_MACHINES = "minimize_machines"
    MINIMIZE_POWER = "minimize_power"
    MINIMIZE_WASTE = "minimize_waste"
    BALANCED = "balanced"


class CalculationStatus(Enum):
    """Status of the calculation."""
    SUCCESS = "success"
    INSUFFICIENT_RECIPES = "insufficient_recipes"
    IMPOSSIBLE_RATE = "impossible_rate"
    RESOURCE_WARNING = "resource_warning"


@dataclass
class ItemFlow:
    """Represents a flow of items."""
    item_id: str
    item_name: str
    rate: float  # items per minute
    

@dataclass
class MachineNode:
    """Represents a production machine in the production chain."""
    node_id: str
    recipe_id: str
    recipe_name: str
    machine_type: str
    item_produced: str
    item_produced_name: str
    
    # Production details
    target_rate: float  # items/min output
    machine_count: float  # can be fractional
    clock_speed: float = 100.0  # percentage (100 = normal speed)
    
    # Resource consumption
    power_per_machine: float = 0.0
    total_power: float = 0.0
    
    # Inputs and outputs
    inputs: List[ItemFlow] = field(default_factory=list)
    outputs: List[ItemFlow] = field(default_factory=list)
    
    # Metadata
    tier: int = 0
    is_alternate: bool = False
    
    def __post_init__(self):
        """Calculate total power."""
        self.total_power = self.power_per_machine * self.machine_count * (self.clock_speed / 100.0)


@dataclass
class Connection:
    """Represents a connection between machines."""
    connection_id: str
    from_node_id: str
    to_node_id: str
    item_id: str
    item_name: str
    rate: float  # items per minute
    is_recycling_loop: bool = False


@dataclass
class RawResourceRequirement:
    """Represents raw resource requirements."""
    item_id: str
    item_name: str
    rate: float  # items per minute
    

@dataclass
class ProductionChainResult:
    """Result of a production chain calculation."""
    status: CalculationStatus
    
    # Target information
    target_item_id: str
    target_item_name: str
    target_rate: float
    
    # Production details
    nodes: List[MachineNode] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)
    raw_resources: List[RawResourceRequirement] = field(default_factory=list)
    
    # Summary statistics
    total_machines: int = 0
    total_power: float = 0.0
    total_raw_resources: int = 0
    
    # Messages and warnings
    messages: List[str] = field(default_factory=list)
    missing_recipes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Metadata
    unlocked_recipes: Set[str] = field(default_factory=set)
    optimization_objective: OptimizationObjective = OptimizationObjective.BALANCED
    timestamp: Optional[str] = None
    
    def add_message(self, message: str):
        """Add a message."""
        self.messages.append(message)
    
    def add_warning(self, warning: str):
        """Add a warning."""
        self.warnings.append(warning)
    
    def add_missing_recipe(self, recipe_name: str):
        """Add a missing recipe."""
        if recipe_name not in self.missing_recipes:
            self.missing_recipes.append(recipe_name)
    
    def calculate_summary(self):
        """Calculate summary statistics."""
        self.total_machines = sum(int(node.machine_count + 0.99) for node in self.nodes)  # ceiling
        self.total_power = sum(node.total_power for node in self.nodes)
        self.total_raw_resources = len(self.raw_resources)


@dataclass
class RecipeChoice:
    """Represents a choice between multiple recipes for an item."""
    item_id: str
    item_name: str
    recipes: List[Dict] = field(default_factory=list)
    selected_recipe_id: Optional[str] = None
    score: float = 0.0


@dataclass
class ProductionStage:
    """Represents a stage in the production chain."""
    stage_number: int
    stage_name: str
    nodes: List[MachineNode] = field(default_factory=list)
    
    def get_total_machines(self):
        """Get total machines in this stage."""
        return sum(int(node.machine_count + 0.99) for node in self.nodes)
    
    def get_total_power(self):
        """Get total power in this stage."""
        return sum(node.total_power for node in self.nodes)
