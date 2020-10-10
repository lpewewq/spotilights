TARGET_EXEC := lightstrip-pc
BUILD_DIR   := ./bin/release
SRC_DIRS    := ./src

CFLAGS      := -MMD -MP -std=c99 -Wall -Wextra -Werror -pedantic
LDFLAGS     := -lm

USB_DEVICE  := /dev/ttyUSB0

ifneq (,$(filter $(MAKECMDGOALS),debug))
	BUILD_DIR := ./bin/debug
	CFLAGS += -g3 -O0
endif

SRCS := $(shell find $(SRC_DIRS) -name *.c)

OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRC_DIRS) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

all: $(BUILD_DIR)/$(TARGET_EXEC)

debug: $(BUILD_DIR)/$(TARGET_EXEC)

run: $(BUILD_DIR)/$(TARGET_EXEC)
	@./$(BUILD_DIR)/$(TARGET_EXEC) $(USB_DEVICE)

$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
	@$(CC) $(OBJS) -o $@ $(LDFLAGS)
	@echo Done. Placed executable at $(BUILD_DIR)/$(TARGET_EXEC)

$(BUILD_DIR)/%.c.o: %.c
	@mkdir -p $(dir $@)
	@echo Compiling $<
	@$(CC) $(INC_FLAGS) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	$(RM) -r ./bin

-include $(DEPS)
