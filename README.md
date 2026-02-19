# Satisfactory Production Chain Calculator

A powerful production chain calculator for the game Satisfactory, built with Python and Streamlit.

## Quick Start

### Windows
```powershell
cd app
.\install.bat   # First time only
.\run.bat       # Start the app
```

### Linux/macOS
```bash
cd app
chmod +x install.sh run.sh  # First time only
./install.sh                # First time only
./run.sh                    # Start the app
```

Then open your browser at `http://localhost:8501`

## Features

✅ **P0 Features (Implemented)**
- Target item selection with production rate input
- Optimization priority selection (balanced, minimize machines/power/waste)
- Recipe unlock configuration UI with browser localStorage persistence
- Production chain computation with multi-stage dependency resolution
- Interactive SVG visualization with zoom/pan and tooltips
- Clear error messages for insufficient recipes
- Export to SVG, JSON, and text summary

## Stack

- **UI & App:** Streamlit only
- **Data Storage:** In-memory Python dictionaries (no SQL database)
- **User Config:** Browser localStorage with JSON export/import fallback
- **Visualization:** Graphviz (SVG/PNG generation)

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Graphviz** (system package)

---

### Windows Installation

#### 1. Install Graphviz

Choose one of the following methods:

**Using winget (Recommended):**
```powershell
winget install --id Graphviz.Graphviz
```

**Using Chocolatey:**
```powershell
choco install graphviz
```

**Manual Installation:**
- Download from: https://graphviz.org/download/
- Install and make sure it's added to your PATH

**Verify installation:**
```powershell
# Close and reopen PowerShell, then run:
where dot
# Should show: C:\Program Files\Graphviz\bin\dot.exe
```

#### 2. Install Python Dependencies

Run the provided installation script:
```powershell
cd app
.\install.bat
```

This will:
- Create a virtual environment (if not exists)
- Install all required Python packages
- Verify Graphviz installation

---

### Linux/macOS Installation

#### 1. Install Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**Fedora:**
```bash
sudo dnf install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Verify installation:**
```bash
which dot
# Should show the path to dot executable
```

#### 2. Install Python Dependencies

#### Using the provided scripts:

```bash
cd app

# Make scripts executable (first time only)
chmod +x install.sh run.sh

# Run installation and run 
./install.sh
venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

#### Manual installation:

```bash
cd app

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

### Windows

Simply run the provided batch file:
```powershell
cd app
.\run.bat
```

This will:
- Activate the virtual environment
- Start Streamlit
- Open the app at `http://localhost:8501`

**Alternative (manual):**
```powershell
cd app
.\venv\Scripts\activate
streamlit run streamlit_app.py
```

### Linux/macOS

#### Using the provided script:

```bash
cd app
./run.sh
```

#### Manual method:

```bash
cd app

# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

**To stop the application:** Press `Ctrl+C` in the terminal

## Usage

### 1. Configure Recipes

In the sidebar:
- Use **Quick Presets** to unlock all recipes or reset to standard recipes
- Browse recipes by category and check/uncheck to unlock/lock
- Your selections are saved in browser localStorage

### 2. Select Production Target

1. Choose your **target item** from the dropdown (sorted by category)
2. Enter the desired **production rate** (items/min)
3. Select your **optimization priority**:
   - **Balanced:** Good all-around choice
   - **Minimize Machines:** Fewest machine count
   - **Minimize Power:** Lowest power consumption
   - **Minimize Waste:** Best input/output efficiency

### 3. Calculate

Click **"Calculate Production Chain"** to generate the solution.

### 4. View Results

- **Summary:** Total machines, power consumption, raw resources
- **Raw Resources:** Required input rates for all raw materials
- **Production Nodes:** Detailed breakdown of each production step
- **Diagram:** Interactive visualization (zoom with mouse wheel, pan by dragging)

### 5. Export

- **JSON:** Complete calculation data (can be re-imported)
- **SVG:** Vector diagram for documentation
- **Summary:** Text summary of the production chain

## Data Storage

### Recipe Configuration

- **Primary:** Browser localStorage (persists across sessions)
- **Fallback:** Export/Import JSON files

### Calculation Results

- **Export only:** Download as JSON, SVG, or text
- No server-side storage (everything is client-side)

## Project Structure

```
app/
├── streamlit_app.py              # Main Streamlit UI
├── requirements.txt              # Python dependencies
├── data/
│   ├── satisfactory_db.py        # Items & recipes database
│   └── __init__.py
├── optimizer/
│   ├── models.py                 # Data classes (nodes, edges, results)
│   ├── objectives.py             # Scoring functions for optimization
│   ├── solver.py                 # Production chain computation algorithm
│   └── __init__.py
├── viz/
│   ├── graphviz_render.py        # Visualization & diagram generation
│   └── __init__.py
├── storage/
│   ├── local_storage_component.py # Browser localStorage bridge
│   ├── import_export.py          # JSON import/export
│   └── __init__.py
└── utils/
    ├── validation.py             # Input validation & formatting
    └── __init__.py
```

## Algorithm Overview

The production chain solver works recursively:

1. **Target Selection:** User specifies item and rate
2. **Recipe Selection:** Algorithm picks best recipe based on optimization objective
3. **Dependency Resolution:** Recursively resolves all input requirements
4. **Machine Calculation:** Computes exact machine counts for each step
5. **Connection Building:** Creates edges between production nodes
6. **Visualization:** Generates interactive Graphviz diagram

### Optimization Objectives

- **MINIMIZE_MACHINES:** Prefer recipes that need fewer machines
- **MINIMIZE_POWER:** Prefer recipes with lower power consumption
- **MINIMIZE_WASTE:** Prefer recipes with better input/output efficiency
- **BALANCED:** Weight all factors equally

### Circular Dependencies

The solver detects circular dependencies (recycling loops) and marks them in the visualization with dashed red lines.

## Recipe Database

The included recipe database contains:
- **Raw Resources:** Iron Ore, Copper Ore, Coal, Limestone, Caterium Ore, Raw Quartz, Crude Oil, Water
- **Ingots:** Iron, Copper, Steel, Caterium
- **Basic Materials:** Concrete, Wire, Cable, Rods, Plates, Pipes, Beams, etc.
- **Components:** Rotors, Modular Frames, Motors, Computers, Circuit Boards, etc.
- **Machines:** Smelter, Constructor, Assembler, Manufacturer, Foundry, Refinery
- **Alternate Recipes:** Iron Wire, Stitched Iron Plate, Bolted Frame, etc.

All values are based on Satisfactory game data (crafting times, power consumption, input/output rates).

## Troubleshooting

### "Error rendering diagram" or "failed to execute WindowsPath('dot')"

**Cause:** Graphviz is not installed or not in your system PATH.

**Solution:**

**Windows:**
```powershell
# Install Graphviz
winget install --id Graphviz.Graphviz

# Restart your terminal (important!)
# Or refresh PATH in current session:
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
where dot
```

**Linux/macOS:**
```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Verify
which dot
```

After installing Graphviz, **restart Streamlit** (Ctrl+C and run again).

### "streamlit: command not found" or "No module named streamlit"

**Cause:** Virtual environment is not activated or dependencies not installed.

**Solution:**
```bash
# Run the installation script
# Windows: .\install.bat
# Linux/macOS: ./install.sh
```

### "LocalStorage is not available"

**Solution:** Use Export/Import buttons to save/load recipe configurations as JSON files

### "Insufficient recipes unlocked"

**Solution:** Unlock required recipes in the sidebar. The error message will list which recipes are needed.

### Calculation is slow

**Solution:** This is normal for complex items with deep dependency chains (e.g., Computers, Heavy Modular Frames)

## Future Enhancements (P1/P2)

Not yet implemented but planned:

- **P1:**
  - Auto-recalc on input change
  - Machine/power/waste objective improvements
  - Collapse groups for 50+ machines
  - Search/filter in diagrams
  
- **P2:**
  - Variant comparison (show multiple solutions)
  - Recycling loop styling improvements
  - Import JSON to restore calculations
  - More alternate recipes
  - Clock speed adjustment

## Contributing

This is a personal project, but suggestions for improvements are welcome!

## License

This project is for educational purposes. Satisfactory is a trademark of Coffee Stain Studios.

## Credits

- **Game:** Satisfactory by Coffee Stain Studios
- **Framework:** Streamlit
- **Visualization:** Graphviz
- **Data:** Based on Satisfactory game mechanics

---

**Enjoy optimizing your factories!** 🏭
