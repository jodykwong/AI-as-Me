function stats() {
    return {
        charts: {},
        async init() {
            await this.loadStats();
        },
        async loadStats() {
            const res = await fetch('/api/stats');
            const data = await res.json();
            this.renderCharts(data);
        },
        renderCharts(data) {
            // 应用频率
            const freqCtx = document.getElementById('frequencyChart');
            this.charts.frequency = new Chart(freqCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.rule_applications),
                    datasets: [{
                        label: '应用次数',
                        data: Object.values(data.rule_applications),
                        backgroundColor: '#3498db'
                    }]
                }
            });

            // 效果评分
            const effCtx = document.getElementById('effectivenessChart');
            this.charts.effectiveness = new Chart(effCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.effectiveness_scores),
                    datasets: [{
                        label: '效果评分',
                        data: Object.values(data.effectiveness_scores),
                        backgroundColor: '#2ecc71'
                    }]
                },
                options: { scales: { y: { max: 1 } } }
            });

            // 趋势图
            const trendCtx = document.getElementById('trendChart');
            this.charts.trend = new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: '灵感成熟度',
                        data: [0.3, 0.5, 0.7, 0.8],
                        borderColor: '#e74c3c',
                        fill: false
                    }]
                }
            });
        }
    };
}
