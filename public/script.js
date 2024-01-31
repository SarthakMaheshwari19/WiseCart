// public/script.js
document.addEventListener('DOMContentLoaded', () => {
    const amazonResults = document.getElementById('amazon-results');
    const flipkartResults = document.getElementById('flipkart-results');
    const myntraResults = document.getElementById('myntra-results'); 


    // Fetch and display Amazon results
    fetchResults('/amazon', amazonResults);

    // Fetch and display Flipkart results
    fetchResults('/flipkart', flipkartResults);
    fetchResults('/myntra', myntraResults);
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

