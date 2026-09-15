// ============================================
// SALES ANALYTICS CHARTS
// ============================================


// ============================================
// MONTHLY SALES CHART
// ============================================

const monthlySalesCanvas = document.getElementById("monthlySalesChart");

if (monthlySalesCanvas) {

    new Chart(monthlySalesCanvas, {

        type: "line",

        data: {

            labels: [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June"
            ],

            datasets: [

                {
                    label: "Revenue",

                    data: [
                        110000,
                        93000,
                        150000,
                        140000,
                        125000,
                        110000
                    ],

                    borderWidth: 2,

                    tension: 0.3,

                    fill: false
                }

            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: true
                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(value) {
                            return "₹" + value.toLocaleString();
                        }

                    }

                }

            }

        }

    });

}