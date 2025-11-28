let df = [];

function processXLSXData(rows) {
    let data = [];
    const headers = ['S_No', 'Name', 'Designation', 'Journal_Publications', 'Conference_Publications', 'Books_Chapters', 'Research_Projects_Completed', 'Research_Projects_Ongoing', 'Domain'];

    for (let i = 0; i < rows.length; i++) {
        let values = rows[i];
        
        if (!values || values.length < headers.length) continue; 

        let obj = {};
        
        obj.S_No = parseInt(values[0]);
        obj.Name = values[1] ? String(values[1]).trim() : '';
        obj.Designation = values[2] ? String(values[2]).trim() : '';
        obj.Journal_Publications = parseInt(values[3] || 0); 
        obj.Conference_Publications = parseInt(values[4] || 0);
        obj.Books_Chapters = parseInt(values[5] || 0);
        obj.Research_Projects_Completed = parseInt(values[6] || 0);
        obj.Research_Projects_Ongoing = parseInt(values[7] || 0);
        obj.Domain = values[8] ? String(values[8]).trim() : '';
        
        if (isNaN(obj.S_No)) continue; 

        obj.Total_Publications = obj.Journal_Publications + obj.Conference_Publications + obj.Books_Chapters;
        obj.Total_Research_Projects = obj.Research_Projects_Completed + obj.Research_Projects_Ongoing;
        data.push(obj);
    }
    return data;
}

async function fetchAndProcessData() {
    try {
        const response = await fetch('ece.xlsx');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const arrayBuffer = await response.arrayBuffer();

        if (typeof XLSX === 'undefined') {
            throw new Error("XLSX parsing library (SheetJS) not found. Please ensure it's included in index.html.");
        }
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        
        const rawData = XLSX.utils.sheet_to_json(worksheet, { header: 1, range: 3 }); 

        df = processXLSXData(rawData);
        
        setupFilters();
        applyFilters();

    } catch (error) {
        console.error("Error fetching or processing data:", error);
        document.getElementById('main-content').innerHTML = `
            <div style="color: red; padding: 20px; text-align: center;">
                <h2>Error Loading Data</h2>
                <p>Could not load the XLSX file: ece.xlsx. Please ensure the file is correctly placed and accessible.</p>
                <p>Error details: ${error.message}</p>
            </div>
        `;
    }
}

function resetFilters() {
    document.getElementById('search-name').value = '';

    const designationSelect = document.getElementById('designation-multiselect');
    Array.from(designationSelect.options).forEach(option => option.selected = true);
    
    const domainSelect = document.getElementById('domain-multiselect');
    Array.from(domainSelect.options).forEach(option => option.selected = true);

    const totalPubsSlider = document.getElementById('min-total-pubs');
    totalPubsSlider.value = 0;
    document.getElementById('min-total-pubs-value').textContent = 0;

    const journalPubsSlider = document.getElementById('min-journal-pubs');
    journalPubsSlider.value = 0;
    document.getElementById('min-journal-pubs-value').textContent = 0;

    applyFilters();
}

function applyFilters() {
    let filteredDf = [...df];

    const searchName = document.getElementById('search-name').value.toLowerCase();
    if (searchName) {
        filteredDf = filteredDf.filter(row => row.Name.toLowerCase().includes(searchName));
    }

    const designationSelect = document.getElementById('designation-multiselect');
    let selectedDesignations = Array.from(designationSelect ? designationSelect.selectedOptions : []).map(option => option.value);
    if (selectedDesignations.length > 0) {
        filteredDf = filteredDf.filter(row => selectedDesignations.includes(row.Designation));
    }

    const domainSelect = document.getElementById('domain-multiselect');
    let selectedDomains = Array.from(domainSelect ? domainSelect.selectedOptions : []).map(option => option.value);
    if (selectedDomains.length > 0) {
        filteredDf = filteredDf.filter(row => selectedDomains.includes(row.Domain));
    }
    
    const minTotalPubs = parseInt(document.getElementById('min-total-pubs').value) || 0;
    const minJournalPubs = parseInt(document.getElementById('min-journal-pubs').value) || 0;

    filteredDf = filteredDf.filter(row => row.Total_Publications >= minTotalPubs);
    filteredDf = filteredDf.filter(row => row.Journal_Publications >= minJournalPubs);

    renderKPIs(filteredDf);
    renderCharts(filteredDf);
    renderDataTable(filteredDf);
}

function setupFilters() {
    const uniqueDesignations = [...new Set(df.map(item => item.Designation))].sort();
    const uniqueDomains = [...new Set(df.map(item => item.Domain))].sort();

    function createMultiselect(containerId, options, selectId, label) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = `
            <label for="${selectId}">${label}</label>
            <select id="${selectId}" multiple>
                ${options.map(opt => `<option value="${opt}" selected>${opt}</option>`).join('')}
            </select>
        `;
        document.getElementById(selectId).addEventListener('change', applyFilters);
    }

    createMultiselect('designation-filter-nav', uniqueDesignations, 'designation-multiselect', '👔 Filter by Designation');
    createMultiselect('domain-filter-nav', uniqueDomains, 'domain-multiselect', '🔬 Filter by Research Domain');
    
    const totalPubsSlider = document.getElementById('min-total-pubs');
    const journalPubsSlider = document.getElementById('min-journal-pubs');

    const maxTotalPubs = Math.max(...df.map(r => r.Total_Publications));
    const maxJournalPubs = Math.max(...df.map(r => r.Journal_Publications));

    if (totalPubsSlider) {
        totalPubsSlider.max = maxTotalPubs;
        document.getElementById('min-total-pubs-value').textContent = totalPubsSlider.value;
        totalPubsSlider.addEventListener('input', (e) => {
            document.getElementById('min-total-pubs-value').textContent = e.target.value;
            applyFilters();
        });
    }

    if (journalPubsSlider) {
        journalPubsSlider.max = maxJournalPubs;
        document.getElementById('min-journal-pubs-value').textContent = journalPubsSlider.value;
        journalPubsSlider.addEventListener('input', (e) => {
            document.getElementById('min-journal-pubs-value').textContent = e.target.value;
            applyFilters();
        });
    }
    
    document.getElementById('search-name').addEventListener('input', applyFilters);
    
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

function renderKPIs(data) {
    const totalProfessors = data.length;
    const totalJournalPubs = data.reduce((sum, row) => sum + row.Journal_Publications, 0);
    const totalConferencePubs = data.reduce((sum, row) => sum + row.Conference_Publications, 0);
    const totalBooksChapters = data.reduce((sum, row) => sum + row.Books_Chapters, 0);
    const completedProjects = data.reduce((sum, row) => sum + row.Research_Projects_Completed, 0);
    const ongoingProjects = data.reduce((sum, row) => sum + row.Research_Projects_Ongoing, 0);
    const totalPublications = data.reduce((sum, row) => sum + row.Total_Publications, 0);
    const avgPubs = totalProfessors > 0 ? (totalPublications / totalProfessors).toFixed(1) : 0;
    const uniqueDomains = [...new Set(data.map(row => row.Domain))].length;

    const metrics = [
        { title: "👨‍🏫 Total Professors", value: totalProfessors },
        { title: "📚 Total Journal Publications", value: totalJournalPubs },
        { title: "📄 Total Conference Publications", value: totalConferencePubs },
        { title: "📖 Total Books/Chapters", value: totalBooksChapters },
        { title: "✅ Completed Projects", value: completedProjects },
        { title: "🔄 Ongoing Projects", value: ongoingProjects },
        { title: "📊 Avg Publications/Professor", value: avgPubs },
        { title: "🔬 Unique Domains", value: uniqueDomains },
    ];

    const kpiContainer = document.getElementById('kpi-metrics');
    kpiContainer.innerHTML = metrics.map(m => `
        <div class="metric-card">
            <h4>${m.title}</h4>
            <p>${m.value}</p>
        </div>
    `).join('');
}

function renderDataTable(data) {
    data.sort((a, b) => b.Total_Publications - a.Total_Publications);

    const columns = [
        'S_No', 'Name', 'Designation', 'Domain',
        'Journal_Publications', 'Conference_Publications', 'Books_Chapters',
        'Total_Publications', 'Research_Projects_Completed', 'Research_Projects_Ongoing',
        'Total_Research_Projects'
    ];

    const tableContainer = document.getElementById('data-table-container');
    
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    ${columns.map(col => `<th>${col.replace(/_/g, ' ')}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
                ${data.map(row => `
                    <tr>
                        ${columns.map(col => `<td>${row[col]}</td>`).join('')}
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    tableContainer.innerHTML = tableHTML;
}

function renderCharts(data) {
    if (data.length === 0) {
        document.getElementById('chart1').innerHTML = '<p style="text-align:center;">No data to display.</p>';
        document.getElementById('chart2').innerHTML = '<p style="text-align:center;">No data to display.</p>';
        document.getElementById('chart3').innerHTML = '<p style="text-align:center;">No data to display.</p>';
        document.getElementById('chart4').innerHTML = '<p style="text-align:center;">No data to display.</p>';
        return;
    }

    const topProfs = data
        .sort((a, b) => b.Total_Publications - a.Total_Publications)
        .slice(0, 15);

    Plotly.newPlot('chart1', [{
        x: topProfs.map(r => r.Total_Publications),
        y: topProfs.map(r => r.Name.replace('Dr ', '')),
        type: 'bar',
        orientation: 'h',
        marker: { color: topProfs.map(r => r.Total_Publications), colorscale: 'Blues' }
    }], {
        title: 'Top 15 Professors by Total Publications',
        height: 500,
        xaxis: { title: 'Total Publications' },
        yaxis: { automargin: true }
    }, { responsive: true });

    const domainPubsMap = data.reduce((acc, row) => {
        acc[row.Domain] = (acc[row.Domain] || 0) + row.Total_Publications;
        return acc;
    }, {});
    const domainPubs = Object.entries(domainPubsMap).sort(([, a], [, b]) => b - a);

    Plotly.newPlot('chart2', [{
        x: domainPubs.map(([domain]) => domain),
        y: domainPubs.map(([, count]) => count),
        type: 'bar',
        marker: { color: domainPubs.map(([, count]) => count), colorscale: 'Viridis' }
    }], {
        title: 'Total Publications by Research Domain',
        height: 500,
        xaxis: { title: 'Research Domain', automargin: true },
        yaxis: { title: 'Total Publications' }
    }, { responsive: true });
    
    const designationCountsMap = data.reduce((acc, row) => {
        acc[row.Designation] = (acc[row.Designation] || 0) + 1;
        return acc;
    }, {});

    Plotly.newPlot('chart4', [{
        values: Object.values(designationCountsMap),
        labels: Object.keys(designationCountsMap),
        type: 'pie',
        hole: 0.4,
        marker: { colors: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'] }
    }], {
        title: 'Faculty Distribution by Designation',
        height: 500
    }, { responsive: true });
    
    const projectDataMap = data
        .filter(r => r.Total_Research_Projects > 0)
        .sort((a, b) => (b.Research_Projects_Completed + b.Research_Projects_Ongoing) - (a.Research_Projects_Completed + a.Research_Projects_Ongoing))
        .slice(0, 15)
        .reduce((acc, row) => {
            acc.names.push(row.Name.replace('Dr ', ''));
            acc.completed.push(row.Research_Projects_Completed);
            acc.ongoing.push(row.Research_Projects_Ongoing);
            return acc;
        }, { names: [], completed: [], ongoing: [] });

    const trace1 = {
        x: projectDataMap.names,
        y: projectDataMap.completed,
        name: 'Completed',
        type: 'bar',
        marker: { color: '#2ecc71' }
    };

    const trace2 = {
        x: projectDataMap.names,
        y: projectDataMap.ongoing,
        name: 'Ongoing',
        type: 'bar',
        marker: { color: '#3498db' }
    };

    const layout3 = {
        title: 'Research Projects: Completed vs Ongoing (Top 15)',
        xaxis: { automargin: true },
        yaxis: { title: 'Number of Projects' },
        barmode: 'stack',
        height: 500
    };

    Plotly.newPlot('chart3', [trace1, trace2], layout3, { responsive: true });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('last-updated').textContent = `*Last Updated: ${new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}*`;

    fetchAndProcessData();
});