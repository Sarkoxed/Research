.PHONY: default
default: init

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

.PHONY: verify
verify: witness map veripy

.PHONY: deep_verify
deep_verify: witness map deep_veripy

.PHONY: check
check: deep_verify tools/verify.py constraints/constr.json witness/witness.json tools/map.js
	@rm calculations/*
	@python tools/verify.py 2
	@tools/check.sh

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

.PHONY: veripy
veripy: tools/verify.py constraints/constr.json witness/witness.json 
	@python tools/verify.py 1

.PHONY: deep_veripy
deep_veripy: tools/verify.py constraints/constr.json witness/witness.json tools/map.js
	@python tools/verify.py 2

.PHONY: self_witness
self_gen_witness: data/input1.json src/main.circom
	@circom src/main.circom --wasm -o twitness/
	@snarkjs wc twitness/main_js/main.wasm data/input1.json twitness/witness.wtns 
	@snarkjs wej twitness/witness.wtns twitness/witness.json

.PHONY: test
test: tools/test.js src/main.circom
	@mocha tools/test.js
