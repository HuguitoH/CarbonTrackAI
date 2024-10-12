// Calendar Heatmap Configuration
document.addEventListener('DOMContentLoaded', function() {
    const heatmap = new CalHeatMap();
    heatmap.init({
        itemSelector: "#calendar-widget",
        domain: "month",             // Define domain as months
        subDomain: "day",            // Subdomain is day (each square is a day)
        range: 3,                    // Show last 3 months
        cellSize: 20,                // Size of each day cell
        domainGutter: 10,            // Space between months
        legend: [2, 4, 6, 8, 10],    // Define color steps for the heatmap
        data: getActivityData(),      // Data source (JSON or function)
        start: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000),  // Start date: 90 days ago
        tooltip: true,                // Display tooltips
        itemName: ["activity", "activities"]
    });

    // Dummy function to return sample activity data (for demo purposes)
    function getActivityData() {
        const today = new Date();
        const startDate = new Date(today.getFullYear(), today.getMonth() - 2, 1);
        const endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);

        let data = {};
        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
            const timestamp = Math.floor(d.getTime() / 1000);  // Convert to UNIX timestamp
            data[timestamp] = Math.floor(Math.random() * 10);  // Random activities count
        }
        return data;
    }
});
