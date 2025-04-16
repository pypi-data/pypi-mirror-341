.PHONY: all clean

all: src/pycregex/stub.so

src/pycregex/stub.so: src/pycregex/stub.c
	$(CC) $(CFLAGS) -shared $< -o $@

clean:
	rm -f src/pycregex/stub.so
