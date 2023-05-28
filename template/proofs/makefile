SHELL = zsh

circom = src/main.circom
r1cs = constraints/main.r1cs
wasm = witness/main_js/main.wasm
wit_gen = witness/main_js/generate_witness.js

compile_outputs = witness/main_js/witness_calculator.js $(r1cs) $(wasm) $(wit_gen)
pk = main.pk
vk = main.vk
ptau = main.ptau
keys = $(pk) $(vk)
p_input = data/input.json
wit = witness/witness.wtns
pf = main.pf.json
inst = main.inst.json
prove_outputs = $(pf) $(inst)

compiled_results = ../src ../witness ../constraints ../data


all: verify

init: $(compiled_results)
	cp -r $(compiled_results) ./

$(compile_outputs): $(circom)
	circom $< --r1cs --wasm

$(ptau):
	snarkjs powersoftau new bn128 12 tmp.ptau -v
	snarkjs powersoftau prepare phase2 tmp.ptau $(ptau) -v
	rm tmp.ptau

#$(keys): $(ptau) $(r1cs)
#	snarkjs groth16 setup $(r1cs) $(ptau) $(pk)
#	snarkjs zkey export verificationkey $(pk) $(vk)

$(keys): $(ptau) $(r1cs)
	snarkjs plonk setup $(r1cs) $(ptau) $(pk)
	snarkjs zkey export verificationkey $(pk) $(vk)

$(wit): $(p_input) $(wasm) $(wit_gen)
	node $(wit_gen) $(wasm) $(p_input) $@

#$(prove_outputs): $(wit) $(pk)
#	snarkjs groth16 prove $(pk) $(wit) $(pf) $(inst)

$(prove_outputs): $(wit) $(pk)
	snarkjs plonk prove $(pk) $(wit) $(pf) $(inst)


.PHONY = verify clean

#verify: $(pf) $(inst) $(vk)
#	snarkjs groth16 verify $(vk) $(inst) $(pf)

verify: init $(pf) $(inst) $(vk)
	snarkjs plonk verify $(vk) $(inst) $(pf)


clean:
	rm -rf src witness constraints data $(compile_outputs) $(ptau) $(keys) $(wit) $(prove_outputs)
