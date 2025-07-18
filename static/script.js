function search() {
    const query = document.getElementById("searchBox").value;
    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            const result = document.getElementById("result");
            if (data.status === "found") {
                result.innerHTML = `<strong>${data.entry.identifier}</strong> is marked as <em>DWC</em>: ${data.entry.reason}`;
            } else {
                result.innerHTML = `<strong>${query}</strong> is <span style='color:green;'>not flagged</span>.`;
            }
        });
}

function submitDWC() {
    const identifier = document.getElementById("newID").value;
    const reason = document.getElementById("reason").value;
    const key = document.getElementById("adminkey").value;
    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `identifier=${encodeURIComponent(identifier)}&reason=${encodeURIComponent(reason)}&adminkey=${encodeURIComponent(key)}`
    })
    .then(res => res.json())
    .then(data => {
        const status = document.getElementById("submitStatus");
        if (data.status === "success") {
            status.innerHTML = "Entry submitted successfully.";
        } else if (data.status === "unauthorized") {
            status.innerHTML = "Unauthorized. Invalid admin key.";
        } else {
            status.innerHTML = "Error submitting entry.";
        }
    });
}
