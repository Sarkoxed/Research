.PHONY: default
default: init


.PHONY: init
init:
	@mkdir src || true
	@mkdir witness || true
	@mkdir constraints || true
	@touch src/main.circom || true
	@printf "pragma circom 2.0.0;\n\ninclude \"temp.circom\";\n\ncomponent main = temp();" > src/main.circom
	
.PHONY: witness
witness: src/main.circom input.json
	@circom src/main.circom --wasm -o witness/
	@snarkjs wc witness/main_js/main.wasm ./input.json witness/witness.wtns 
	@snarkjs wej witness/witness.wtns witness/witness.json

.PHONY: constraints
constraints: src/main.circom
	@circom $^ --r1cs --sym -o constraints/
	@snarkjs rp constraints/main.r1cs constraints/main.sym > constraints/constr
	@snarkjs rej constraints/main.r1cs constraints/constr.json

.PHONY: test
test: test.js src/main.circom
	@mocha test.js
