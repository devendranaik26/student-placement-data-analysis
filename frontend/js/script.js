
const API_BASE = "http://127.0.0.1:5000";

// Load Chart.js and its data labels plugin
function loadChartLibrary() {
    return new Promise((resolve, reject) => {
        if (window.Chart && window.ChartDataLabels) {
            resolve();
            return;
        }

        function loadLabelsPlugin() {
            if (window.ChartDataLabels) {
                Chart.register(ChartDataLabels);
                resolve();
                return;
            }

            const pluginScript = document.createElement("script");
            pluginScript.src =
                "https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2";

            pluginScript.onload = () => {
                Chart.register(ChartDataLabels);
                resolve();
            };

            pluginScript.onerror = () =>
                reject(new Error("Could not load chart labels plugin."));

            document.head.appendChild(pluginScript);
        }

        if (window.Chart) {
            loadLabelsPlugin();
            return;
        }

        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/chart.js";

        script.onload = loadLabelsPlugin;
        script.onerror = () =>
            reject(new Error("Could not load Chart.js."));

        document.head.appendChild(script);
    });
}

// Shared labels for pie charts
function getPieChartPlugins() {
    return {
        legend: {
            position: "bottom"
        },

        tooltip: {
            callbacks: {
                label: function (context) {
                    const value = Number(context.raw || 0);
                    const total = context.dataset.data.reduce(
                        (sum, item) => sum + Number(item || 0), 0
                    );

                    const percentage = total > 0
                        ? ((value / total) * 100).toFixed(1)
                        : "0.0";

                    return `${context.label}: ${value} students (${percentage}%)`;
                }
            }
        },

        datalabels: {
            color: "#ffffff",
            font: {
                weight: "bold",
                size: 13
            },
            textAlign: "center",

            formatter: function (value, context) {
                const total = context.dataset.data.reduce(
                    (sum, item) => sum + Number(item || 0), 0
                );

                if (total === 0 || Number(value) === 0) {
                    return "";
                }

                const percentage = (
                    Number(value) / total * 100
                ).toFixed(1);

                return `${value}\n${percentage}%`;
            }
        }
    };
}

// Shared labels for bar charts
function getBarChartPlugins(formatter) {
    return {
        legend: {
            position: "bottom"
        },

        datalabels: {
            color: "#334155",
            anchor: "end",
            align: "end",
            clamp: false,
            clip: false,
            offset: 4,

            font: {
                weight: "bold",
                size: 11
            },

            formatter: formatter
        }
    };
}

// Dashboard summary cards
async function loadDashboardSummary() {
    try {
        const response = await fetch(`${API_BASE}/api/departments`);

        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid department data received");
        }

        const departments = result.data;

        const totalStudents = departments.reduce(
            (sum, dept) => sum + Number(dept.total_students || 0), 0
        );

        const placedStudents = departments.reduce(
            (sum, dept) => sum + Number(dept.placed_students || 0), 0
        );

        const unplacedStudents = totalStudents - placedStudents;

        const placementRate = totalStudents > 0
            ? placedStudents / totalStudents * 100
            : 0;

        document.getElementById("total-students").textContent =
            totalStudents;

        document.getElementById("placed-students").textContent =
            placedStudents;

        document.getElementById("placement-rate").textContent =
            `${placementRate.toFixed(1)}%`;

        document.getElementById("unplaced-students").textContent =
            unplacedStudents;

    } catch (error) {
        console.error("Dashboard summary error:", error);
    }
}

// Dashboard placement status pie chart
async function loadPlacementStatusChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/departments`);
        if (!response.ok) throw new Error("Could not load department data.");

        const result = await response.json();
        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid department data.");
        }

        const total = result.data.reduce(
            (sum, dept) => sum + Number(dept.total_students || 0), 0
        );

        const placed = result.data.reduce(
            (sum, dept) => sum + Number(dept.placed_students || 0), 0
        );

        const canvas = document.getElementById("placementStatusChart");
        if (!canvas) return;

        new Chart(canvas, {
            type: "pie",
            data: {
                labels: ["Placed Students", "Not Yet Placed"],
                datasets: [{
                    data: [placed, total - placed],
                    backgroundColor: ["#16a34a", "#f59e0b"],
                    borderColor: "#ffffff",
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500
                },
                plugins: getPieChartPlugins()
            }
        });

    } catch (error) {
        console.error("Placement pie chart error:", error);
    }
}

// Dashboard company distribution pie chart
async function loadCompanyDistributionChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/companies`);
        if (!response.ok) throw new Error("Could not load company data.");

        const result = await response.json();
        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid company data.");
        }

        const canvas = document.getElementById("companyDistributionChart");
        if (!canvas) return;

        const companies = result.data;

        new Chart(canvas, {
            type: "pie",
            data: {
                labels: companies.map(company => company.company),
                datasets: [{
                    data: companies.map(
                        company => Number(company.students_placed || 0)
                    ),
                    backgroundColor: [
                        "#2563eb", "#7c3aed", "#0891b2",
                        "#ea580c", "#db2777", "#16a34a"
                    ],
                    borderColor: "#ffffff",
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500
                },
                plugins: getPieChartPlugins()
            }
        });

    } catch (error) {
        console.error("Company pie chart error:", error);
    }
}

// Department summary cards
async function loadDepartmentSummary() {
    try {
        const response = await fetch(`${API_BASE}/api/departments`);
        if (!response.ok) throw new Error("Failed to load department data.");

        const result = await response.json();
        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid department data.");
        }

        const departments = result.data;

        const totalStudents = departments.reduce(
            (sum, dept) => sum + Number(dept.total_students || 0), 0
        );

        const placedStudents = departments.reduce(
            (sum, dept) => sum + Number(dept.placed_students || 0), 0
        );

        const rate = totalStudents > 0
            ? placedStudents / totalStudents * 100
            : 0;

        document.getElementById("total-departments").textContent =
            departments.length;

        document.getElementById("department-total-students").textContent =
            totalStudents;

        document.getElementById("department-placed-students").textContent =
            placedStudents;

        document.getElementById("department-placement-rate").textContent =
            `${rate.toFixed(1)}%`;

    } catch (error) {
        console.error("Department summary error:", error);
    }
}

// Animated department placement rate bar chart
async function loadDepartmentPlacementRateChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/departments`);
        if (!response.ok) throw new Error("Could not load department data.");

        const result = await response.json();
        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid department data.");
        }

        const departments = result.data;
        const canvas = document.getElementById(
            "departmentPlacementRateChart"
        );

        if (!canvas) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: departments.map(dept => dept.department),
                datasets: [{
                    label: "Placement Rate (%)",
                    data: departments.map(
                        dept => Number(dept.placement_rate || 0)
                    ),
                    backgroundColor: [
                        "#2563eb", "#7c3aed", "#0891b2",
                        "#ea580c", "#db2777"
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1500,
                    easing: "easeOutQuart"
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: "Placement Rate (%)"
                        },
                        ticks: {
                            callback: value => `${value}%`
                        }
                    }
                },
                plugins: getBarChartPlugins(
                    value => `${Number(value).toFixed(1)}%`
                )
            }
        });

    } catch (error) {
        console.error("Department placement rate chart error:", error);
    }
}

// Animated total students vs placed students bar chart
async function loadDepartmentStudentComparisonChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/departments`);
        if (!response.ok) throw new Error("Could not load department data.");

        const result = await response.json();
        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid department data.");
        }

        const departments = result.data;
        const canvas = document.getElementById(
            "departmentStudentComparisonChart"
        );

        if (!canvas) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: departments.map(dept => dept.department),
                datasets: [
                    {
                        label: "Total Students",
                        data: departments.map(
                            dept => Number(dept.total_students || 0)
                        ),
                        backgroundColor: "#94a3b8",
                        borderRadius: 5
                    },
                    {
                        label: "Placed Students",
                        data: departments.map(
                            dept => Number(dept.placed_students || 0)
                        ),
                        backgroundColor: "#16a34a",
                        borderRadius: 5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1500,
                    easing: "easeOutQuart"
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Number of Students"
                        },
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: getBarChartPlugins(value => value)
            }
        });

    } catch (error) {
        console.error("Department student comparison chart error:", error);
    }
}

// Package Analysis summary cards
async function loadPackageSummary() {
    try {
        const response = await fetch(`${API_BASE}/api/packages`);
        if (!response.ok) {
            throw new Error("Failed to load package data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid package API response.");
        }

        const packages = result.data
            .map(item => Number(item.package_lpa))
            .filter(value => Number.isFinite(value));

        if (packages.length === 0) {
            throw new Error("No valid package records found.");
        }

        const average = packages.reduce(
            (sum, value) => sum + value, 0
        ) / packages.length;

        document.getElementById("package-records").textContent =
            packages.length;

        document.getElementById("average-package").textContent =
            `${average.toFixed(2)} LPA`;

        document.getElementById("highest-package").textContent =
            `${Math.max(...packages).toFixed(2)} LPA`;

        document.getElementById("lowest-package").textContent =
            `${Math.min(...packages).toFixed(2)} LPA`;

    } catch (error) {
        console.error("Package summary error:", error);
    }
}

// Animated average package by department chart
async function loadAveragePackageDepartmentChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/packages`);
        if (!response.ok) {
            throw new Error("Could not load package data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid package API response.");
        }

        const packageData = result.data.filter(
            item =>
                item.department &&
                Number.isFinite(Number(item.package_lpa))
        );

        const departmentPackages = {};

        packageData.forEach(item => {
            const department = item.department;

            if (!departmentPackages[department]) {
                departmentPackages[department] = [];
            }

            departmentPackages[department].push(
                Number(item.package_lpa)
            );
        });

        const departments = Object.keys(departmentPackages).sort();

        const averages = departments.map(department => {
            const values = departmentPackages[department];

            return values.reduce((sum, value) => sum + value, 0)
                / values.length;
        });

        const canvas = document.getElementById(
            "averagePackageDepartmentChart"
        );

        if (!canvas) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: departments,
                datasets: [{
                    label: "Average Package (LPA)",
                    data: averages,
                    backgroundColor: [
                        "#2563eb",
                        "#7c3aed",
                        "#0891b2",
                        "#ea580c",
                        "#16a34a"
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 30,
                        right: 15
                    }
                },
                animation: {
                    duration: 1600,
                    easing: "easeOutQuart"
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grace: "15%",
                        title: {
                            display: true,
                            text: "Average Package (LPA)"
                        },
                        ticks: {
                            callback: value => `${value} LPA`
                        }
                    }
                },
                plugins: getBarChartPlugins(
                    value => `${Number(value).toFixed(2)} LPA`
                )
            }
        });

    } catch (error) {
        console.error("Average package chart error:", error);
    }
}

// Animated package distribution chart
async function loadPackageDistributionChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/packages`);
        if (!response.ok) {
            throw new Error("Could not load package data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid package API response.");
        }

        const packages = result.data
            .map(item => Number(item.package_lpa))
            .filter(value => Number.isFinite(value))
            .sort((a, b) => a - b);

        const distribution = {};

        packages.forEach(value => {
            const key = value.toFixed(2);
            distribution[key] = (distribution[key] || 0) + 1;
        });

        const packageValues = Object.keys(distribution).sort(
            (a, b) => Number(a) - Number(b)
        );

        const counts = packageValues.map(
            value => distribution[value]
        );

        const canvas = document.getElementById(
            "packageDistributionChart"
        );

        if (!canvas) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: packageValues.map(value => `${Number(value)} LPA`),
                datasets: [{
                    label: "Number of Placements",
                    data: counts,
                    backgroundColor: "#0d9488",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 30,
                        right: 15
                    }
                },
                animation: {
                    duration: 1600,
                    easing: "easeOutQuart"
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Package Range"
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grace: "15%",
                        title: {
                            display: true,
                            text: "Number of Placements"
                        },
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: getBarChartPlugins(value => value)
            }
        });

    } catch (error) {
        console.error("Package distribution chart error:", error);
    }
}

// Company Analysis summary cards
async function loadCompanySummary() {
    try {
        const response = await fetch(`${API_BASE}/api/companies`);

        if (!response.ok) {
            throw new Error("Failed to load company data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid company API response.");
        }

        const companies = result.data;

        const totalPlacements = companies.reduce(
            (sum, company) =>
                sum + Number(company.students_placed || 0),
            0
        );

        const highestPackage = Math.max(
            0,
            ...companies.map(company =>
                Number(company.highest_package_lpa || 0)
            )
        );

        const bestAverage = Math.max(
            0,
            ...companies.map(company =>
                Number(company.average_package_lpa || 0)
            )
        );

        document.getElementById("company-count").textContent =
            companies.length;

        document.getElementById("company-total-placements").textContent =
            totalPlacements;

        document.getElementById("company-highest-package").textContent =
            `${highestPackage.toFixed(2)} LPA`;

        document.getElementById("company-best-average").textContent =
            `${bestAverage.toFixed(2)} LPA`;

    } catch (error) {
        console.error("Company summary error:", error);
    }
}

// Animated company-wise placements bar chart
async function loadCompanyPlacementsChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/companies`);

        if (!response.ok) {
            throw new Error("Could not load company data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid company API response.");
        }

        const companies = result.data;
        const canvas = document.getElementById("companyPlacementsChart");

        if (!canvas) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: companies.map(company => company.company),
                datasets: [{
                    label: "Students Placed",
                    data: companies.map(
                        company => Number(company.students_placed || 0)
                    ),
                    backgroundColor: [
                        "#2563eb",
                        "#7c3aed",
                        "#0891b2",
                        "#ea580c",
                        "#db2777",
                        "#16a34a"
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 30,
                        right: 15
                    }
                },
                animation: {
                    duration: 1600,
                    easing: "easeOutQuart"
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Company"
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grace: "15%",
                        title: {
                            display: true,
                            text: "Number of Students Placed"
                        },
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: getBarChartPlugins(value => value)
            }
        });

    } catch (error) {
        console.error("Company placements chart error:", error);
    }
}

// Skills Analysis summary cards
async function loadSkillsSummary() {
    try {
        const response = await fetch(`${API_BASE}/api/skills`);

        if (!response.ok) {
            throw new Error("Failed to load skills data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid skills API response.");
        }

        const skills = result.data;

        if (skills.length === 0) {
            throw new Error("No skills data available.");
        }

        const topSkill = skills.reduce((best, current) =>
            Number(current.total_students_with_skill || 0) >
            Number(best.total_students_with_skill || 0)
                ? current
                : best
        );

        const studentsWithSkills = Math.max(
            0,
            ...skills.map(skill =>
                Number(skill.total_students_with_skill || 0)
            )
        );

        const skillStudents =
            Number(topSkill.total_students_with_skill || 0);

        const placedStudents =
            Number(topSkill.placed_students_with_skill || 0);

        const placementRate = skillStudents > 0
            ? placedStudents / skillStudents * 100
            : 0;

        document.getElementById("total-skills").textContent =
            skills.length;

        document.getElementById("students-with-skills").textContent =
            studentsWithSkills;

        document.getElementById("top-skill").textContent =
            topSkill.skill_name;

        document.getElementById("top-skill-placement-rate").textContent =
            `${placementRate.toFixed(1)}%`;

    } catch (error) {
        console.error("Skills summary error:", error);
    }
}

// Animated skill demand bar chart
async function loadSkillsDemandChart() {
    try {
        await loadChartLibrary();

        const response = await fetch(`${API_BASE}/api/skills`);

        if (!response.ok) {
            throw new Error("Could not load skills data.");
        }

        const result = await response.json();

        if (!result.success || !Array.isArray(result.data)) {
            throw new Error("Invalid skills API response.");
        }

        const skills = [...result.data].sort(
            (a, b) =>
                Number(b.total_students_with_skill || 0) -
                Number(a.total_students_with_skill || 0)
        );

        const canvas = document.getElementById("skillsDemandChart");

        if (!canvas) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: skills.map(skill => skill.skill_name),
                datasets: [{
                    label: "Number of Students",
                    data: skills.map(
                        skill => Number(
                            skill.total_students_with_skill || 0
                        )
                    ),

                    // All skill bars are blue
                    backgroundColor: "#2563eb",
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 10,
                        right: 35
                    }
                },
                animation: {
                    duration: 1600,
                    easing: "easeOutQuart"
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grace: "15%",
                        title: {
                            display: true,
                            text: "Number of Students"
                        },
                        ticks: {
                            precision: 0
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Skills"
                        }
                    }
                },
                plugins: getBarChartPlugins(value => value)
            }
        });

    } catch (error) {
        console.error("Skills demand chart error:", error);
    }
}

// Start only the functions needed by the current page
document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("placementStatusChart")) {
        loadDashboardSummary();
        loadPlacementStatusChart();
        loadCompanyDistributionChart();
    }

    if (document.getElementById("departmentPlacementRateChart")) {
        loadDepartmentSummary();
        loadDepartmentPlacementRateChart();
        loadDepartmentStudentComparisonChart();
    }

    if (document.getElementById("averagePackageDepartmentChart")) {
        loadPackageSummary();
        loadAveragePackageDepartmentChart();
        loadPackageDistributionChart();
    }

    if (document.getElementById("companyPlacementsChart")) {
        loadCompanySummary();
        loadCompanyPlacementsChart();
    }

    if (document.getElementById("skillsDemandChart")) {
        loadSkillsSummary();
        loadSkillsDemandChart();
    }
});
