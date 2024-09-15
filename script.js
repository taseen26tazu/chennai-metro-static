
document.addEventListener('DOMContentLoaded', () => {
    const resultsDiv = document.getElementById('results');
    const sourceStationDropdown = document.getElementById('sourceStation');
    const destinationStationDropdown = document.getElementById('destinationStation');

    // Populate the dropdown with station names
    function populateStations() {
        fetch('http://localhost:5000/api/list_stations')
            .then(response => response.json())
            .then(data => {
                const stations = data.stations;
                stations.forEach(station => {
                    const option1 = document.createElement('option');
                    option1.value = station;
                    option1.textContent = station.split('~')[0]; // Remove suffix for display
                    sourceStationDropdown.appendChild(option1);
    
                    const option2 = document.createElement('option');
                    option2.value = station;
                    option2.textContent = station.split('~')[0]; // Remove suffix for display
                    destinationStationDropdown.appendChild(option2);
                });
            })
            .catch(error => {
                console.error('Error fetching stations:', error);
                resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            });
    }
    

    // Call this function to populate the dropdowns once the page loads
    populateStations();

    // Function to send request to server
    function sendRequest(endpoint, data = {}) {
        return fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }).then(async response => {
            if (!response.ok) {
                const errorBody = await response.text();
                console.error('Error response:', response.status, errorBody);
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
            }
            return response.json();
        }).catch(error => {
            console.error('Fetch error:', error);
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            throw error;
        });
    }
    
    /*function isSameLine(source, destination) {
        const blueLineStations = [
            "Wimco Nagar Depot", "Wimco Nagar", "Thiruvottriyur", "Thiruvottriyur Theradi", "Kaladipet", "Tollgate",
            "New Washermanpet", "Tondiarpet", "Sir Theagaraya College", "Washermanpet", "Mannadi", "High Court",
            "MGR Central (Chennai Central)", "Government Estate", "LIC", "Thousand Lights", "AG DMS", "Teynampet",
            "Nandanam", "Saidapet", "Little Mount", "Guindy", "Arignar Anna Alandur", "Nanganallur Road","Meenambakkam","Chennai International Airport"               
        ];
    
        const greenLineStations = [
            "MGR Central (Chennai Central)","Egmore","Nehru Park","Kilpauk Medical College","Pachaiyappa College","Shenoy Nagar","Anna Nagar East",
            "Anna Nagar Tower","Thirumangalam","Koyambedu","CMBT","Arumbakkam","Vadapalani","Ashok Nagar",  "Ekkattuthangal", 
            "Arignar Anna Alandur","ST Thomas Mount"
            
           
        ];
    
        // Check if both stations are on the Blue Line
        if (blueLineStations.includes(source) && blueLineStations.includes(destination)) {
            return 'blue';
        }
        
        // Check if both stations are on the Green Line
        if (greenLineStations.includes(source) && greenLineStations.includes(destination)) {
            return 'green';
        }
    
        // Check if interchange is required at MGR Central or Alandur
        if (source === "MGR Central (Chennai Central)" || destination === "MGR Central (Chennai Central)" ||
            source === "Alandur" || destination === "Alandur") {
            return 'blue-green-interconnected';
        }
    
        // Default case for interchange
        return 'interchange';
    }*/
    

    // Find Path by Distance
    
    function findPathByDistance() {
        const source = sourceStationDropdown.value;
        const destination = destinationStationDropdown.value;
    
        if (source && destination) {
            console.log(`Sending request for path from ${source} to ${destination}`);
    
            resultsDiv.innerHTML = '<div class="spinner"></div>';  // Show spinner
    
            sendRequest('path_details', { source, destination })
                .then(data => {
                    let resultHTML = `<h3>Path Details:</h3>`;
                    resultHTML += `<p>From ${source} to ${destination}</p>`;
                    resultHTML += `<p>Total stations between: ${data.stations_between.count}</p>`;
                    resultHTML += `<p>Stations: ${data.stations_between.names.join(' -> ')}</p>`;
                    resultHTML += `<p>Distance: ${data.distance}</p>`;
                    resultHTML += `<p>Total time: ${data.time}</p>`;
    
                    // Handle interchanges
                    if (data.interchanges.count > 0) {
                        resultHTML += `<p>Interchanges (${data.interchanges.count}): ${data.interchanges.stations.join(', ')}</p>`;
                    } else {
                        resultHTML += `<p>Interchanges: No interchange required</p>`;
                    }
    
                    resultsDiv.innerHTML = resultHTML;
                })
                .catch(error => {
                    console.error('Error in findPathByDistance:', error);
                    console.error('Error details:', {
                        message: error.message,
                        stack: error.stack,
                        source: source,
                        destination: destination
                    });

                    resultsDiv.innerHTML = `<p>Error: An unknown error occurred.</p>`;
                    
                });
        }    
    }
    

    // Add event listener for the button
    document.getElementById('pathDistance').addEventListener('click', findPathByDistance);
});


