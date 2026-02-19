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
    crafting_speed = recipe["craftingSpeed"]
    power = recipe["powerConsumption"]
    
    # Calculate output rate per machine
    output_amount = sum(output["amount"] for output in recipe["outputs"])
    output_rate_per_machine = (output_amount / crafting_speed) * 60  # items per minute
    
    # Calculate machines needed
    machines_needed = target_rate / output_rate_per_machine if output_rate_per_machine > 0 else float('inf')
    
    # Calculate total power needed
    total_power = machines_needed * power
    
    # Calculate input complexity (number of input types)
    input_complexity = len(recipe["inputs"])
    
    # Calculate total input resources needed
    total_input_rate = sum(
        (inp["amount"] / crafting_speed) * 60 * machines_needed
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
    crafting_speed = recipe["craftingSpeed"]
    power = recipe["powerConsumption"]
    
    # Calculate output per minute
    output_amount = sum(output["amount"] for output in recipe["outputs"])
    output_rate = (output_amount / crafting_speed) * 60
    
    # Calculate efficiency: output per power per minute
    if power > 0:
        efficiency = output_rate / power
    else:
        efficiency = output_rate
    
    return efficiency
