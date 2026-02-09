class LanguageAnalyzer {
    constructor() {
        this.baseUrl = 'http://localhost:8000';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeLanguage());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveResults());
        document.getElementById('urlInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.analyzeLanguage();
        });
    }

    async analyzeLanguage() {
        const url = document.getElementById('urlInput').value.trim();

        if (!url) {
            this.showMessage('Пожалуйста, введите URL', 'error');
            return;
        }

        this.showLoading(true);
        this.hideMessage();
        this.hideResults();

        try {
            const response = await fetch(`${this.baseUrl}/api/detect-language?url=${encodeURIComponent(url)}`);

            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const data = await response.json();
            this.displayResults(data);

        } catch (error) {
            console.error('Ошибка при анализе:', error);
            this.showMessage(`Ошибка при анализе: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(data) {
        // Отображаем анализируемый URL как кликабельную ссылку
        const analyzedUrlElement = document.getElementById('analyzedUrl');
        analyzedUrlElement.innerHTML = '';

        const urlLink = document.createElement('a');
        urlLink.href = data.url;
        urlLink.target = '_blank';
        urlLink.rel = 'noopener noreferrer';
        urlLink.className = 'url-link';
        urlLink.textContent = data.url;

        analyzedUrlElement.appendChild(urlLink);

        const methodsContainer = document.getElementById('methodsContainer');
        methodsContainer.innerHTML = '';

        // Создаем карточки для каждого метода
        const methods = ['frequency_method', 'alphabet_method', 'neural_network_method'];
        const methodTitles = {
            frequency_method: '📊 Частотный анализ',
            alphabet_method: '🔤 Анализ алфавита',
            neural_network_method: '🧠 Нейросеть'
        };

        methods.forEach(method => {
            if (data[method]) {
                const methodCard = this.createMethodCard(methodTitles[method], data[method]);
                methodsContainer.appendChild(methodCard);
            }
        });

        // Сохраняем результаты для возможного сохранения в файл
        this.currentResults = data;

        // Показываем секцию с результатами
        document.getElementById('resultsSection').style.display = 'block';
    }

    createMethodCard(title, methodData) {
        const card = document.createElement('div');
        card.className = 'method-card';

        const scores = methodData.scores || {};
        const languages = Object.keys(scores);

        // Сортируем языки по убыванию score для лучшего отображения
        languages.sort((a, b) => scores[b] - scores[a]);

        card.innerHTML = `
            <div class="method-header">
                <div class="method-title">${title}</div>
                <div class="detected-language">${this.formatLanguageName(methodData.language)}</div>
            </div>
            <div class="language-scores">
                ${languages.map(language => `
                    <div class="score-item">
                        <span class="language-name">${this.formatLanguageName(language)}</span>
                        <div class="score-bar-container">
                            <div class="score-bar" style="width: ${scores[language] * 100}%"></div>
                        </div>
                        <span class="score-value">${(scores[language] * 100).toFixed(2)}%</span>
                    </div>
                `).join('')}
            </div>
        `;

        return card;
    }

    formatLanguageName(language) {
        const languageNames = {
            'russian': 'Русский',
            'german': 'Немецкий',
            'english': 'Английский',
            'french': 'Французский',
            'spanish': 'Испанский',
            'italian': 'Итальянский',
            'chinese': 'Китайский',
            'japanese': 'Японский'
        };

        return languageNames[language.toLowerCase()] ||
               language.charAt(0).toUpperCase() + language.slice(1);
    }

    async saveResults() {
        if (!this.currentResults) {
            this.showMessage('Нет результатов для сохранения', 'error');
            return;
        }

        const filename = document.getElementById('filenameInput').value.trim() || 'language_analysis';

        try {
            // Формируем URL с query параметром filename
            const url = `${this.baseUrl}/api/save?filename=${encodeURIComponent(filename)}`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentResults)
            });

            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const result = await response.json();
            this.showMessage(`Результаты успешно сохранены в файл: ${filename}`, 'success');

        } catch (error) {
            console.error('Ошибка при сохранении:', error);
            this.showMessage(`Ошибка при сохранении: ${error.message}`, 'error');
        }
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }

    showMessage(text, type) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = text;
        messageEl.className = `message ${type}`;
        messageEl.style.display = 'block';

        // Автоматически скрывать сообщение через 5 секунд
        setTimeout(() => {
            this.hideMessage();
        }, 5000);
    }

    hideMessage() {
        document.getElementById('message').style.display = 'none';
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
    }
}

// Инициализация приложения когда DOM загружен
document.addEventListener('DOMContentLoaded', () => {
    new LanguageAnalyzer();
});