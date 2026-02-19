"""
Input validation and error message helpers.
"""

from typing import Optional, Tuple
from data import satisfactory_db


def validate_target_item(item_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate target item ID.
    
    Args:
        item_id: Item ID to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not item_id:
        return False, "Please select a target item."
    
    item = satisfactory_db.get_item_by_id(item_id)
    if not item:
        return False, f"Item '{item_id}' not found in database."
    
    return True, None


def validate_target_rate(rate: float) -> Tuple[bool, Optional[str]]:
    """
    Validate target production rate.
    
    Args:
        rate: Production rate (items/min)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if rate <= 0:
        return False, "Production rate must be greater than 0."
    
    if rate > 100000:
        return False, "Production rate is unreasonably high (max: 100,000/min)."
    
    return True, None


def validate_unlocked_recipes(unlocked_recipes: set) -> Tuple[bool, Optional[str]]:
    """
    Validate unlocked recipes set.
    
    Args:
        unlocked_recipes: Set of recipe IDs
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not unlocked_recipes:
        return False, "No recipes unlocked. Please unlock at least one recipe."
    
    all_recipes = satisfactory_db.get_all_recipes()
    invalid_recipes = [rid for rid in unlocked_recipes if rid not in all_recipes]
    
    if invalid_recipes:
        return False, f"Invalid recipe IDs: {', '.join(invalid_recipes)}"
    
    return True, None


def get_missing_recipe_message(item_name: str, available_recipes: list) -> str:
    """
    Generate helpful error message for missing recipes.
    
    Args:
        item_name: Name of the item that can't be produced
        available_recipes: List of recipe dictionaries that could produce it
    
    Returns:
        Error message string
    """
    if not available_recipes:
        return f"No recipes available to produce {item_name}."
    
    recipe_names = [r["name"] for r in available_recipes]
    
    if len(recipe_names) == 1:
        return f"To produce {item_name}, unlock the recipe: {recipe_names[0]}"
    else:
        recipes_str = ", ".join(recipe_names)
        return f"To produce {item_name}, unlock one of these recipes: {recipes_str}"


def format_rate(rate: float) -> str:
    """
    Format production rate for display.
    
    Args:
        rate: Rate in items/min
    
    Returns:
        Formatted string
    """
    if rate < 1:
        return f"{rate:.3f}/min"
    elif rate < 10:
        return f"{rate:.2f}/min"
    elif rate < 100:
        return f"{rate:.1f}/min"
    else:
        return f"{rate:.0f}/min"


def format_machine_count(count: float) -> str:
    """
    Format machine count for display.
    
    Args:
        count: Machine count (can be fractional)
    
    Returns:
        Formatted string
    """
    if count < 0.01:
        return "< 0.01"
    elif count < 1:
        return f"{count:.2f}"
    elif count % 1 < 0.01:  # Nearly whole number
        return f"{int(count + 0.5)}"
    else:
        return f"{count:.2f}"


def format_power(power: float) -> str:
    """
    Format power consumption for display.
    
    Args:
        power: Power in MW
    
    Returns:
        Formatted string
    """
    if power < 1:
        return f"{power*1000:.0f} kW"
    elif power < 10:
        return f"{power:.2f} MW"
    elif power < 100:
        return f"{power:.1f} MW"
    else:
        return f"{power:.0f} MW"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename


def validate_calculation_inputs(
    item_id: str,
    rate: float,
    unlocked_recipes: set
) -> Tuple[bool, Optional[str]]:
    """
    Validate all calculation inputs together.
    
    Args:
        item_id: Target item ID
        rate: Production rate
        unlocked_recipes: Set of unlocked recipe IDs
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate item
    is_valid, error = validate_target_item(item_id)
    if not is_valid:
        return False, error
    
    # Validate rate
    is_valid, error = validate_target_rate(rate)
    if not is_valid:
        return False, error
    
    # Validate recipes
    is_valid, error = validate_unlocked_recipes(unlocked_recipes)
    if not is_valid:
        return False, error
    
    return True, None


def get_tier_name(tier: int) -> str:
    """
    Get friendly name for unlock tier.
    
    Args:
        tier: Tier number
    
    Returns:
        Tier name string
    """
    tier_names = {
        0: "Tier 0 - HUB Upgrade 1",
        1: "Tier 1 - Field Research",
        2: "Tier 2 - Part Assembly",
        3: "Tier 3 - Basic Steel Production",
        4: "Tier 4 - Advanced Steel Production",
        5: "Tier 5 - Oil Processing",
        6: "Tier 6 - Industrial Manufacturing",
        7: "Tier 7 - Bauxite Refinement",
        8: "Tier 8 - Nuclear Power",
    }
    return tier_names.get(tier, f"Tier {tier}")


def get_machine_type_icon(machine_type: str) -> str:
    """
    Get emoji icon for machine type.
    
    Args:
        machine_type: Machine type name
    
    Returns:
        Icon string
    """
    icons = {
        "Smelter": "🔥",
        "Constructor": "🔨",
        "Assembler": "⚙️",
        "Manufacturer": "🏭",
        "Foundry": "🔥",
        "Refinery": "🛢️",
    }
    return icons.get(machine_type, "⚡")


def format_summary_stats(result) -> str:
    """
    Format summary statistics as a readable string.
    
    Args:
        result: ProductionChainResult object
    
    Returns:
        Formatted summary string
    """
    lines = []
    lines.append(f"**Target:** {result.target_rate:.1f} {result.target_item_name}/min")
    lines.append(f"**Total Machines:** {result.total_machines}")
    lines.append(f"**Total Power:** {format_power(result.total_power)}")
    lines.append(f"**Raw Resources:** {result.total_raw_resources} types")
    
    if result.raw_resources:
        lines.append("\n**Raw Resource Requirements:**")
        for rr in result.raw_resources:
            lines.append(f"  • {rr.item_name}: {format_rate(rr.rate)}")
    
    return "\n".join(lines)
