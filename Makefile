.PHONY: all scad stl test format clean

# Directories
OUTPUT_DIR := output
SRC_DIR := src
TESTS_DIR := tests

# Python sources that generate SCAD files
PYTHON_SRCS := main.py $(wildcard $(SRC_DIR)/*.py)

# Models and target files
MODELS := \
	two_piece_bottom \
	two_piece_lid \
	two_piece_assembly \
	travel_base \
	travel_card_tray \
	travel_lid \
	travel_assembly \
	card_tray_tier1 \
	card_tray_tier2 \
	card_tray_tier3 \
	token_tray \
	noble_tray \
	master_box \
	master_lid \
	artisanal_bottom \
	artisanal_lid \
	artisanal_cover \
	artisanal_assembly



SCAD_FILES := $(sort $(patsubst %, $(OUTPUT_DIR)/%.scad, $(MODELS)) $(wildcard $(OUTPUT_DIR)/*.scad))
STL_FILES  := $(patsubst $(OUTPUT_DIR)/%.scad, $(OUTPUT_DIR)/%.stl, $(SCAD_FILES))

all: scad stl

# Generate OpenSCAD (.scad) files from SolidPython2 scripts
scad: $(SCAD_FILES)

$(SCAD_FILES) &: $(PYTHON_SRCS)
	uv run python main.py

# Generic rule for scad -> stl
%.stl: %.scad
	openscad -o $@ $<

# Render all STL files
stl: $(STL_FILES)


# Run unit tests
test:
	uv run python -m unittest discover -s $(TESTS_DIR)

# Format Python files with Ruff
format:
	uvx ruff format .

# Clean build artifacts
clean:
	rm -rf $(OUTPUT_DIR)/*.scad $(OUTPUT_DIR)/*.stl __pycache__ src/__pycache__ tests/__pycache__
