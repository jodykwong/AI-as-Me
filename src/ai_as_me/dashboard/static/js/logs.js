function logs() {
    return {
        level: '',
        keyword: '',
        logs: [],
        eventSource: null,
        init() {
            this.connect();
        },
        connect() {
            const url = `/api/logs/stream${this.level ? '?level=' + this.level : ''}`;
            this.eventSource = new EventSource(url);
            
            this.eventSource.onmessage = (event) => {
                const log = JSON.parse(event.data);
                this.addLog(log);
            };
        },
        reconnect() {
            if (this.eventSource) this.eventSource.close();
            this.clearLogs();
            this.connect();
        },
        addLog(log) {
            this.logs.push(log);
            if (this.logs.length > 1000) this.logs.shift();
            this.renderLogs();
        },
        renderLogs() {
            const filtered = this.keyword 
                ? this.logs.filter(l => JSON.stringify(l).includes(this.keyword))
                : this.logs;
            
            const html = filtered.map(log => {
                const color = {
                    ERROR: '#e74c3c',
                    WARNING: '#f39c12',
                    INFO: '#3498db',
                    DEBUG: '#95a5a6'
                }[log.level] || '#d4d4d4';
                
                return `<div style="color: ${color}">[${log.timestamp}] ${log.level} - ${log.message}</div>`;
            }).join('');
            
            document.getElementById('log-viewer').innerHTML = html;
        },
        filterLogs() {
            this.renderLogs();
        },
        clearLogs() {
            this.logs = [];
            document.getElementById('log-viewer').innerHTML = '';
        }
    };
}
