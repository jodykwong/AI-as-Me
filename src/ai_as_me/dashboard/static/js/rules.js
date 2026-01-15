function rules() {
    return {
        selectedRule: null,
        showRollbackDialog: false,
        rollbackVersion: null,
        async init() {
            await this.loadRules();
        },
        async loadRules() {
            const res = await fetch('/api/rules');
            const data = await res.json();
            this.renderRules(data);
        },
        renderRules(rules) {
            const html = rules.map(r => `
                <div class="rule-item" onclick="selectRule('${r.name}')">
                    <h4>${r.name}</h4>
                    <p>当前版本: ${r.current_version} | 历史版本: ${r.version_count}</p>
                </div>
            `).join('');
            document.getElementById('rules-list').innerHTML = html || '<p>暂无规则</p>';
        },
        async selectRule(name) {
            this.selectedRule = name;
            const res = await fetch(`/api/rules/${name}/history`);
            const history = await res.json();
            this.renderHistory(history);
        },
        renderHistory(history) {
            const html = history.map(v => `
                <div class="version-item">
                    <span>${v.version} - ${v.timestamp}</span>
                    <button onclick="rollback('${v.version}')">回滚</button>
                </div>
            `).join('');
            document.getElementById('history-list').innerHTML = html;
        },
        rollback(version) {
            this.rollbackVersion = version;
            this.showRollbackDialog = true;
        },
        async confirmRollback() {
            await fetch(`/api/rules/${this.selectedRule}/rollback?version=${this.rollbackVersion}`, { method: 'POST' });
            this.showRollbackDialog = false;
            location.reload();
        }
    };
}

function selectRule(name) {
    Alpine.store('rules').selectRule(name);
}

function rollback(version) {
    Alpine.store('rules').rollback(version);
}
