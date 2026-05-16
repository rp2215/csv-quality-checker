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

// render a half-doughnut guage showing overall quality scores
function renderGaugeChart(canvasId, score) {

    // pick colour based on score
    let colour;
    if (score >= 75) colour = "#16a34a";       // green — good
    else if (score >= 50) colour = "#d97706";  // amber — needs attention
    else colour = "#dc2626";                    // red — poor

    // draws the score number inside gauge arc
    const centreTextPlugin = {
        id: "centreText",
        afterDraw(chart) {
            const { ctx, chartArea: { top, left, width, height } } = chart;
            ctx.save();

            // position text at bottom center of half circle
            const centerX = left + width / 2;
            const centerY = top + height / 0.9;

            ctx.font = "bold 32px Arial";
            ctx.fillStyle = colour;
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(score + "%", centerX, centerY);

            ctx.restore();
        }
    };

    new Chart(document.getElementById(canvasId), {
        type: "doughnut",
        data: {
            datasets: [{
                // first segment is score, second is the empty remainder
                data: [score, 100 - score],
                backgroundColor: [colour, "#e5e7eb"],
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            rotation: -90,       // start arc from the left side
            circumference: 180,  // only draw half the circle
            cutout: "75%",       // how thick the ring is
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false },
            }
        },
        plugins: [centreTextPlugin]
    });
}

