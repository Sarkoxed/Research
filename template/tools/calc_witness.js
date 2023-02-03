async calculateWTNSBin(witness) {
    let n32 = 
    let withnessSize = witness.length
    const buff32 = new Uint32Array(this.witnessSize*this.n32+this.n32+11);
	const buff =   new  Uint8Array(buff32.buffer);
  
	//"wtns"
	buff[0] = "w".charCodeAt(0)
	buff[1] = "t".charCodeAt(0)
	buff[2] = "n".charCodeAt(0)
	buff[3] = "s".charCodeAt(0)

	//version 2
	buff32[1] = 2;

	//number of sections: 2
	buff32[2] = 2;

	//id section 1
	buff32[3] = 1;

	const n8 = this.n32*4;
	//id section 1 length in 64bytes
	const idSection1length = 8 + n8;
	const idSection1lengthHex = idSection1length.toString(16);
        buff32[4] = parseInt(idSection1lengthHex.slice(0,8), 16);
        buff32[5] = parseInt(idSection1lengthHex.slice(8,16), 16);

	//this.n32
	buff32[6] = n8;

	//prime number
	this.instance.exports.getRawPrime();

	var pos = 7;
        for (let j=0; j<this.n32; j++) {
	    buff32[pos+j] = this.instance.exports.readSharedRWMemory(j);
        }
	pos += this.n32;

	// witness size
	buff32[pos] = this.witnessSize;
	pos++;

	//id section 2
	buff32[pos] = 2;
	pos++;

	// section 2 length
	const idSection2length = n8*this.witnessSize;
	const idSection2lengthHex = idSection2length.toString(16);
        buff32[pos] = parseInt(idSection2lengthHex.slice(0,8), 16);
        buff32[pos+1] = parseInt(idSection2lengthHex.slice(8,16), 16);

	pos += 2;
        for (let i=0; i<this.witnessSize; i++) {
            this.instance.exports.getWitness(i);
            for (let j=0; j<this.n32; j++) {
		buff32[pos+j] = this.instance.exports.readSharedRWMemory(j);
            }
	    pos += this.n32;
        }

	return buff;
    }

}
