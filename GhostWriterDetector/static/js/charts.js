document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

function initializeCharts() {
    const chartElements = document.querySelectorAll('[data-chart-type]');
    
    chartElements.forEach(element => {
        const type = element.getAttribute('data-chart-type');
        const data = element.getAttribute('data-chart-data');
        
        if (type && data) {
            try {
                const chartData = JSON.parse(data);
                createChart(element, type, chartData);
            } catch(e) {
                console.log('Chart data parse error');
            }
        }
    });
}

function createChart(container, type, data) {
    const ctx = container.getContext ? container.getContext('2d') : null;
    
    if (!ctx) return;
    
    let config = {};
    
    switch(type) {
        case 'bar':
            config = createBarChart(data);
            break;
        case 'line':
            config = createLineChart(data);
            break;
        case 'doughnut':
            config = createDoughnutChart(data);
            break;
        default:
            return;
    }
    
    new Chart(ctx, config);
}

function createBarChart(data) {
    return {
        type: 'bar',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: data.label || 'Data',
                data: data.values || [],
                backgroundColor: [
                    'rgba(99, 102, 241, 0.6)',
                    'rgba(16, 185, 129, 0.6)',
                    'rgba(239, 68, 68, 0.6)',
                    'rgba(245, 158, 11, 0.6)',
                    'rgba(139, 92, 246, 0.6)',
                    'rgba(6, 182, 212, 0.6)',
                ],
                borderColor: [
                    'rgba(99, 102, 241, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(139, 92, 246, 1)',
                    'rgba(6, 182, 212, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#e5e7eb' }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#e5e7eb' },
                    grid: { color: 'rgba(55, 65, 81, 0.3)' }
                },
                x: {
                    ticks: { color: '#e5e7eb' },
                    grid: { color: 'rgba(55, 65, 81, 0.3)' }
                }
            }
        }
    };
}

function createLineChart(data) {
    return {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: data.label || 'Data',
                data: data.values || [],
                borderColor: 'rgba(99, 102, 241, 1)',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(99, 102, 241, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#e5e7eb' }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#e5e7eb' },
                    grid: { color: 'rgba(55, 65, 81, 0.3)' }
                },
                x: {
                    ticks: { color: '#e5e7eb' },
                    grid: { color: 'rgba(55, 65, 81, 0.3)' }
                }
            }
        }
    };
}

function createDoughnutChart(data) {
    return {
        type: 'doughnut',
        data: {
            labels: data.labels || [],
            datasets: [{
                data: data.values || [],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(99, 102, 241, 0.8)',
                ],
                borderColor: '#1f2937',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#e5e7eb' }
                }
            }
        }
    };
}

// Utility function to format numbers
function formatNumber(num) {
    return num.toFixed(2);
}

// Utility function to get color based on score
function getScoreColor(score) {
    if (score > 70) return '#10b981';
    if (score > 50) return '#f59e0b';
    if (score > 30) return '#ef4444';
    return '#6b7280';
}
