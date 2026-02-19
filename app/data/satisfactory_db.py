"""
Satisfactory game data: Items and Recipes
Single source of truth for all items and recipes in the production calculator.
"""

# Items database
ITEMS = {
    # Raw Resources
    "iron_ore": {
        "id": "iron_ore",
        "name": "Iron Ore",
        "category": "Raw Resource",
        "stackSize": 100,
        "isRawResource": True
    },
    "copper_ore": {
        "id": "copper_ore",
        "name": "Copper Ore",
        "category": "Raw Resource",
        "stackSize": 100,
        "isRawResource": True
    },
    "limestone": {
        "id": "limestone",
        "name": "Limestone",
        "category": "Raw Resource",
        "stackSize": 100,
        "isRawResource": True
    },
    "coal": {
        "id": "coal",
        "name": "Coal",
        "category": "Raw Resource",
        "stackSize": 100,
        "isRawResource": True
    },
    "caterium_ore": {
        "id": "caterium_ore",
        "name": "Caterium Ore",
        "category": "Raw Resource",
        "stackSize": 100,
        "isRawResource": True
    },
    "raw_quartz": {
        "id": "raw_quartz",
        "name": "Raw Quartz",
        "category": "Raw Resource",
        "stackSize": 100,
        "isRawResource": True
    },
    "crude_oil": {
        "id": "crude_oil",
        "name": "Crude Oil",
        "category": "Raw Resource",
        "stackSize": 1,
        "isRawResource": True
    },
    "water": {
        "id": "water",
        "name": "Water",
        "category": "Raw Resource",
        "stackSize": 1,
        "isRawResource": True
    },
    
    # Basic Ingots
    "iron_ingot": {
        "id": "iron_ingot",
        "name": "Iron Ingot",
        "category": "Ingot",
        "stackSize": 100,
        "isRawResource": False
    },
    "copper_ingot": {
        "id": "copper_ingot",
        "name": "Copper Ingot",
        "category": "Ingot",
        "stackSize": 100,
        "isRawResource": False
    },
    "steel_ingot": {
        "id": "steel_ingot",
        "name": "Steel Ingot",
        "category": "Ingot",
        "stackSize": 100,
        "isRawResource": False
    },
    "caterium_ingot": {
        "id": "caterium_ingot",
        "name": "Caterium Ingot",
        "category": "Ingot",
        "stackSize": 100,
        "isRawResource": False
    },
    
    # Basic Materials
    "concrete": {
        "id": "concrete",
        "name": "Concrete",
        "category": "Material",
        "stackSize": 100,
        "isRawResource": False
    },
    "wire": {
        "id": "wire",
        "name": "Wire",
        "category": "Material",
        "stackSize": 500,
        "isRawResource": False
    },
    "cable": {
        "id": "cable",
        "name": "Cable",
        "category": "Material",
        "stackSize": 200,
        "isRawResource": False
    },
    "iron_rod": {
        "id": "iron_rod",
        "name": "Iron Rod",
        "category": "Material",
        "stackSize": 200,
        "isRawResource": False
    },
    "iron_plate": {
        "id": "iron_plate",
        "name": "Iron Plate",
        "category": "Material",
        "stackSize": 200,
        "isRawResource": False
    },
    "reinforced_iron_plate": {
        "id": "reinforced_iron_plate",
        "name": "Reinforced Iron Plate",
        "category": "Material",
        "stackSize": 100,
        "isRawResource": False
    },
    "screw": {
        "id": "screw",
        "name": "Screw",
        "category": "Material",
        "stackSize": 500,
        "isRawResource": False
    },
    "steel_beam": {
        "id": "steel_beam",
        "name": "Steel Beam",
        "category": "Material",
        "stackSize": 100,
        "isRawResource": False
    },
    "steel_pipe": {
        "id": "steel_pipe",
        "name": "Steel Pipe",
        "category": "Material",
        "stackSize": 100,
        "isRawResource": False
    },
    "encased_industrial_beam": {
        "id": "encased_industrial_beam",
        "name": "Encased Industrial Beam",
        "category": "Material",
        "stackSize": 100,
        "isRawResource": False
    },
    "quickwire": {
        "id": "quickwire",
        "name": "Quickwire",
        "category": "Material",
        "stackSize": 500,
        "isRawResource": False
    },
    "quartz_crystal": {
        "id": "quartz_crystal",
        "name": "Quartz Crystal",
        "category": "Material",
        "stackSize": 100,
        "isRawResource": False
    },
    
    # Components
    "rotor": {
        "id": "rotor",
        "name": "Rotor",
        "category": "Component",
        "stackSize": 100,
        "isRawResource": False
    },
    "modular_frame": {
        "id": "modular_frame",
        "name": "Modular Frame",
        "category": "Component",
        "stackSize": 50,
        "isRawResource": False
    },
    "smart_plating": {
        "id": "smart_plating",
        "name": "Smart Plating",
        "category": "Component",
        "stackSize": 50,
        "isRawResource": False
    },
    "stator": {
        "id": "stator",
        "name": "Stator",
        "category": "Component",
        "stackSize": 100,
        "isRawResource": False
    },
    "motor": {
        "id": "motor",
        "name": "Motor",
        "category": "Component",
        "stackSize": 50,
        "isRawResource": False
    },
    "heavy_modular_frame": {
        "id": "heavy_modular_frame",
        "name": "Heavy Modular Frame",
        "category": "Component",
        "stackSize": 50,
        "isRawResource": False
    },
    "ai_limiter": {
        "id": "ai_limiter",
        "name": "AI Limiter",
        "category": "Component",
        "stackSize": 100,
        "isRawResource": False
    },
    "computer": {
        "id": "computer",
        "name": "Computer",
        "category": "Component",
        "stackSize": 50,
        "isRawResource": False
    },
    "circuit_board": {
        "id": "circuit_board",
        "name": "Circuit Board",
        "category": "Component",
        "stackSize": 200,
        "isRawResource": False
    },
    
    # Oil Products
    "plastic": {
        "id": "plastic",
        "name": "Plastic",
        "category": "Oil Product",
        "stackSize": 100,
        "isRawResource": False
    },
    "rubber": {
        "id": "rubber",
        "name": "Rubber",
        "category": "Oil Product",
        "stackSize": 100,
        "isRawResource": False
    },
}

# Recipes database
RECIPES = {
    # Smelter Recipes
    "iron_ingot": {
        "id": "iron_ingot",
        "name": "Iron Ingot",
        "category": "Smelting",
        "unlockTier": 0,
        "machineType": "Smelter",
        "powerConsumption": 4,
        "craftingSpeed": 2.0,
        "alternateRecipe": False,
        "inputs": [{"item": "iron_ore", "amount": 30}],
        "outputs": [{"item": "iron_ingot", "amount": 30}]
    },
    "copper_ingot": {
        "id": "copper_ingot",
        "name": "Copper Ingot",
        "category": "Smelting",
        "unlockTier": 0,
        "machineType": "Smelter",
        "powerConsumption": 4,
        "craftingSpeed": 2.0,
        "alternateRecipe": False,
        "inputs": [{"item": "copper_ore", "amount": 30}],
        "outputs": [{"item": "copper_ingot", "amount": 30}]
    },
    "steel_ingot": {
        "id": "steel_ingot",
        "name": "Steel Ingot",
        "category": "Smelting",
        "unlockTier": 3,
        "machineType": "Foundry",
        "powerConsumption": 16,
        "craftingSpeed": 4.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "iron_ore", "amount": 45},
            {"item": "coal", "amount": 45}
        ],
        "outputs": [{"item": "steel_ingot", "amount": 45}]
    },
    "caterium_ingot": {
        "id": "caterium_ingot",
        "name": "Caterium Ingot",
        "category": "Smelting",
        "unlockTier": 2,
        "machineType": "Smelter",
        "powerConsumption": 4,
        "craftingSpeed": 4.0,
        "alternateRecipe": False,
        "inputs": [{"item": "caterium_ore", "amount": 45}],
        "outputs": [{"item": "caterium_ingot", "amount": 15}]
    },
    
    # Constructor Recipes
    "concrete": {
        "id": "concrete",
        "name": "Concrete",
        "category": "Construction",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 4.0,
        "alternateRecipe": False,
        "inputs": [{"item": "limestone", "amount": 45}],
        "outputs": [{"item": "concrete", "amount": 15}]
    },
    "iron_rod": {
        "id": "iron_rod",
        "name": "Iron Rod",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 4.0,
        "alternateRecipe": False,
        "inputs": [{"item": "iron_ingot", "amount": 15}],
        "outputs": [{"item": "iron_rod", "amount": 15}]
    },
    "iron_plate": {
        "id": "iron_plate",
        "name": "Iron Plate",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 6.0,
        "alternateRecipe": False,
        "inputs": [{"item": "iron_ingot", "amount": 30}],
        "outputs": [{"item": "iron_plate", "amount": 20}]
    },
    "screw": {
        "id": "screw",
        "name": "Screw",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 2.0,
        "alternateRecipe": False,
        "inputs": [{"item": "iron_rod", "amount": 10}],
        "outputs": [{"item": "screw", "amount": 40}]
    },
    "wire": {
        "id": "wire",
        "name": "Wire",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 4.0,
        "alternateRecipe": False,
        "inputs": [{"item": "copper_ingot", "amount": 15}],
        "outputs": [{"item": "wire", "amount": 30}]
    },
    "cable": {
        "id": "cable",
        "name": "Cable",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 2.0,
        "alternateRecipe": False,
        "inputs": [{"item": "wire", "amount": 60}],
        "outputs": [{"item": "cable", "amount": 30}]
    },
    "steel_beam": {
        "id": "steel_beam",
        "name": "Steel Beam",
        "category": "Material",
        "unlockTier": 3,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 4.0,
        "alternateRecipe": False,
        "inputs": [{"item": "steel_ingot", "amount": 60}],
        "outputs": [{"item": "steel_beam", "amount": 15}]
    },
    "steel_pipe": {
        "id": "steel_pipe",
        "name": "Steel Pipe",
        "category": "Material",
        "unlockTier": 3,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 6.0,
        "alternateRecipe": False,
        "inputs": [{"item": "steel_ingot", "amount": 30}],
        "outputs": [{"item": "steel_pipe", "amount": 20}]
    },
    "quickwire": {
        "id": "quickwire",
        "name": "Quickwire",
        "category": "Material",
        "unlockTier": 2,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 5.0,
        "alternateRecipe": False,
        "inputs": [{"item": "caterium_ingot", "amount": 12}],
        "outputs": [{"item": "quickwire", "amount": 60}]
    },
    "quartz_crystal": {
        "id": "quartz_crystal",
        "name": "Quartz Crystal",
        "category": "Material",
        "unlockTier": 2,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 8.0,
        "alternateRecipe": False,
        "inputs": [{"item": "raw_quartz", "amount": 37.5}],
        "outputs": [{"item": "quartz_crystal", "amount": 22.5}]
    },
    
    # Assembler Recipes
    "reinforced_iron_plate": {
        "id": "reinforced_iron_plate",
        "name": "Reinforced Iron Plate",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 12.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "iron_plate", "amount": 30},
            {"item": "screw", "amount": 60}
        ],
        "outputs": [{"item": "reinforced_iron_plate", "amount": 5}]
    },
    "rotor": {
        "id": "rotor",
        "name": "Rotor",
        "category": "Component",
        "unlockTier": 1,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 15.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "iron_rod", "amount": 20},
            {"item": "screw", "amount": 100}
        ],
        "outputs": [{"item": "rotor", "amount": 4}]
    },
    "modular_frame": {
        "id": "modular_frame",
        "name": "Modular Frame",
        "category": "Component",
        "unlockTier": 2,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 60.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "reinforced_iron_plate", "amount": 3},
            {"item": "iron_rod", "amount": 12}
        ],
        "outputs": [{"item": "modular_frame", "amount": 2}]
    },
    "smart_plating": {
        "id": "smart_plating",
        "name": "Smart Plating",
        "category": "Component",
        "unlockTier": 1,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 30.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "reinforced_iron_plate", "amount": 1},
            {"item": "rotor", "amount": 1}
        ],
        "outputs": [{"item": "smart_plating", "amount": 1}]
    },
    "encased_industrial_beam": {
        "id": "encased_industrial_beam",
        "name": "Encased Industrial Beam",
        "category": "Material",
        "unlockTier": 4,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 10.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "steel_beam", "amount": 24},
            {"item": "concrete", "amount": 30}
        ],
        "outputs": [{"item": "encased_industrial_beam", "amount": 6}]
    },
    "stator": {
        "id": "stator",
        "name": "Stator",
        "category": "Component",
        "unlockTier": 4,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 12.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "steel_pipe", "amount": 15},
            {"item": "wire", "amount": 40}
        ],
        "outputs": [{"item": "stator", "amount": 5}]
    },
    "motor": {
        "id": "motor",
        "name": "Motor",
        "category": "Component",
        "unlockTier": 4,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 12.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "rotor", "amount": 10},
            {"item": "stator", "amount": 10}
        ],
        "outputs": [{"item": "motor", "amount": 5}]
    },
    "ai_limiter": {
        "id": "ai_limiter",
        "name": "AI Limiter",
        "category": "Component",
        "unlockTier": 5,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 12.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "copper_ingot", "amount": 25},
            {"item": "quickwire", "amount": 100}
        ],
        "outputs": [{"item": "ai_limiter", "amount": 5}]
    },
    "circuit_board": {
        "id": "circuit_board",
        "name": "Circuit Board",
        "category": "Component",
        "unlockTier": 5,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 8.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "copper_ingot", "amount": 15},
            {"item": "plastic", "amount": 30}
        ],
        "outputs": [{"item": "circuit_board", "amount": 7.5}]
    },
    
    # Manufacturer Recipes
    "heavy_modular_frame": {
        "id": "heavy_modular_frame",
        "name": "Heavy Modular Frame",
        "category": "Component",
        "unlockTier": 4,
        "machineType": "Manufacturer",
        "powerConsumption": 55,
        "craftingSpeed": 30.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "modular_frame", "amount": 10},
            {"item": "steel_pipe", "amount": 30},
            {"item": "encased_industrial_beam", "amount": 10},
            {"item": "screw", "amount": 200}
        ],
        "outputs": [{"item": "heavy_modular_frame", "amount": 2}]
    },
    "computer": {
        "id": "computer",
        "name": "Computer",
        "category": "Component",
        "unlockTier": 5,
        "machineType": "Manufacturer",
        "powerConsumption": 55,
        "craftingSpeed": 24.0,
        "alternateRecipe": False,
        "inputs": [
            {"item": "circuit_board", "amount": 25},
            {"item": "cable", "amount": 22.5},
            {"item": "plastic", "amount": 45},
            {"item": "screw", "amount": 130}
        ],
        "outputs": [{"item": "computer", "amount": 2.5}]
    },
    
    # Refinery Recipes
    "plastic": {
        "id": "plastic",
        "name": "Plastic",
        "category": "Oil Product",
        "unlockTier": 5,
        "machineType": "Refinery",
        "powerConsumption": 30,
        "craftingSpeed": 6.0,
        "alternateRecipe": False,
        "inputs": [{"item": "crude_oil", "amount": 30}],
        "outputs": [{"item": "plastic", "amount": 20}]
                  
    },
    "rubber": {
        "id": "rubber",
        "name": "Rubber",
        "category": "Oil Product",
        "unlockTier": 5,
        "machineType": "Refinery",
        "powerConsumption": 30,
        "craftingSpeed": 6.0,
        "alternateRecipe": False,
        "inputs": [{"item": "crude_oil", "amount": 30}],
        "outputs": [{"item": "rubber", "amount": 20}]
    },
    
    # Alternate Recipes
    "iron_wire": {
        "id": "iron_wire",
        "name": "Iron Wire (Alternate)",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Constructor",
        "powerConsumption": 4,
        "craftingSpeed": 24.0,
        "alternateRecipe": True,
        "inputs": [{"item": "iron_ingot", "amount": 50}],
        "outputs": [{"item": "wire", "amount": 90}]
    },
    "stitched_iron_plate": {
        "id": "stitched_iron_plate",
        "name": "Stitched Iron Plate (Alternate)",
        "category": "Material",
        "unlockTier": 0,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 32.0,
        "alternateRecipe": True,
        "inputs": [
            {"item": "iron_plate", "amount": 18.75},
            {"item": "wire", "amount": 37.5}
        ],
        "outputs": [{"item": "reinforced_iron_plate", "amount": 5.625}]
    },
    "bolted_frame": {
        "id": "bolted_frame",
        "name": "Bolted Frame (Alternate)",
        "category": "Component",
        "unlockTier": 2,
        "machineType": "Assembler",
        "powerConsumption": 15,
        "craftingSpeed": 24.0,
        "alternateRecipe": True,
        "inputs": [
            {"item": "reinforced_iron_plate", "amount": 7.5},
            {"item": "screw", "amount": 140}
        ],
        "outputs": [{"item": "modular_frame", "amount": 5}]
    },
}


def get_all_items():
    """Return all items."""
    return ITEMS


def get_all_recipes():
    """Return all recipes."""
    return RECIPES


def get_item_by_id(item_id):
    """Get item by ID."""
    return ITEMS.get(item_id)


def get_recipe_by_id(recipe_id):
    """Get recipe by ID."""
    return RECIPES.get(recipe_id)


def get_recipes_for_item(item_id):
    """Get all recipes that produce a given item."""
    producing_recipes = []
    for recipe_id, recipe in RECIPES.items():
        for output in recipe["outputs"]:
            if output["item"] == item_id:
                producing_recipes.append(recipe)
                break
    return producing_recipes


def get_raw_resources():
    """Get all raw resource items."""
    return {k: v for k, v in ITEMS.items() if v["isRawResource"]}


def get_craftable_items():
    """Get all non-raw items that can be crafted."""
    return {k: v for k, v in ITEMS.items() if not v["isRawResource"]}
