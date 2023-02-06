var fastFile = require('fastfile');

const r1csfile = require("r1csfile");
var r1csName = "constraints/main.r1cs";
var symName =  "constraints/main.sym";

//const cir = r1csfile.readR1cs(r1csName, true, true, false);

async function map(symFileName){
    const fd = await fastFile.readExisting(symFileName);
    const buff = await fd.read(fd.totalSize);
    const symsStr = new TextDecoder("utf-8").decode(buff);
    const lines = symsStr.split("\n");
    
    var varIdx2Name = [ "one" ];
    
    for (let i=0; i<lines.length; i++) {
        const arr = lines[i].split(",");
        if (arr.length!=4) continue;
        if (varIdx2Name[arr[1]]) {
            varIdx2Name[arr[1]] += "|" + arr[3];
        } else {
            varIdx2Name[arr[1]] = arr[3];
        }
    }
    await fd.close();

    var data = {
        map: varIdx2Name
    };

    var jsonData = JSON.stringify(data);


    var fs = require('fs');
    fs.writeFile("data/map.json", jsonData, function(err) {
        if (err) {
            console.log(err);
        }
    });
}

map(symName);
