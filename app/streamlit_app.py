"""
Satisfactory Production Chain Calculator
Main Streamlit Application
"""

import streamlit as st
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from data import satisfactory_db
from optimizer.models import OptimizationObjective, CalculationStatus
from optimizer.solver import calculate_production_chain
from viz import graphviz_render
from storage import import_export, local_storage_component
from utils import validation

# Page configuration
st.set_page_config(
    page_title="Satisfactory Production Calculator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'unlocked_recipes' not in st.session_state:
    # Default: unlock all non-alternate recipes
    all_recipes = satisfactory_db.get_all_recipes()
    st.session_state.unlocked_recipes = set(
        rid for rid, recipe in all_recipes.items() 
        if not recipe["alternateRecipe"]
    )

if 'calculation_result' not in st.session_state:
    st.session_state.calculation_result = None

if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False


# Main title
st.title("🏭 Satisfactory Production Chain Calculator")
st.markdown("Calculate optimal production chains for Satisfactory items")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Recipe Management Section
    st.subheader("📋 Recipe Management")
    
    # Show localStorage status
    with st.expander("💾 Storage Status", expanded=False):
        local_storage_component.display_localStorage_status()
        st.info("Recipe settings are saved in your browser. Use Export/Import if localStorage is unavailable.")
    
    # Recipe preset selection
    st.markdown("**Quick Presets:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔓 Unlock All", use_container_width=True):
            all_recipes = satisfactory_db.get_all_recipes()
            st.session_state.unlocked_recipes = set(all_recipes.keys())
            st.success("All recipes unlocked!")
    
    with col2:
        if st.button("🔒 Standard Only", use_container_width=True):
            all_recipes = satisfactory_db.get_all_recipes()
            st.session_state.unlocked_recipes = set(
                rid for rid, recipe in all_recipes.items() 
                if not recipe["alternateRecipe"]
            )
            st.success("Reset to standard recipes!")
    
    # Export/Import recipes
    with st.expander("📤 Export/Import Recipes", expanded=False):
        # Export
        if st.button("📤 Export Unlocked Recipes"):
            json_string = import_export.export_unlocked_recipes(
                st.session_state.unlocked_recipes
            )
            st.download_button(
                label="⬇️ Download JSON",
                data=json_string,
                file_name="satisfactory_unlocked_recipes.json",
                mime="application/json"
            )
        
        # Import
        uploaded_file = st.file_uploader(
            "📥 Import Unlocked Recipes",
            type=['json'],
            help="Upload a previously exported recipe configuration"
        )
        
        if uploaded_file is not None:
            try:
                json_string = uploaded_file.read().decode('utf-8')
                unlocked = import_export.import_unlocked_recipes(json_string)
                if unlocked:
                    st.session_state.unlocked_recipes = unlocked
                    st.success(f"Imported {len(unlocked)} recipes!")
                else:
                    st.error("Failed to import recipes")
            except Exception as e:
                st.error(f"Error importing: {e}")
    
    # Recipe selection by category
    st.subheader("🔧 Select Recipes")
    
    all_recipes = satisfactory_db.get_all_recipes()
    
    # Group recipes by category
    categories = {}
    for recipe_id, recipe in all_recipes.items():
        category = recipe["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((recipe_id, recipe))
    
    # Display by category
    for category in sorted(categories.keys()):
        with st.expander(f"{category} ({len(categories[category])} recipes)", expanded=False):
            for recipe_id, recipe in sorted(categories[category], key=lambda x: x[1]["name"]):
                is_unlocked = recipe_id in st.session_state.unlocked_recipes
                
                label = recipe["name"]
                if recipe["alternateRecipe"]:
                    label += " (ALT)"
                
                if st.checkbox(
                    label,
                    value=is_unlocked,
                    key=f"recipe_{recipe_id}",
                    help=f"Machine: {recipe['machineType']} | Tier: {recipe['unlockTier']}"
                ):
                    st.session_state.unlocked_recipes.add(recipe_id)
                else:
                    st.session_state.unlocked_recipes.discard(recipe_id)

# Main content area
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("🎯 Production Target")
    
    # Get craftable items (non-raw resources)
    all_items = satisfactory_db.get_all_items()
    craftable_items = {
        item_id: item for item_id, item in all_items.items()
        if not item["isRawResource"]
    }
    
    # Sort items by category and name
    sorted_items = sorted(
        craftable_items.items(),
        key=lambda x: (x[1]["category"], x[1]["name"])
    )
    
    # Target item selection
    item_options = {
        f"{item['name']} ({item['category']})": item_id
        for item_id, item in sorted_items
    }
    
    selected_item_display = st.selectbox(
        "Target Item",
        options=list(item_options.keys()),
        help="Select the item you want to produce"
    )
    
    target_item_id = item_options[selected_item_display]
    
    # Target rate input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        target_rate = st.number_input(
            "Production Rate",
            min_value=0.1,
            max_value=10000.0,
            value=60.0,
            step=10.0,
            help="Desired production rate in items per minute"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**items/min**")
    
    # Optimization objective
    objective_options = {
        "Balanced": OptimizationObjective.BALANCED,
        "Minimize Machines": OptimizationObjective.MINIMIZE_MACHINES,
        "Minimize Power": OptimizationObjective.MINIMIZE_POWER,
        "Minimize Waste": OptimizationObjective.MINIMIZE_WASTE
    }
    
    selected_objective = st.selectbox(
        "Optimization Priority",
        options=list(objective_options.keys()),
        help="Choose optimization strategy for recipe selection"
    )
    
    objective = objective_options[selected_objective]
    
    # Advanced options
    with st.expander("⚙️ Advanced Options", expanded=False):
        allow_locked_preview = st.checkbox(
            "Show preview with locked recipes",
            value=False,
            help="Preview what would be possible if all recipes were unlocked"
        )
    
    # Calculate button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        calculate_button = st.button(
            "🚀 Calculate Production Chain",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        if st.session_state.calculation_result is not None:
            if st.button("🗑️ Clear Results", use_container_width=True):
                st.session_state.calculation_result = None
                st.rerun()
    
    # Perform calculation
    if calculate_button:
        # Validate inputs
        is_valid, error_msg = validation.validate_calculation_inputs(
            target_item_id,
            target_rate,
            st.session_state.unlocked_recipes
        )
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
        else:
            with st.spinner("Calculating production chain..."):
                try:
                    result = calculate_production_chain(
                        target_item_id=target_item_id,
                        target_rate=target_rate,
                        unlocked_recipes=st.session_state.unlocked_recipes,
                        objective=objective,
                        allow_locked_preview=allow_locked_preview
                    )
                    st.session_state.calculation_result = result
                except Exception as e:
                    st.error(f"❌ Calculation error: {str(e)}")
                    st.exception(e)

with col_right:
    st.header("ℹ️ Info")
    
    st.metric("Unlocked Recipes", len(st.session_state.unlocked_recipes))
    st.metric("Total Recipes", len(satisfactory_db.get_all_recipes()))
    st.metric("Total Items", len(satisfactory_db.get_all_items()))
    
    with st.expander("📖 How to Use"):
        st.markdown("""
        1. **Select recipes** in the sidebar (standard recipes are unlocked by default)
        2. **Choose target item** and production rate
        3. **Select optimization priority** (balanced, machines, power, or waste)
        4. **Click Calculate** to generate the production chain
        5. **View the diagram** and download results
        
        💡 **Tip:** Use Export/Import to save your recipe configurations!
        """)

# Display results
if st.session_state.calculation_result is not None:
    result = st.session_state.calculation_result
    
    st.markdown("---")
    st.header("📊 Results")
    
    # Status indicator
    if result.status == CalculationStatus.SUCCESS:
        st.success("✅ Production chain calculated successfully!")
    elif result.status == CalculationStatus.INSUFFICIENT_RECIPES:
        st.error("❌ Insufficient recipes unlocked")
    elif result.status == CalculationStatus.IMPOSSIBLE_RATE:
        st.error("❌ Cannot produce at requested rate")
    else:
        st.warning(f"⚠️ Status: {result.status.value}")
    
    # Display messages
    if result.messages:
        for msg in result.messages:
            st.info(msg)
    
    # Display warnings
    if result.warnings:
        for warning in result.warnings:
            st.warning(f"⚠️ {warning}")
    
    # Display missing recipes
    if result.missing_recipes:
        st.error("🔒 Missing Recipes:")
        for recipe in result.missing_recipes:
            st.markdown(f"- {recipe}")
        st.info("💡 Unlock these recipes in the sidebar to complete the chain")
    
    # Summary statistics
    if result.nodes:
        st.subheader("📈 Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Machines", result.total_machines)
        
        with col2:
            st.metric("Total Power", validation.format_power(result.total_power))
        
        with col3:
            st.metric("Production Nodes", len(result.nodes))
        
        with col4:
            st.metric("Raw Resources", result.total_raw_resources)
        
        # Raw resources
        if result.raw_resources:
            st.subheader("⛏️ Raw Resources Required")
            
            for rr in result.raw_resources:
                st.markdown(
                    f"**{rr.item_name}:** {validation.format_rate(rr.rate)}"
                )
        
        # Production nodes detail
        with st.expander("🏭 Production Nodes Detail", expanded=False):
            for i, node in enumerate(result.nodes, 1):
                st.markdown(f"**{i}. {node.recipe_name}**")
                st.markdown(
                    f"- Machine: {validation.format_machine_count(node.machine_count)}x "
                    f"{node.machine_type}"
                )
                st.markdown(f"- Output: {validation.format_rate(node.target_rate)} {node.item_produced_name}")
                st.markdown(f"- Power: {validation.format_power(node.total_power)}")
                
                if node.inputs:
                    st.markdown("- Inputs:")
                    for inp in node.inputs:
                        st.markdown(f"  - {validation.format_rate(inp.rate)} {inp.item_name}")
                
                st.markdown("---")
        
        # Visualization
        st.subheader("🗺️ Production Chain Diagram")
        
        try:
            # Render SVG
            svg_html = graphviz_render.get_svg_with_interactivity(
                result,
                show_rates=True,
                show_power=True
            )
            
            st.components.v1.html(svg_html, height=600, scrolling=True)
            
            st.info("💡 Use mouse wheel to zoom, click and drag to pan")
            
        except Exception as e:
            st.error(f"Error rendering diagram: {e}")
            st.info("Make sure Graphviz is installed on your system")
        
        # Export options
        st.subheader("💾 Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export JSON
            json_string = import_export.export_result_to_json(result)
            filename = import_export.create_download_filename(result, "json")
            
            st.download_button(
                label="📥 Download JSON",
                data=json_string,
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Export SVG
            try:
                svg_content = graphviz_render.render_to_svg(result)
                svg_filename = import_export.create_download_filename(result, "svg")
                
                st.download_button(
                    label="📥 Download SVG",
                    data=svg_content,
                    file_name=svg_filename,
                    mime="image/svg+xml",
                    use_container_width=True
                )
            except:
                st.button("📥 Download SVG", disabled=True, use_container_width=True)
                st.caption("Graphviz not available")
        
        with col3:
            # Export summary text
            summary_text = graphviz_render.create_summary_text(result)
            text_filename = import_export.create_download_filename(result, "txt")
            
            st.download_button(
                label="📥 Download Summary",
                data=summary_text,
                file_name=text_filename,
                mime="text/plain",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Satisfactory Production Chain Calculator | "
    "Built with Streamlit & Python | "
    "Data based on Satisfactory game"
    "</div>",
    unsafe_allow_html=True
)
