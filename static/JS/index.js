document.addEventListener('DOMContentLoaded', function () {
    // Simulate client data (replace with your actual data)
    const clientsData = [
        { id: 1, name: 'Client 1', ip: '192.168.1.1', mac: '00:11:22:33:44:55', longitude: '12.345', latitude: '67.890' },
        { id: 2, name: 'Client 2', ip: '192.168.1.2', mac: '00:11:22:33:44:56', longitude: '23.456', latitude: '78.901' },
        // Add more clients as needed
    ];

    // Create a table row for each client
    const table = document.getElementById('clientTable');
    clientsData.forEach(client => {
        const row = table.insertRow();
        row.innerHTML = `<td>${client.id}</td><td><a href="/client/${client.id}">${client.name}</a></td><td>${client.ip}</td><td>${client.mac}</td><td>${client.longitude}</td><td>${client.latitude}</td>`;
    });
});
