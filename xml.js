
var fs = require('fs'),
    xml2js = require('xml2js')

var parser = new xml2js.Parser()

fs.readFile('./123.xml', function (err, data) {
    parser.parseString(data, function (err, result) {
        console.log("NF:", result['nfeProc']["NFe"][0]['infNFe'][0]['ide'][0]['nNF'][0])
        console.log('Data de Emissão:', result['nfeProc']["NFe"][0]['infNFe'][0]['ide'][0]['dhEmi'][0])
        console.log("Chave de Acesso:", (result['nfeProc']["NFe"][0]['infNFe'][0]['$']['Id']).replace("NFe", ''))
        var i
        for (i = 0; i < (result['nfeProc']["NFe"][0]['infNFe'][0]['det']).length; i++) {
            console.log('\n')
            // console.log(result['nfeProc']["NFe"][0]['infNFe'][0]['det'][i]['prod'][0])
            console.log("Produto %d:", i, result['nfeProc']["NFe"][0]['infNFe'][0]['det'][i]['prod'][0]['xProd'][0])
            console.log("SKU %d:", i, result['nfeProc']["NFe"][0]['infNFe'][0]['det'][i]['prod'][0]['cProd'][0])
            console.log("Qtd %d:", i, result['nfeProc']["NFe"][0]['infNFe'][0]['det'][i]['prod'][0]['qCom'][0], result['nfeProc']["NFe"][0]['infNFe'][0]['det'][i]['prod'][0]['uTrib'][0])

        }

    });
});
