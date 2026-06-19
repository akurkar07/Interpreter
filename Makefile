CC = gcc
CFLAGS ?= -Wall -Wextra -std=c11 -g

BUILD_DIR := build
TARGET := $(BUILD_DIR)/vm.exe
SRC := native/main.c native/vm.c native/bytecode_loader.c native/value_ops.c
OBJ := $(patsubst native/%.c,$(BUILD_DIR)/%.o,$(SRC))
PBC ?= examples\FeatureShowcase.pbc

.PHONY: all run clean

all: $(TARGET)

$(BUILD_DIR):
	if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)

$(TARGET): $(OBJ) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: native/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/main.o: native/vm.h native/bytecode_loader.h
$(BUILD_DIR)/vm.o: native/vm.h native/value_ops.h
$(BUILD_DIR)/bytecode_loader.o: native/bytecode_loader.h native/vm.h
$(BUILD_DIR)/value_ops.o: native/value_ops.h native/vm.h

run: $(TARGET)
	.\$(TARGET) $(PBC)

clean:
	if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
