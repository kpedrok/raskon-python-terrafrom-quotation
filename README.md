# raskon-quotation

install pandas


http://simp.ly/publish/MMkKpX


readme

            const priceQuery: EntityDataFilter = {
                filter: {
                    OR: innerFilter
                }
            }
            this.entityDataService.report('custos', priceQuery).then((costs) => {
                this.results.forEach((row) => {
                    const cost = costs.find((c) => c.tarifa == row.tarifa && c.metodo == row.metodo && c.uf == row.uf)
                    if (cost) {
                        let max = 9999
                        for (let prop in cost) {
                            if (!isNaN(+prop)) {
                                if (+prop < max && +prop >= this.peso * 1000) {
                                    row.cost = cost[prop]
                                    row.grams = prop
                                    max = +prop
                                }
                            }