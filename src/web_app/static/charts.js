// renders a bar chart onto the given canvas element
function renderBarChart(canvasId, labels, data, colours, labelText) {

    new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: labelText,
                data: data,
                backgroundColor: colours,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 0,
                    max: 100,
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// returns colour for each quality score bar based on value
function getQualityColours(scores) {
    return scores.map(score => {
        if (score >= 75) return "#16a34a";
        if (score >= 50) return "#d97706";
        return "#dc2626";
    });
}

// returns colour for each missing perentage bar based on severity
function getMissingColours(percentages) {
    return percentages.map(pct => {
        if (pct === 100) return "#dc2626";
        if (pct > 25) return "#d97706";
        return "#2563eb";
    });
}
