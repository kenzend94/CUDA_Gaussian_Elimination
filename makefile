# Define the compiler
CC=nvcc

# Define the target executable
TARGET=gaussian_elimination

# Define the source file
SRC=gaussian_elimination.cu

# Define the build rule
all: $(TARGET)

# Define how to build the target
$(TARGET): $(SRC)
	$(CC) -o $(TARGET) $(SRC)

# Define the clean rule
clean:
	rm -f $(TARGET)

# Define the run rule
run: $(TARGET)
	./$(TARGET)