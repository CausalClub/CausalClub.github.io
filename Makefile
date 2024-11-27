# Makefile to update www/index.html when dependencies change

# Target file
TARGET = www/index.html

# Dependencies
DEPENDENCIES = src/layout/* src/scripts/* src/static/* src/Seminars.csv

# Rule to build the target
$(TARGET): $(DEPENDENCIES)
	bash src/scripts/render.sh

# PHONY target to force rebuild
.PHONY: clean
clean:
	rm -f $(TARGET)
