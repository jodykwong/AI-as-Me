function inspirations() {
    return {
        status: '',
        minMaturity: 0,
        chart: null,
        async init() {
            await this.loadInspirations();
            this.initChart();
        },
        async loadInspirations() {
            const params = new URLSearchParams();
            if (this.status) params.append('status', this.status);
            if (this.minMaturity > 0) params.append('min_maturity', this.minMaturity);
            
            const res = await fetch(`/api/inspirations?${params}`);
            const data = await res.json();
            this.renderList(data);
            this.updateChart(data);
        },
        renderList(inspirations) {
            const html = inspirations.map(i => `
                <div class="inspiration-item">
                    <h4>${i.content}</h4>
                    <p>成熟度: ${(i.maturity * 100).toFixed(0)}% | 状态: ${i.status}</p>
                    <button onclick="convertInspiration('${i.id}', 'rule')">转为规则</button>
                </div>
            `).join('');
            document.getElementById('inspirations-list').innerHTML = html || '<p>暂无灵感</p>';
        },
        initChart() {
            const ctx = document.getElementById('heatmapChart');
            this.chart = new Chart(ctx, {
                type: 'bar',
                data: { labels: [], datasets: [{ label: '成熟度', data: [] }] }
            });
        },
        updateChart(data) {
            if (!this.chart) return;
            this.chart.data.labels = data.map(i => i.id.slice(0, 8));
            this.chart.data.datasets[0].data = data.map(i => i.maturity);
            this.chart.update();
        }
    };
}

async function convertInspiration(id, type) {
    await fetch(`/api/inspirations/${id}/convert?target_type=${type}`, { method: 'POST' });
    location.reload();
}
