const chai = require("chai");
const path = require("path");
const crypto = require("crypto");

const assert = chai.assert;

//const sha256 = require("./helpers/sha256");

const wasm_tester = require("../test/tester");

// const printSignal = require("./helpers/printsignal");


function buffer2bitArray(b) {
    const res = [];
    for (let i=0; i<b.length; i++) {
        for (let j=0; j<8; j++) {
            res.push((b[i] >> (7-j) &1));
        }
    }
    return res;
}

function bitArray2buffer(a) {
    const len = Math.floor((a.length -1 )/8)+1;
    const b = new Buffer.alloc(len);

    for (let i=0; i<a.length; i++) {
        const p = Math.floor(i/8);
        b[p] = b[p] | (Number(a[i]) << ( 7 - (i%8)  ));
    }
    return b;
}

function bitArray2num(a){
    let res = BigInt(0);
    for (let i = 0; i < a.length; i++){
        res = res * 2 + a[i];
    }
    return res;
}

function randint(max) {
  return Math.floor(Math.random() * max);
}

function xor3(a, b, c){
    const out = [];
    for(var i = 0; i < 32; i++){
        out.push(BigInt(a[i] ^ b[i] ^ c[i]));
    }
    return out;
}

describe("rotr test", function () {
    this.timeout(100000);
    it("Should calculate a hash", async () => {
        const cir = await wasm_tester(path.join(__dirname, "src", "main.circom"));

        let b = [];
        let a = [];
        let c = [];

        for (let i=0; i<32; i++) {
            b.push(randint(2));
            a.push(randint(2));
            c.push(randint(2));
        }
        //let b = [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0];
        console.log(a);
        console.log(b);
        console.log(c);


        const witness = await cir.calculateWitness({ "a": a, "b": b, "c": c}, true);

        //console.log(witness);

        const arrOut = witness.slice(1, 33);
        const xor = xor3(a, b, c);

        console.log(arrOut);
        console.log(xor);

        //console.log(hash2);
        assert.deepEqual(xor, arrOut);

    }).timeout(1000000);
});
