class Api {
    constructor(url, headers) {
        this._url = url
        this._headers = headers
    }

    checkResponse(res) {
        return new Promise((resolve, reject) => {
            if (res.status === 204) {
                return resolve(res)
            }
            const func = res.status < 400 ? resolve : reject
            res.json().then(data => func(data))
        })
    }

    signin({ username, password }) {
        return fetch(
            '/jwt/login/',
            {
                method: 'POST',
                headers: this._headers,
                body: JSON.stringify({
                    username, password
                })
            }
        ).then(this.checkResponse)
    }
}

export default new Api(process.env.API_URL || 'http://localhost', { 'content-type': 'application/json' })