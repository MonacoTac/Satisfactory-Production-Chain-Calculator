"""
Optimization objective scoring functions.
"""

from typing import Dict, List
from optimizer.models import OptimizationObjective


def score_recipe(
    recipe: Dict,
    objective: OptimizationObjective,
    target_rate: float
) -> float:
    """
    Score a recipe based on the optimization objective.
    Higher score = better choice.
    
    Args:
        recipe: Recipe dictionary from database
        objective: Optimization objective
        target_rate: Target production rate (items/min)
    
    Returns:
        Score (higher is better)
    """
    # Base calculations
    power = recipe["powerConsumption"]
    
    # In this dataset the recipe "amount" is already a per-minute rate.
    # We ignore craftingSpeed and use the raw amount directly.
    output_amount = sum(output["amount"] for output in recipe["outputs"])
    output_rate_per_machine = output_amount
    
    # Calculate machines needed as integer and approximate utilization
    import math
    machines_needed = math.ceil(target_rate / output_rate_per_machine) if output_rate_per_machine > 0 else float('inf')
    # compute clock speed fraction (0-1)
    clock_util = (target_rate / (machines_needed * output_rate_per_machine)) if machines_needed > 0 else 1.0
    clock_util = min(clock_util, 1.0)
    # Calculate total power needed (scales with clock speed)
    total_power = machines_needed * power * clock_util
    
    # Calculate input complexity (number of input types)
    input_complexity = len(recipe["inputs"])
    
    # Calculate total input resources needed (scaled by clock utilization)
    # inputs are stored as per-minute amounts, so we can use them directly
    total_input_rate = sum(
        inp["amount"] * machines_needed * clock_util
        for inp in recipe["inputs"]
    )
    
    # Scoring based on objective
    if objective == OptimizationObjective.MINIMIZE_MACHINES:
        # Prefer recipes that need fewer machines for the target rate
        # Also consider input complexity as a tiebreaker
        score = 1000.0 / (machines_needed + 1) - (input_complexity * 10)
        return score
    
    elif objective == OptimizationObjective.MINIMIZE_POWER:
        # Prefer recipes with lower total power consumption
        score = 1000.0 / (total_power + 1)
        return score
    
    elif objective == OptimizationObjective.MINIMIZE_WASTE:
        # Prefer recipes with better input/output ratios
        # Lower waste = higher efficiency
        efficiency = output_rate_per_machine / (total_input_rate / machines_needed + 1)
        score = efficiency * 100
        return score
    
    elif objective == OptimizationObjective.BALANCED:
        # Balanced approach: consider machines, power, and complexity
        machine_score = 100.0 / (machines_needed + 1)
        power_score = 100.0 / (total_power + 1)
        complexity_penalty = input_complexity * 5
        score = machine_score + power_score - complexity_penalty
        return score
    
    else:
        # Default: balanced
        return 50.0


def compare_recipes(
    recipe1: Dict,
    recipe2: Dict,
    objective: OptimizationObjective,
    target_rate: float
) -> int:
    """
    Compare two recipes based on optimization objective.
    
    Args:
        recipe1: First recipe
        recipe2: Second recipe
        objective: Optimization objective
        target_rate: Target production rate
    
    Returns:
        -1 if recipe1 is better, 1 if recipe2 is better, 0 if equal
    """
    score1 = score_recipe(recipe1, objective, target_rate)
    score2 = score_recipe(recipe2, objective, target_rate)
    
    if score1 > score2:
        return -1
    elif score1 < score2:
        return 1
    else:
        return 0


def select_best_recipe(
    recipes: List[Dict],
    objective: OptimizationObjective,
    target_rate: float,
    unlocked_only: bool = True,
    unlocked_recipes: set = None
) -> Dict:
    """
    Select the best recipe from a list based on objective.
    
    Args:
        recipes: List of recipes to choose from
        objective: Optimization objective
        target_rate: Target production rate
        unlocked_only: If True, only consider unlocked recipes
        unlocked_recipes: Set of unlocked recipe IDs
    
    Returns:
        Best recipe (or first recipe if no unlocked recipes found)
    """
    if not recipes:
        return None
    
    # Filter for unlocked recipes if needed
    if unlocked_only and unlocked_recipes:
        available_recipes = [r for r in recipes if r["id"] in unlocked_recipes]
        if not available_recipes:
            # No unlocked recipes available, return None
            return None
    else:
        available_recipes = recipes
    
    if not available_recipes:
        return None
    
    # Score all recipes
    scored_recipes = [
        (recipe, score_recipe(recipe, objective, target_rate))
        for recipe in available_recipes
    ]
    
    # Sort by score (descending)
    scored_recipes.sort(key=lambda x: x[1], reverse=True)
    
    # Return best recipe
    return scored_recipes[0][0]


def get_recipe_variants(
    recipes: List[Dict],
    objective: OptimizationObjective,
    target_rate: float,
    unlocked_recipes: set = None,
    max_variants: int = 3
) -> List[tuple]:
    """
    Get top N recipe variants with scores.
    
    Args:
        recipes: List of recipes
        objective: Optimization objective
        target_rate: Target production rate
        unlocked_recipes: Set of unlocked recipe IDs
        max_variants: Maximum number of variants to return
    
    Returns:
        List of (recipe, score) tuples
    """
    if not recipes:
        return []
    
    # Filter for unlocked recipes
    if unlocked_recipes:
        available_recipes = [r for r in recipes if r["id"] in unlocked_recipes]
    else:
        available_recipes = recipes
    
    if not available_recipes:
        return []
    
    # Score all recipes
    scored_recipes = [
        (recipe, score_recipe(recipe, objective, target_rate))
        for recipe in available_recipes
    ]
    
    # Sort by score (descending)
    scored_recipes.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N
    return scored_recipes[:max_variants]


def calculate_recipe_efficiency(recipe: Dict) -> float:
    """
    Calculate overall efficiency of a recipe.
    
    Args:
        recipe: Recipe dictionary
    
    Returns:
        Efficiency score (higher is better)
    """
    power = recipe["powerConsumption"]
    
    # Calculate output per minute
    output_amount = sum(output["amount"] for output in recipe["outputs"])
    # output_amount already reflects per-minute production
    output_rate = output_amount
    
    # Calculate efficiency: output per power per minute
    if power > 0:
        efficiency = output_rate / power
    else:
        efficiency = output_rate
    
    return efficiency
