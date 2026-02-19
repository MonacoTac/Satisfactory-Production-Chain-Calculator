"""
Browser localStorage component for Streamlit.
Uses HTML/JavaScript bridge to interact with browser localStorage.
"""

import streamlit.components.v1 as components
import json
from typing import Optional, Set


def get_local_storage_value(key: str) -> Optional[str]:
    """
    Get a value from localStorage (read-only component).
    
    Args:
        key: localStorage key
    
    Returns:
        Value string or None
    
    Note: This returns None in the initial render. Use session state to persist.
    """
    # Create HTML with JavaScript to read from localStorage
    html_code = f"""
    <script>
        // Get value from localStorage
        const value = localStorage.getItem("{key}");
        
        // Send to Streamlit via postMessage
        window.parent.postMessage({{
            type: "streamlit:setComponentValue",
            value: value
        }}, "*");
    </script>
    <div style="display: none;">Reading from localStorage...</div>
    """
    
    # Render component (returns the value)
    result = components.html(html_code, height=0)
    return result


def set_local_storage_value(key: str, value: str):
    """
    Set a value in localStorage.
    
    Args:
        key: localStorage key
        value: Value to store (will be converted to string)
    """
    # Escape the value for JavaScript
    escaped_value = json.dumps(value)
    
    # Create HTML with JavaScript to write to localStorage
    html_code = f"""
    <script>
        // Set value in localStorage
        localStorage.setItem("{key}", {escaped_value});
        
        // Confirm to Streamlit
        window.parent.postMessage({{
            type: "streamlit:setComponentValue",
            value: "success"
        }}, "*");
    </script>
    <div style="display: none;">Writing to localStorage...</div>
    """
    
    components.html(html_code, height=0)


def remove_local_storage_value(key: str):
    """
    Remove a value from localStorage.
    
    Args:
        key: localStorage key
    """
    html_code = f"""
    <script>
        localStorage.removeItem("{key}");
        window.parent.postMessage({{
            type: "streamlit:setComponentValue",
            value: "removed"
        }}, "*");
    </script>
    <div style="display: none;">Removing from localStorage...</div>
    """
    
    components.html(html_code, height=0)


def clear_local_storage():
    """Clear all localStorage."""
    html_code = """
    <script>
        localStorage.clear();
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: "cleared"
        }, "*");
    </script>
    <div style="display: none;">Clearing localStorage...</div>
    """
    
    components.html(html_code, height=0)


# Helper functions for recipe storage

UNLOCKED_RECIPES_KEY = "satisfactory_unlocked_recipes"


def save_unlocked_recipes_to_storage(unlocked_recipes: Set[str]):
    """
    Save unlocked recipes to localStorage.
    
    Args:
        unlocked_recipes: Set of recipe IDs
    """
    json_string = json.dumps(list(unlocked_recipes))
    set_local_storage_value(UNLOCKED_RECIPES_KEY, json_string)


def load_unlocked_recipes_from_storage() -> Optional[Set[str]]:
    """
    Load unlocked recipes from localStorage.
    
    Returns:
        Set of recipe IDs or None if not found
    """
    value = get_local_storage_value(UNLOCKED_RECIPES_KEY)
    
    if value:
        try:
            recipe_list = json.loads(value)
            return set(recipe_list)
        except:
            return None
    
    return None


def create_localStorage_reader(key: str, default_value: str = "") -> str:
    """
    Create HTML/JS code to read from localStorage and display in Streamlit.
    Returns the value through Streamlit's component value system.
    
    Args:
        key: localStorage key
        default_value: Default value if key doesn't exist
    
    Returns:
        HTML string
    """
    default_json = json.dumps(default_value)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            function readLocalStorage() {{
                const value = localStorage.getItem("{key}");
                const result = value !== null ? value : {default_json};
                
                // Send to Streamlit
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: result
                }}, "*");
            }}
            
            // Read on load
            window.addEventListener('load', readLocalStorage);
        </script>
    </head>
    <body>
        <div style="font-family: sans-serif; font-size: 12px; color: #666;">
            Reading from localStorage...
        </div>
    </body>
    </html>
    """
    
    return html


def create_localStorage_writer(key: str, value: str) -> str:
    """
    Create HTML/JS code to write to localStorage.
    
    Args:
        key: localStorage key
        value: Value to write
    
    Returns:
        HTML string
    """
    value_json = json.dumps(value)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            function writeLocalStorage() {{
                localStorage.setItem("{key}", {value_json});
                
                // Confirm to Streamlit
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: "success"
                }}, "*");
            }}
            
            // Write on load
            window.addEventListener('load', writeLocalStorage);
        </script>
    </head>
    <body>
        <div style="font-family: sans-serif; font-size: 12px; color: #666;">
            Saved to localStorage ✓
        </div>
    </body>
    </html>
    """
    
    return html


def display_localStorage_status():
    """Display localStorage availability status."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .status {
                font-family: sans-serif;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            .available {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .unavailable {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
        <script>
            function checkLocalStorage() {
                const statusDiv = document.getElementById('status');
                try {
                    localStorage.setItem('test', 'test');
                    localStorage.removeItem('test');
                    statusDiv.className = 'status available';
                    statusDiv.innerHTML = '✓ LocalStorage is available';
                } catch(e) {
                    statusDiv.className = 'status unavailable';
                    statusDiv.innerHTML = '✗ LocalStorage is not available (use Export/Import)';
                }
            }
            
            window.addEventListener('load', checkLocalStorage);
        </script>
    </head>
    <body>
        <div id="status" class="status">Checking...</div>
    </body>
    </html>
    """
    
    components.html(html, height=60)
