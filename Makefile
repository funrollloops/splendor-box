.PHONY: all scad stl test format clean

# Directories
OUTPUT_DIR := output
SRC_DIR := src
TESTS_DIR := tests

# Target STLs
SCAD_FILES := $(wildcard $(OUTPUT_DIR)/*.scad)
STL_FILES := $(patsubst $(OUTPUT_DIR)/%.scad, $(OUTPUT_DIR)/%.stl, $(SCAD_FILES))

all: scad stl

# Generate OpenSCAD (.scad) files from SolidPython2 scripts
scad:
	uv run python main.py

# Render STL files from OpenSCAD models
stl: scad
	@mkdir -p $(OUTPUT_DIR)
	@for scad_file in $(OUTPUT_DIR)/*.scad; do \
		stl_file="$${scad_file%.scad}.stl"; \
		echo "Rendering $$scad_file -> $$stl_file"; \
		openscad -o "$$stl_file" "$$scad_file"; \
	done

# Run unit tests
test:
	uv run python -m unittest discover -s $(TESTS_DIR)

# Format Python files with Ruff
format:
	uvx ruff format .

# Clean build artifacts
clean:
	rm -rf $(OUTPUT_DIR)/*.scad $(OUTPUT_DIR)/*.stl __pycache__ src/__pycache__ tests/__pycache__
