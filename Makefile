.PHONY: all scad stl test format clean

# Directories
OUTPUT_DIR := output

# Python sources that generate SCAD files
PYTHON_SRCS := $(wildcard ./*.py)

# Models and target files
MODELS := bottom cover lid

SCAD_FILES := $(sort $(patsubst %, $(OUTPUT_DIR)/%.scad, $(MODELS)) $(wildcard $(OUTPUT_DIR)/*.scad))
STL_FILES  := $(patsubst $(OUTPUT_DIR)/%.scad, $(OUTPUT_DIR)/%.stl, $(SCAD_FILES))

all: scad
scad: $(SCAD_FILES)
stl: $(STL_FILES)

$(SCAD_FILES) &: $(PYTHON_SRCS)
	uv run python main.py

# Generic rule for scad -> stl
%.stl: %.scad
	openscad -o $@ $<

# Format Python files with Ruff
format:
	uvx ruff format .

# Clean build artifacts
clean:
	rm -rf $(OUTPUT_DIR)/*.scad $(OUTPUT_DIR)/*.stl
