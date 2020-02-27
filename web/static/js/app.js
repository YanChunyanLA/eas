const range = (start, end) => {
    let o = []
    for (let i = start; i < end; i++) {
        o.push(i)
    }
    return o
}

// api
const ajaxPromise = params => {
    return new Promise((resolve, reject) => {
        $.ajax({
            ...params,
            success: res => {
                console.debug(res)
                resolve(res)
            },
            error: err => {
                console.error(err)
                reject(err)
            }
        })
    })
}