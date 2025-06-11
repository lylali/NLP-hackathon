document.addEventListener('DOMContentLoaded', () => {
    // --- Element Selectors ---
    const searchForm = document.getElementById('search-form');
    const topicInput = document.getElementById('topic-input');
    const resultsDashboard = document.getElementById('results-dashboard');
    const loader = document.getElementById('loader');
    const resultsContent = document.getElementById('results-content');
    const newsCardsContainer = document.getElementById('news-cards-container');
    const globalConsensusEl = document.getElementById('global-consensus');
    const keyDivergencesEl = document.getElementById('key-divergences');
    const worldMap = document.getElementById('world-map');
    
    // --- Comparison Modal Selectors ---
    const modalOverlay = document.getElementById('comparison-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const comparisonPane1 = document.getElementById('comparison-pane-1');
    const comparisonPane2 = document.getElementById('comparison-pane-2');

    // --- State Variables ---
    let fullReportData = []; // Store the full data to access for comparison
    let comparisonSelections = []; // Array to hold the 2 reports to compare

    // --- Mock Data: Replace with your real API call ---
    const mockData = {
        analysis: { /* ... (same as before) ... */ },
        countryReports: [
            { country: "United States", countryCode: "USA", flag: "🇺🇸", headline: "Summit Heralds New Era of Economic Policy and Global Trade", summary: "American media frames the summit's success through an economic lens, detailing new trade agreements and predicting a positive impact on the domestic market. The focus is on policy wins for the administration.", sentiment: { score: 78, label: "Positive" }, keywords: ["Economy", "Trade Deals", "Policy", "Market Growth"], link: "#" },
            { country: "United Kingdom", countryCode: "GBR", flag: "🇬🇧", headline: "Diplomatic Triumph: UK Plays Key Role in Brokering International Accord", summary: "British outlets highlight the UK's central diplomatic role in negotiations. The narrative emphasizes statesmanship and the strengthening of international alliances post-Brexit.", sentiment: { score: 85, label: "Positive" }, keywords: ["Diplomacy", "Alliance", "Negotiation", "Global Britain"], link: "#" },
            { country: "China", countryCode: "CHN", flag: "🇨🇳", headline: "Global Summit Concludes with Call for Multilateralism, Rejects Unilateral Actions", summary: "Chinese state media reports on the summit as a victory for multilateral cooperation, implicitly critiquing unilateralism. The focus is on shared development and respect for national sovereignty.", sentiment: { score: 60, label: "Neutral" }, keywords: ["Multilateralism", "Cooperation", "Sovereignty", "Development"], link: "#" },
            { country: "India", countryCode: "IND", flag: "🇮🇳", headline: "Leaders Address Climate and Security, But Financial Commitments Remain Vague", summary: "Indian reporting takes a more cautious tone, acknowledging the progress on climate change but questioning the lack of concrete financial aid for developing nations. The security implications for the region are a key focus.", sentiment: { score: 45, label: "Negative" }, keywords: ["Climate Change", "Financial Aid", "Security", "Developing Nations"], link: "#" },
            { country: "Japan", countryCode: "JPN", flag: "🇯🇵", headline: "Technological Cooperation at the Forefront of New Global Partnership", summary: "Japanese news highlights agreements on technology sharing and research collaboration. The reporting is optimistic about how this will drive future innovation and economic stability.", sentiment: { score: 75, label: "Positive" }, keywords: ["Technology", "Innovation", "R&D", "Partnership"], link: "#" }
        ]
    };
    mockData.analysis.globalConsensus = "The event is widely seen as a significant diplomatic achievement, fostering international cooperation. Most reports emphasize the positive outcomes and future commitments made by world leaders.";
    mockData.analysis.keyDivergences = "Reporting from Western nations (e.g., USA, GBR) focuses on the economic implications and policy changes. In contrast, reports from Eastern nations (e.g., China, India) highlight the geopolitical shifts and regional impacts. Sentiment varies, with some outlets expressing skepticism about long-term enforcement.";


    // --- Event Listeners ---
    searchForm.addEventListener('submit', handleSearch);
    
    // Use event delegation for dynamically created compare buttons
    newsCardsContainer.addEventListener('click', handleCardClick);

    // Modal close events
    modalCloseBtn.addEventListener('click', closeComparisonModal);
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeComparisonModal();
        }
    });

    // --- Core Functions ---
    function handleSearch(e) {
        e.preventDefault();
        const topic = topicInput.value.trim();
        if (!topic) return;

        resultsDashboard.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        loader.style.display = 'block';
        newsCardsContainer.innerHTML = '';
        closeComparisonModal(); // Reset any existing comparison

        fetchNewsData(topic)
            .then(data => {
                loader.style.display = 'none';
                fullReportData = data.countryReports; // Store data
                renderDashboard(data);
                resultsContent.classList.remove('hidden');
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                loader.innerText = "Sorry, an error occurred. Please try again.";
            });
    }

    function fetchNewsData(topic) {
        console.log(`Fetching data for topic: ${topic}`);
        return new Promise((resolve) => {
            setTimeout(() => resolve(mockData), 2500);
        });
    }

    // --- Rendering Functions ---
    function renderDashboard(data) {
        globalConsensusEl.textContent = data.analysis.globalConsensus;
        keyDivergencesEl.textContent = data.analysis.keyDivergences;

        data.countryReports.forEach((report, index) => {
            const card = createNewsCard(report);
            card.style.animationDelay = `${index * 150}ms`;
            newsCardsContainer.appendChild(card);
        });
        
        setupMapInteractions();
    }

    function createNewsCard(report) {
        const sentimentClass = report.sentiment.label.toLowerCase();
        const cardElement = document.createElement('div');
        cardElement.className = `news-card ${sentimentClass}`;
        cardElement.dataset.country = report.countryCode;

        // UPDATED: Now includes a .card-actions wrapper and a compare button
        cardElement.innerHTML = `
            <div class="card-header">
                <span class="flag">${report.flag}</span>
                <h4>${report.country}</h4>
            </div>
            <p class="card-headline">${report.headline}</p>
            <p class="card-summary">${report.summary}</p>
            
            <div class="sentiment-analysis">
                <div class="sentiment-label">
                    <span>Sentiment</span>
                    <span style="color: var(--sentiment-${sentimentClass})">${report.sentiment.label} (${report.sentiment.score}%)</span>
                </div>
                <div class="sentiment-bar-container">
                    <div class="sentiment-bar ${sentimentClass}" style="width: ${report.sentiment.score}%"></div>
                </div>
            </div>

            <div class="keywords">
                ${report.keywords.map(kw => `<span class="keyword-tag">${kw}</span>`).join('')}
            </div>

            <div class="card-actions">
                <div class="read-more">
                    <a href="${report.link}" target="_blank" rel="noopener noreferrer">Read Source →</a>
                </div>
                <button class="compare-btn" data-country="${report.countryCode}">Compare</button>
            </div>
        `;
        return cardElement;
    }

    // --- Comparison Logic ---
    function handleCardClick(e) {
        if (e.target.classList.contains('compare-btn')) {
            const button = e.target;
            const countryCode = button.dataset.country;
            const card = button.closest('.news-card');

            const isAlreadySelected = comparisonSelections.some(sel => sel.countryCode === countryCode);

            if (isAlreadySelected) {
                // Deselect the item
                comparisonSelections = comparisonSelections.filter(sel => sel.countryCode !== countryCode);
                card.classList.remove('comparing');
                button.textContent = 'Compare';
            } else if (comparisonSelections.length < 2) {
                // Select the item
                const report = fullReportData.find(r => r.countryCode === countryCode);
                comparisonSelections.push(report);
                card.classList.add('comparing');
                button.textContent = 'Comparing...';

                if (comparisonSelections.length === 2) {
                    showComparisonModal();
                }
            }
        }
    }

    function showComparisonModal() {
        const [report1, report2] = comparisonSelections;
        populateComparisonPane(comparisonPane1, report1);
        populateComparisonPane(comparisonPane2, report2);
        modalOverlay.classList.remove('hidden');
    }
    
    function populateComparisonPane(pane, report) {
        const sentimentClass = report.sentiment.label.toLowerCase();
        pane.innerHTML = `
            <h4><span class="flag">${report.flag}</span> ${report.country}</h4>
            <p class="card-headline">${report.headline}</p>
            <p class="card-summary">${report.summary}</p>
            
            <div class="sentiment-analysis">
                <div class="sentiment-label">
                    <span>Sentiment</span>
                    <span style="color: var(--sentiment-${sentimentClass})">${report.sentiment.label} (${report.sentiment.score}%)</span>
                </div>
                <div class="sentiment-bar-container">
                    <div class="sentiment-bar ${sentimentClass}" style="width: ${report.sentiment.score}%"></div>
                </div>
            </div>
            <div class="keywords">
                ${report.keywords.map(kw => `<span class="keyword-tag">${kw}</span>`).join('')}
            </div>
        `;
    }

    function closeComparisonModal() {
        modalOverlay.classList.add('hidden');
        comparisonSelections = []; // Reset selections
        
        // Reset all card styles and button texts
        document.querySelectorAll('.news-card.comparing').forEach(card => {
            card.classList.remove('comparing');
            card.querySelector('.compare-btn').textContent = 'Compare';
        });
    }

    // --- Map Interactivity ---
    function setupMapInteractions() {
        const cards = document.querySelectorAll('.news-card');
        const mapDots = worldMap.querySelectorAll('circle, path');

        // Clear previous event listeners to avoid duplicates if re-rendering
        // (A more robust solution would involve a proper component framework)

        cards.forEach(card => {
            const countryCode = card.dataset.country;
            const correspondingDot = worldMap.querySelector(`[data-country="${countryCode}"]`);

            card.addEventListener('mouseover', () => {
                card.classList.add('highlight');
                if (correspondingDot) correspondingDot.classList.add('active');
            });
            card.addEventListener('mouseout', () => {
                card.classList.remove('highlight');
                if (correspondingDot) correspondingDot.classList.remove('active');
            });
        });

        mapDots.forEach(dot => {
            const countryCode = dot.dataset.country;
            const correspondingCard = document.querySelector(`.news-card[data-country="${countryCode}"]`);
            
            dot.addEventListener('mouseover', () => {
                if (correspondingCard) {
                    correspondingCard.classList.add('highlight');
                    correspondingCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                 dot.classList.add('active');
            });
             dot.addEventListener('mouseout', () => {
                if (correspondingCard) correspondingCard.classList.remove('highlight');
                 dot.classList.remove('active');
            });
        });
    }
});
