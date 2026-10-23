CC = gcc
CFLAGS ?= -Wall -Wextra -std=c11 -g

BUILD_DIR := build
SRC := native/main.c native/vm.c native/bytecode_loader.c native/value_ops.c
OBJ := $(patsubst native/%.c,$(BUILD_DIR)/%.o,$(SRC))
PBC ?= examples/FeatureShowcase.pbc

ifeq ($(OS),Windows_NT)
    TARGET := $(BUILD_DIR)/vm.exe
    MKDIR = if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)
    RM_BUILD = if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
    RUN = .\$(subst /,\,$(TARGET)) $(subst /,\,$(PBC))
else
    TARGET := $(BUILD_DIR)/vm
    MKDIR = mkdir -p $(BUILD_DIR)
    RM_BUILD = rm -rf $(BUILD_DIR)
    RUN = ./$(TARGET) $(PBC)
endif

.PHONY: all run test clean

all: $(TARGET)

$(BUILD_DIR):
	$(MKDIR)

$(TARGET): $(OBJ) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: native/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/main.o: native/vm.h native/bytecode_loader.h
$(BUILD_DIR)/vm.o: native/vm.h native/value_ops.h
$(BUILD_DIR)/bytecode_loader.o: native/bytecode_loader.h native/vm.h
$(BUILD_DIR)/value_ops.o: native/value_ops.h native/vm.h

run: $(TARGET)
	$(RUN)

# Every example must produce identical output on the interpreter, the Python VM and the C VM.
test: $(TARGET)
	python3 tests/differential.py

clean:
	$(RM_BUILD)
