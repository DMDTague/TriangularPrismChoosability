.PHONY: verify brute house-brute audit audit-long paper clean

verify:
	python3 checks/certificate_rebuild.py
	python3 checks/paper_checks.py
	c++ -O2 -std=c++17 checks/house_type_enumeration.cpp -o .house_type_enumeration
	./.house_type_enumeration 4
	./.house_type_enumeration 5
	@rm -f .house_type_enumeration

brute:
	cc -O3 checks/bruteforce_small_universes.c -o .bruteforce_small_universes
	./.bruteforce_small_universes 1 3 6
	./.bruteforce_small_universes 1 4 6
	./.bruteforce_small_universes 1 5 7
	@rm -f .bruteforce_small_universes

house-brute:
	cc -O3 checks/bruteforce_small_universes.c -o .bruteforce_small_universes
	./.bruteforce_small_universes 2 4 8
	@rm -f .bruteforce_small_universes

audit:
	python3 audit/a1_certificate.py paper/main.tex audit/outputs/a1_certificate_output.txt .F0.pkl
	python3 audit/a2_model_validation.py .F0.pkl > audit/outputs/a2_model_validation_output.txt
	cc -O2 audit/a3_house_census.c -o .a3_house_census
	./.a3_house_census 4 > audit/outputs/a3_house_census_k4.txt
	./.a3_house_census 5 > audit/outputs/a3_house_census_k5.txt
	python3 audit/a4_identities.py > audit/outputs/a4_identities_output.txt
	cc -O2 audit/a5_prism_census.c -o .a5_prism_census
	./.a5_prism_census 3 > audit/outputs/a5_prism_k3.txt
	./.a5_prism_census 4 8 > audit/outputs/a5_prism_k4_U8.txt
	python3 audit/a6_validate.py > audit/outputs/a6_validate_output.txt
	@rm -f .a3_house_census .a5_prism_census .F0.pkl

audit-long:
	cc -O2 audit/a3_house_census.c -o .a3_house_census
	./.a3_house_census 6 > audit/outputs/a3_house_census_k6.txt
	cc -O2 audit/a5_prism_census.c -o .a5_prism_census
	./.a5_prism_census 4 9 > audit/outputs/a5_prism_k4_U9.txt
	./.a5_prism_census 5 8 > audit/outputs/a5_prism_k5_U8.txt
	./.a5_prism_census 4 10 > audit/outputs/a5_prism_k4_U10.txt
	@rm -f .a3_house_census .a5_prism_census

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	cd paper && latexmk -C main.tex || true
	rm -f .house_type_enumeration .bruteforce_small_universes .a3_house_census .a5_prism_census .F0.pkl
