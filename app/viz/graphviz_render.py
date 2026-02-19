"""
Graphviz rendering for production chain visualization.
"""

import graphviz
from typing import List, Optional
import tempfile
import os
from pathlib import Path

from optimizer.models import ProductionChainResult, MachineNode, Connection

# Configure Graphviz executable path for Windows
if os.name == 'nt':  # Windows
    graphviz_path = Path(r"C:\Program Files\Graphviz\bin")
    if graphviz_path.exists():
        os.environ["PATH"] = str(graphviz_path) + os.pathsep + os.environ.get("PATH", "")


def create_production_graph(
    result: ProductionChainResult,
    show_rates: bool = True,
    show_power: bool = True,
    collapse_by_tier: bool = False
) -> graphviz.Digraph:
    """
    Create a Graphviz graph from production chain result.
    
    Args:
        result: Production chain result
        show_rates: Show production rates on edges
        show_power: Show power consumption on nodes
        collapse_by_tier: Group nodes by tier (for large diagrams)
    
    Returns:
        Graphviz Digraph object
    """
    # Create graph
    dot = graphviz.Digraph(
        comment=f'Production Chain: {result.target_item_name}',
        format='svg'
    )
    
    # Graph attributes
    dot.attr(rankdir='LR')  # Left to right layout
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    dot.attr('edge', fontname='Arial', fontsize='10')
    
    # Add nodes
    for node in result.nodes:
        label = _create_node_label(node, show_power)
        color = _get_node_color(node)
        tooltip = _create_node_tooltip(node)
        
        dot.node(
            node.node_id,
            label=label,
            fillcolor=color,
            tooltip=tooltip
        )
    
    # Add raw resource nodes
    for raw_resource in result.raw_resources:
        label = f"{raw_resource.item_name}\\n{raw_resource.rate:.1f}/min"
        dot.node(
            f"raw_{raw_resource.item_id}",
            label=label,
            fillcolor='#90EE90',  # Light green
            shape='ellipse',
            tooltip=f"Raw Resource: {raw_resource.item_name}"
        )
    
    # Add connections
    for connection in result.connections:
        label = ""
        if show_rates:
            label = f"{connection.rate:.1f}/min"
        
        color = 'blue' if not connection.is_recycling_loop else 'red'
        style = 'solid' if not connection.is_recycling_loop else 'dashed'
        
        dot.edge(
            connection.from_node_id,
            connection.to_node_id,
            label=label,
            color=color,
            style=style
        )
    
    # Connect raw resources to their consumers
    for node in result.nodes:
        for input_flow in node.inputs:
            # Check if this is a raw resource
            if any(rr.item_id == input_flow.item_id for rr in result.raw_resources):
                label = f"{input_flow.rate:.1f}/min" if show_rates else ""
                dot.edge(
                    f"raw_{input_flow.item_id}",
                    node.node_id,
                    label=label,
                    color='green',
                    style='solid'
                )
    
    return dot


def _create_node_label(node: MachineNode, show_power: bool) -> str:
    """Create label for a machine node."""
    lines = []
    
    # Recipe name
    lines.append(node.recipe_name)
    
    # Machine count
    machine_count_ceil = int(node.machine_count + 0.99)  # Ceiling
    if node.machine_count % 1 < 0.01:  # Nearly whole number
        lines.append(f"{machine_count_ceil}x {node.machine_type}")
    else:
        lines.append(f"{node.machine_count:.2f}x {node.machine_type}")
    
    # Output rate
    lines.append(f"→ {node.target_rate:.1f} {node.item_produced_name}/min")
    
    # Power
    if show_power:
        lines.append(f"⚡ {node.total_power:.1f} MW")
    
    return "\\n".join(lines)


def _get_node_color(node: MachineNode) -> str:
    """Get color for node based on machine type."""
    colors = {
        'Smelter': '#FFB6C1',      # Light pink
        'Constructor': '#ADD8E6',  # Light blue
        'Assembler': '#DDA0DD',    # Plum
        'Manufacturer': '#F0E68C', # Khaki
        'Foundry': '#FFA07A',      # Light salmon
        'Refinery': '#98FB98',     # Pale green
    }
    return colors.get(node.machine_type, '#E0E0E0')  # Default gray


def _create_node_tooltip(node: MachineNode) -> str:
    """Create tooltip text for a node."""
    lines = [
        f"Recipe: {node.recipe_name}",
        f"Machine: {node.machine_type}",
        f"Count: {node.machine_count:.2f}",
        f"Output: {node.target_rate:.2f} {node.item_produced_name}/min",
        f"Power: {node.total_power:.2f} MW"
    ]
    
    if node.inputs:
        lines.append("Inputs:")
        for inp in node.inputs:
            lines.append(f"  - {inp.rate:.2f} {inp.item_name}/min")
    
    return "\\n".join(lines)


def render_to_svg(result: ProductionChainResult, **kwargs) -> str:
    """
    Render production chain to SVG string.
    
    Args:
        result: Production chain result
        **kwargs: Additional arguments for create_production_graph
    
    Returns:
        SVG string
    """
    dot = create_production_graph(result, **kwargs)
    dot.format = 'svg'
    
    try:
        svg_bytes = dot.pipe()
        return svg_bytes.decode('utf-8')
    except Exception as e:
        return f"<svg><text x='10' y='20'>Error rendering graph: {str(e)}</text></svg>"


def render_to_png(result: ProductionChainResult, output_path: str, **kwargs) -> bool:
    """
    Render production chain to PNG file.
    
    Args:
        result: Production chain result
        output_path: Path to save PNG file
        **kwargs: Additional arguments for create_production_graph
    
    Returns:
        True if successful, False otherwise
    """
    dot = create_production_graph(result, **kwargs)
    dot.format = 'png'
    
    try:
        dot.render(output_path, cleanup=True)
        return True
    except Exception as e:
        print(f"Error rendering PNG: {e}")
        return False


def render_to_file(
    result: ProductionChainResult,
    output_path: str,
    format: str = 'svg',
    **kwargs
) -> bool:
    """
    Render production chain to file.
    
    Args:
        result: Production chain result
        output_path: Path to save file (without extension)
        format: Output format ('svg', 'png', 'pdf')
        **kwargs: Additional arguments for create_production_graph
    
    Returns:
        True if successful, False otherwise
    """
    dot = create_production_graph(result, **kwargs)
    dot.format = format
    
    try:
        dot.render(output_path, cleanup=True)
        return True
    except Exception as e:
        print(f"Error rendering to {format}: {e}")
        return False


def get_svg_with_interactivity(result: ProductionChainResult, **kwargs) -> str:
    """
    Get SVG with enhanced interactivity (zoom, pan, tooltips).
    
    Args:
        result: Production chain result
        **kwargs: Additional arguments for create_production_graph
    
    Returns:
        HTML string with SVG and JavaScript for interactivity
    """
    svg_content = render_to_svg(result, **kwargs)
    
    # Wrap SVG in HTML with pan/zoom capabilities
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
            #svg-container {{
                width: 100vw;
                height: 100vh;
                cursor: grab;
            }}
            #svg-container:active {{
                cursor: grabbing;
            }}
            svg {{
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="svg-container">
            {svg_content}
        </div>
        <script>
            // Simple pan and zoom
            const container = document.getElementById('svg-container');
            const svg = container.querySelector('svg');
            
            let scale = 1;
            let translateX = 0;
            let translateY = 0;
            let isDragging = false;
            let startX, startY;
            
            // Zoom on scroll
            container.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                scale *= delta;
                updateTransform();
            }});
            
            // Pan on drag
            container.addEventListener('mousedown', (e) => {{
                isDragging = true;
                startX = e.clientX - translateX;
                startY = e.clientY - translateY;
            }});
            
            container.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    translateX = e.clientX - startX;
                    translateY = e.clientY - startY;
                    updateTransform();
                }}
            }});
            
            container.addEventListener('mouseup', () => {{
                isDragging = false;
            }});
            
            function updateTransform() {{
                svg.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{scale}})`;
            }}
        </script>
    </body>
    </html>
    """
    
    return html


def create_summary_text(result: ProductionChainResult) -> str:
    """
    Create a text summary of the production chain.
    
    Args:
        result: Production chain result
    
    Returns:
        Text summary
    """
    lines = []
    lines.append(f"Production Chain for {result.target_item_name}")
    lines.append(f"Target Rate: {result.target_rate:.2f}/min")
    lines.append(f"Status: {result.status.value}")
    lines.append("")
    
    lines.append(f"Total Machines: {result.total_machines}")
    lines.append(f"Total Power: {result.total_power:.2f} MW")
    lines.append(f"Raw Resources Required: {result.total_raw_resources}")
    lines.append("")
    
    if result.raw_resources:
        lines.append("Raw Resources:")
        for rr in result.raw_resources:
            lines.append(f"  - {rr.item_name}: {rr.rate:.2f}/min")
        lines.append("")
    
    if result.nodes:
        lines.append("Production Nodes:")
        for node in result.nodes:
            lines.append(f"  - {node.recipe_name}: {node.machine_count:.2f}x {node.machine_type}")
        lines.append("")
    
    if result.warnings:
        lines.append("Warnings:")
        for warning in result.warnings:
            lines.append(f"  ! {warning}")
        lines.append("")
    
    if result.missing_recipes:
        lines.append("Missing Recipes:")
        for recipe in result.missing_recipes:
            lines.append(f"  - {recipe}")
    
    return "\n".join(lines)
