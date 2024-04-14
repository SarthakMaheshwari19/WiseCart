// public/script.js
document.addEventListener('DOMContentLoaded', () => {
    const amazonResults = document.getElementById('amazon-results');
    const flipkartResults = document.getElementById('flipkart-results');
    const myntraResults = document.getElementById('myntra-results');
    const paytmFlightsResults = document.getElementById('paytmFlights-results');
    const makemytripResults = document.getElementById('makemytrip-results'); 


    // Fetch and display Amazon results
    fetchResults('/amazon', amazonResults);

    // Fetch and display Flipkart results
    fetchResults('/flipkart', flipkartResults);
    fetchResults('/myntra', myntraResults);
    fetchFlightResults('/paytmflights',paytmFlightsResults)
    fetchFlightResults('/makemytrip',makemytripResults)
});

async function fetchResults(endpoint, container) {
    try {
        const response = await fetch(`http://localhost:3000${endpoint}`);
        const data = await response.json();

        data.forEach(product => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <img src="${product.image_url}" alt="${product.title}">
                <h3>${product.title}</h3>
                <p>${product.price}</p>
                <a href="${product.url}" target="_blank">View Details</a>
            `;
            container.appendChild(listItem);
        });
    } catch (error) {
        console.error(`Error fetching data from ${endpoint}:`, error.message);
    }
}

async function fetchFlightResults(endpoint, container) {
    try {
        const response = await fetch(`http://localhost:3000${endpoint}`);
        const data = await response.json();

        data.forEach(flight => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <h3>${flight.airline}</h3>
                <p>Origin: ${flight.origin} | Destination: ${flight.destination}</p>
                <p>Departure: ${flight.departureTime} | Arrival: ${flight.arrivalTime}</p>
                <p>Duration: ${flight.duration}</p>
                <p>Price: ${flight.price}</p>
                <a href="${flight.bookingUrl}" target="_blank">Book Now</a>
            `;
            container.appendChild(listItem);
        });
    } catch (error) {
        console.error(`Error fetching flight data from ${endpoint}:`, error.message);
    }
}

