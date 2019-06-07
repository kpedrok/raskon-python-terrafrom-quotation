main();

async function main() {
    var um = await funcaoUm();
    var dois = await funcaoDois();
    var tres = await funcaoTres();

    console.log(um);
    console.log(dois);
    console.log(tres);
}


async function funcaoUm() {
    return "Um";
}

async function funcaoDois() {
    return "Dois";
}

async function funcaoTres() {
    return "Três";
}
