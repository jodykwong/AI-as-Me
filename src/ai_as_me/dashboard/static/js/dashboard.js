function dashboard() {
    return {
        stats: null,
        async init() {
            await this.loadStats();
            setInterval(() => this.loadStats(), 10000);
        },
        async loadStats() {
            const res = await fetch('/api/stats');
            this.stats = await res.json();
            this.renderStats();
        },
        renderStats() {
            if (!this.stats) return;
            document.getElementById('stats-content').innerHTML = `
                <div class="stat-item">
                    <h3>${this.stats.total_inspirations}</h3>
                    <p>总灵感数</p>
                </div>
                <div class="stat-item">
                    <h3>${this.stats.mature_inspirations}</h3>
                    <p>成熟灵感</p>
                </div>
                <div class="stat-item">
                    <h3>${this.stats.total_rules}</h3>
                    <p>规则数量</p>
                </div>
            `;
        }
    };
}
