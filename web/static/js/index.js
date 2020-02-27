// dom
let $sltFunction = $('#sltFunction')
let $sltAlgorithm = $('#sltAlgorithm')
let $btnAlgorithm = $('#btnAlgorithm')
let $logFileContainer = $('#logFileContainer')
let $btnDraw = $('#btnDraw')
let $ckbLog10 = $('#ckbLog10')
let chart = echarts.init(document.getElementById('chart'))


// global
let gAlgorithms = undefined


async function fetchFunctions(functionName) {
    return await ajaxPromise({
        url: '/get_algorithm',
        type: 'get',
        dataType: 'json',
        data: {
            functionName,
        }
    })
}

async function fetchLogFiles(functionName, algorithms) {
    return await ajaxPromise({
        url: '/get_log_file',
        type: 'get',
        dataType: 'json',
        data: {
            functionName,
            algorithms: JSON.stringify(algorithms),
        }
    })
}

async function fetchGraphData(lineSets) {
    return await ajaxPromise({
        url: '/get_graph_data',
        type: 'get',
        dataType: 'json',
        data: {
            lineSets: JSON.stringify(lineSets)
        }
    })
}

// interaction
function flushSltAlgorithm($dom, gAlgorithms) {
    $dom.empty()
    gAlgorithms.forEach(d => {
        $sltAlgorithm.append(`<option value="${d}">${d}</option>`)
    })
}

// event
$sltFunction.on('change', function () {
    let functionName = $(this).val()

    fetchFunctions(functionName).then(res => {
        gAlgorithms = res
        flushSltAlgorithm($sltAlgorithm, gAlgorithms)
    })
})

$btnAlgorithm.on('click', function () {
    let functionName = $sltFunction.val()
    let algorithms = $sltAlgorithm.val()

    fetchLogFiles(functionName, algorithms).then(res => {
        $logFileContainer.empty()
        res.forEach(d => {
            $logFileContainer.append(`
                <div class="row">
                    <p class="border border-info">
                      ${d['filename']}
                    </p>
                </div>
            `)

            let $lines = $('<div class="row"></div>')
            for (let i = 1; i <= d['numOfLines']; i++) {
                $lines.append(`
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" data-algorithm="${d['algorithm']}" data-filename="${d['filename']}" value="${i}">
                        <label class="form-check-label">${i}</label>
                    </div>
                `)
            }

            $logFileContainer.append($lines)
        })
    })
})

$btnDraw.on('click', function () {
    let data = []
    $('#logFileContainer').find('input:checked').map((i, dom) => {
        data.push({
            filename: $(dom).data('filename'),
            line: $(dom).val(),
            algorithm: $(dom).data('algorithm'),
        })
    })

    let groupBy = data => {
        let o = {}
        data.forEach(d => {
            let key = d.filename + '#' + d.algorithm
            o[key] = o[key] || []
            delete d['filename']
            delete d['algorithm']
            o[key].push(parseInt(d.line))
        })
        return o
    }

    let unpack = data => {
        let d = []
        for (let k in data) {
            let v = k.split('#')
            d.push({
                'filename': v[0],
                'algorithm': v[1],
                lines: data[k],
            })
        }
        return d
    }

    fetchGraphData(unpack(groupBy(data))).then(res => {
        chart.clear()
        let isLog10 = $ckbLog10.is(':checked')
        let data = {
            'series': [],
            'legend': []
        }
        res.forEach(d => {
            data['series'].push({
                name: d['legend'],
                data: d['data'].map(d => {
                    return isLog10 ? Math.log10(d) : d
                }),
                type: 'line',
                smooth: true,
            })
            data['legend'].push(d['legend'])
        })
        console.log(data)
        let option = {
            title: {
                text: '优化曲线'
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            legend: {
                data: data.legend,
            },
            xAxis: {
                type: 'category',
                data: range(1, 3001)
            },
            yAxis: {
                type: 'value'
            },
            series: data.series,
        }

        chart.setOption(option)
    })
})