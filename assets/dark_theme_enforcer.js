/**
 * MirrorMe Dark Theme Enforcer
 * Lead Developer Solution for Streamlit Chart Overrides
 */

(function() {
    'use strict';
    
    console.log('🌑 MirrorMe Dark Theme Enforcer Loaded');
    
    // ========================================
    // PLOTLY CHART DARK THEME ENFORCER
    // ========================================
    
    function enforcePlotlyDarkTheme() {
        // Find all Plotly charts
        const plotlyCharts = document.querySelectorAll('.js-plotly-plot');
        
        plotlyCharts.forEach(chart => {
            try {
                if (chart && chart.data && chart.layout) {
                    // Update layout for dark theme
                    const darkLayout = {
                        ...chart.layout,
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        font: {
                            color: '#ffffff',
                            family: 'Inter, sans-serif'
                        },
                        xaxis: {
                            ...chart.layout.xaxis,
                            gridcolor: 'rgba(255,255,255,0.2)',
                            zerolinecolor: 'rgba(255,255,255,0.3)',
                            tickcolor: '#ffffff',
                            tickfont: { color: '#ffffff' },
                            titlefont: { color: '#ffffff' }
                        },
                        yaxis: {
                            ...chart.layout.yaxis,
                            gridcolor: 'rgba(255,255,255,0.2)',
                            zerolinecolor: 'rgba(255,255,255,0.3)',
                            tickcolor: '#ffffff',
                            tickfont: { color: '#ffffff' },
                            titlefont: { color: '#ffffff' }
                        },
                        colorway: ['#667eea', '#764ba2', '#4ecdc4', '#ff6b6b', '#45b7d1']
                    };
                    
                    // Apply dark theme
                    if (window.Plotly) {
                        window.Plotly.relayout(chart, darkLayout);
                    }
                }
            } catch (error) {
                console.log('Chart theming skipped for chart:', error.message);
            }
        });
    }
    
    // ========================================
    // STATS CARD VALUE FIXER
    // ========================================
    
    function fixStatsCardValues() {
        const statsCards = document.querySelectorAll('.stats-card');
        
        statsCards.forEach(card => {
            const numberElement = card.querySelector('.stats-number');
            if (numberElement && (!numberElement.textContent || numberElement.textContent.trim() === '')) {
                // If no value, show a placeholder
                const label = card.querySelector('.stats-label');
                if (label) {
                    const labelText = label.textContent.toLowerCase();
                    if (labelText.includes('messages')) {
                        numberElement.textContent = '0';
                    } else if (labelText.includes('stage')) {
                        numberElement.textContent = '1';
                    } else if (labelText.includes('update')) {
                        numberElement.textContent = '5';
                    } else if (labelText.includes('profile')) {
                        numberElement.textContent = 'No';
                    } else {
                        numberElement.textContent = '—';
                    }
                }
            }
        });
    }
    
    // ========================================
    // CHART ERROR STATE HANDLER
    // ========================================
    
    function handleChartErrors() {
        // Find charts with "temporarily unavailable" text
        const errorTexts = Array.from(document.querySelectorAll('*')).filter(el => 
            el.textContent && el.textContent.includes('Chart temporarily unavailable')
        );
        
        errorTexts.forEach(errorElement => {
            const parent = errorElement.closest('.stPlotlyChart') || errorElement.parentElement;
            if (parent) {
                parent.innerHTML = `
                    <div class="chart-error">
                        <h3>📊 Chart Loading</h3>
                        <p>Chart will appear once you interact with the AI more.</p>
                    </div>
                `;
            }
        });
    }
    
    // ========================================
    // DYNAMIC BACKGROUND EFFECTS
    // ========================================
    
    function addDynamicEffects() {
        // Add floating particles effect
        if (!document.querySelector('.particles-bg')) {
            const particlesBg = document.createElement('div');
            particlesBg.className = 'particles-bg';
            particlesBg.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
                background-image: 
                    radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 60%, rgba(78, 205, 196, 0.05) 0%, transparent 50%);
                animation: float 15s ease-in-out infinite;
            `;
            document.body.appendChild(particlesBg);
        }
    }
    
    // ========================================
    // OBSERVER FOR DYNAMIC CONTENT
    // ========================================
    
    function setupObserver() {
        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;
            
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    for (let node of mutation.addedNodes) {
                        if (node.nodeType === 1) { // Element node
                            if (node.classList?.contains('js-plotly-plot') || 
                                node.querySelector?.('.js-plotly-plot') ||
                                node.classList?.contains('stats-card') ||
                                node.querySelector?.('.stats-card')) {
                                shouldUpdate = true;
                                break;
                            }
                        }
                    }
                }
            });
            
            if (shouldUpdate) {
                setTimeout(() => {
                    enforcePlotlyDarkTheme();
                    fixStatsCardValues();
                    handleChartErrors();
                }, 100);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // ========================================
    // INITIALIZATION
    // ========================================
    
    function initialize() {
        console.log('🚀 Initializing Dark Theme Enforcer');
        
        // Apply immediate fixes
        enforcePlotlyDarkTheme();
        fixStatsCardValues();
        handleChartErrors();
        addDynamicEffects();
        
        // Setup observer for dynamic content
        setupObserver();
        
        // Periodic enforcement (fallback)
        setInterval(() => {
            enforcePlotlyDarkTheme();
            fixStatsCardValues();
        }, 2000);
        
        console.log('✅ Dark Theme Enforcer Ready');
    }
    
    // ========================================
    // STARTUP
    // ========================================
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
    
    // Also initialize when Streamlit is ready
    window.addEventListener('load', () => {
        setTimeout(initialize, 500);
    });
    
    // Global functions for manual triggering
    window.mirrorMeTheme = {
        enforceCharts: enforcePlotlyDarkTheme,
        fixStats: fixStatsCardValues,
        handleErrors: handleChartErrors,
        reinitialize: initialize
    };
    
})();