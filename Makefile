.PHONY: clean all

all: index.html

clean:
	rm -f index.html

index.html: $(addprefix src/, index.pug layout.pug next.pug upcoming.pug past.pug) Seminars.csv render.py
	python3 render.py -u Seminars.csv
	npx pug --doctype html --pretty src/index.pug --out .