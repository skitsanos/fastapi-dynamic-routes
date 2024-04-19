class ReconnectingWebSocket {
    constructor(url, protocols = [], options = {}) {
        this.url = url;
        this.protocols = protocols;
        this.options = options;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || Infinity;
        this.reconnectInterval = options.reconnectInterval || 1000;
        this.reconnectDecay = options.reconnectDecay || 1.5;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url, this.protocols);
        this.ws.onopen = this.onOpen.bind(this);
        this.ws.onclose = this.onClose.bind(this);
        this.ws.onmessage = this.options.onmessage;
        this.ws.onerror = this.options.onerror;
    }

    onOpen() {
        console.log('WebSocket connection opened');
        this.reconnectAttempts = 0;
        if (this.options.onopen) {
            this.options.onopen();
        }
    }

    onClose(event) {
        console.log('WebSocket connection closed', event);
        this.reconnect();
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                console.log(`Attempting to reconnect (${this.reconnectAttempts})`);
                this.connect();
            }, this.reconnectInterval * Math.pow(this.reconnectDecay, this.reconnectAttempts));
        } else {
            console.log('Maximum reconnect attempts reached');
            if (this.options.onmaximumreconnectattempts) {
                this.options.onmaximumreconnectattempts();
            }
        }
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(data);
        } else {
            console.error('WebSocket is not open');
        }
    }

    close(code = 1000, reason = '') {
        if (this.ws) {
            this.ws.close(code, reason);
        }
    }
}