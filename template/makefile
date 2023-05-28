.PHONY: default
default: init

all: constraints witness map

.PHONY: init
init:
	@mkdir src || true
	@mkdir data || true
	@mkdir witness || true
	@mkdir twitness || true
	@mkdir constraints || true
	@mkdir calculations || true
	@cp -r ../tools tools || true
	@touch src/main.circom || true
	@printf "pragma circom 2.0.0;\n\ninclude \"temp.circom\";\n\ncomponent main = temp();" > src/main.circom

.PHONY: witness
witness: src/*.circom data/input.json
	@circom src/main.circom --wasm -o witness/
	@snarkjs wc witness/main_js/main.wasm data/input.json witness/witness.wtns 
	@snarkjs wej witness/witness.wtns witness/witness.json

.PHONY: constraints
constraints: src/*.circom
	@circom src/main.circom --r1cs --sym -o constraints/
	@snarkjs rp constraints/main.r1cs constraints/main.sym > constraints/constr
	@snarkjs rej constraints/main.r1cs constraints/constr.json

.PHONY: map
map: constraints
	@node tools/map.js

.PHONY: verify
verify: constraints witness map veripy

.PHONY: deep_verify
deep_verify: constraints witness map deep_veripy

.PHONY: check
check: deep_verify tools/verify.py constraints/constr.json witness/witness.json tools/map.js
	@rm calculations/*
	@python tools/verify.py 2
	@tools/check.sh


.PHONY: verify_circuit
verify_circuit: constraints witness map tools/verify.py  
	@python tools/verify.py --all

.PHONY: verify_equal
verify_equal: constraints witness map verify_equal.py python_function.py 
	@python verify_equal.py --all

.PHONY: self_witness
self_witness: data/input1.json src/main.circom
	@circom src/main.circom --wasm -o twitness/
	@snarkjs wc twitness/main_js/main.wasm data/input1.json twitness/witness.wtns 
	@snarkjs wej twitness/witness.wtns twitness/witness.json

.PHONY: test
test: tools/test.js src/main.circom
	@mocha tools/test.js

.PHONY: clean
clean: 
	@echo "Cleaning constraints, witness, twitness and calculations directories"
	@rm constraints/* 2>/dev/null || true
	@rm -r witness/* 2>/dev/null || true
	@rm -r twitness/* 2>/dev/null || true
	@rm -r calculations/* 2>/dev/null || true
