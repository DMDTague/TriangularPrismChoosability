.PHONY: verify brute paper clean

verify:
	python3 checks/certificate_rebuild.py
	python3 checks/paper_checks.py
	c++ -O2 -std=c++17 checks/house_type_enumeration.cpp -o .house_type_enumeration
	./.house_type_enumeration 4
	./.house_type_enumeration 5
	@rm -f .house_type_enumeration

brute:
	cc -O2 checks/bruteforce_small_universes.c -o .bruteforce_small_universes
	./.bruteforce_small_universes 1 3 6
	./.bruteforce_small_universes 2 4 8
	@rm -f .bruteforce_small_universes

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	cd paper && latexmk -C main.tex || true
	rm -f .house_type_enumeration .bruteforce_small_universes
