interface Context {
    context: string
    entries: number
    lines: number
}

interface Entry {
    id: number
    source: string
    v6: boolean
    received_at: number
    context: string
    line: number
    data: string
}

interface Line {
    context: string
    line: number
    entry: Entry
    selected_at: number
}

interface Summary {
    lines: Array<Entry>
    missing: Array<number>
}

type Export = Array<string>

export default class Api {
    private url: string;

    constructor(url: string) {
        this.url = url;
    }

    protected handleResponse<T>(promise: Promise<Response>): Promise<T> {
        return new Promise<T>((resolve, reject) => {
            promise.then((response: Response) => {
                if (!response.ok) {
                    reject("No connection to the API")
                }
                response.json().then((json: { [index: string]: any }) => {
                    if (json["ok"] !== true) {
                        reject(new Error(json["error"] || "Invalid response"));
                    } else {
                        console.log(json["data"]);
                        resolve(json["data"]);
                    }
                }).catch(reject)
            }).catch(reject)
        })
    }

    public listContexts() {
        return this.handleResponse<Array<Context>>(fetch(`${this.url}/dora/context`))
    }

    public getSummary(context: string) {
        return this.handleResponse<Summary>(fetch(`${this.url}/dora/entry/${encodeURIComponent(context)}/summary`))
    }

    public getEntries(context: string) {
        return this.handleResponse<Summary>(fetch(`${this.url}/dora/entry/${encodeURIComponent(context)}`))
    }

    public getEntriesForLine(context: string, line: number) {
        return this.handleResponse<Summary>(fetch(`${this.url}/dora/entry/${encodeURIComponent(context)}?line=${encodeURIComponent(line)}`))
    }

    public setLine(context: string, line: number, id: number) {
        return this.handleResponse<null>(fetch(`${this.url}/dora/line`, {
            method: "POST",
            body: JSON.stringify({
                context,
                line,
                id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }))
    }

    public autoselectLines(context: string) {
        return this.handleResponse<null>(fetch(`${this.url}/dora/line/auto`, {
            method: "POST",
            body: JSON.stringify({
                context,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }))
    }

    public exportEntry(context: string, decoded: boolean = true) {
        const response = this.handleResponse<Export>(fetch(`${this.url}/dora/entry/${encodeURIComponent(context)}/export`))
        if (!decoded) return response;
        return response.then(data => {
            return data.reduce((lines: string, line: string) => {
            try {
                return lines + atob(line);
            } catch (e) {
                return lines;
            }
        }, '');
        })
    }

    public generateContext() {
        return this.handleResponse<null>(fetch(`${this.url}/swiper/context`))
    }

    public generatePayload(context: string, tool: string, command: string) {
        return this.handleResponse<null>(fetch(`${this.url}/swiper/payload`, {
            method: "POST",
            body: JSON.stringify({
                context,
                tool,
                command,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }))
    }
}
