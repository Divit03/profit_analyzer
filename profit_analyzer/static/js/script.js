function addRow() {
    const tableBody = document.querySelector('#salesTable tbody');
    const rowCount = tableBody.rows.length + 1;
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${rowCount}</td>
        <td><input type="number" class="form-control bg-dark text-light animate-pulse" name="revenue" required></td>
        <td><input type="number" class="form-control bg-dark text-light animate-pulse" name="cost" required></td>
        <td><button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this); playSound('remove')"><i class="fas fa-trash"></i></button></td>
    `;
    tableBody.appendChild(newRow);
}

function removeRow(button) {
    button.closest('tr').remove();
    // Re-number rows after removal
    const rows = document.querySelectorAll('#salesTable tbody tr');
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

function simulateData() {
    // Simulate sample data
    const sampleData = [
        { revenue: 1000, cost: 800 },
        { revenue: 1200, cost: 1300 },
        { revenue: 1100, cost: 850 },
        { revenue: 1300, cost: 1400},
        { revenue: 1400, cost: 1000}
    ];
    const tableBody = document.querySelector('#salesTable tbody');
    tableBody.innerHTML = '';  // Clear existing
    sampleData.forEach((data, index) => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${index + 1}</td>
            <td><input type="number" class="form-control bg-dark text-light animate-pulse" name="revenue" value="${data.revenue}" required></td>
            <td><input type="number" class="form-control bg-dark text-light animate-pulse" name="cost" value="${data.cost}" required></td>
            <td><button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this); playSound('remove')"><i class="fas fa-trash"></i></button></td>
        `;
        tableBody.appendChild(newRow);
    });
}

function playSound(type) {
    // Placeholder for sound effects (add audio files if needed)
    console.log('Playing sound:', type);
}