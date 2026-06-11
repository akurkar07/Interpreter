CC = gcc
CFLAGS ?= -Wall -Wextra -std=c11 -g

BUILD_DIR := build
TARGET := $(BUILD_DIR)/vm.exe
SRC := native/vm.c
OBJ := $(BUILD_DIR)/vm.o
PBC ?= examples\FeatureShowcase.pbc

.PHONY: all run clean

all: $(TARGET)

$(BUILD_DIR):
	if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)

$(TARGET): $(OBJ) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: native/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	.\$(TARGET) $(PBC)

clean:
	powershell -NoProfile -Command "Remove-Item -Force -Recurse -ErrorAction SilentlyContinue '$(BUILD_DIR)'; exit 0"
