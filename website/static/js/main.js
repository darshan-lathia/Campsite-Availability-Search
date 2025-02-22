// Helper function to reformat a date range string
function formatDateRange(dateRange) {
    // Expecting dateRange like "2025-02-28 (Fri) -> 2025-03-02 (Sun)"
    let parts = dateRange.split('->');
    if (parts.length !== 2) return dateRange; // Fallback if not in expected format
    let start = parts[0].trim();
    let end = parts[1].trim();
    
    function formatPart(part) {
        // Extract the date part (first 10 characters) and the day-of-week in parentheses using a regex
        let datePart = part.substring(0, 10); // "YYYY-MM-DD"
        let dayOfWeekMatch = part.match(/\((.*?)\)/);
        let dayOfWeek = dayOfWeekMatch ? ` (${dayOfWeekMatch[1]})` : "";
        let [year, month, day] = datePart.split('-');
        const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        let formattedDay = parseInt(day, 10); // Removing any leading zeros
        let formattedMonth = months[parseInt(month, 10)-1];
        let formattedYear = year.substring(2);
        return `${formattedDay} ${formattedMonth} ${formattedYear}${dayOfWeek}`;
    }
    
    let startFormatted = formatPart(start);
    let endFormatted = formatPart(end);
    return `${startFormatted} - ${endFormatted}`;
}

document.addEventListener('DOMContentLoaded', function() {
    // Check for stored park ID
    const fillParkId = sessionStorage.getItem('fillParkId');
    if (fillParkId) {
        document.getElementById('parkId').value = fillParkId;
        sessionStorage.removeItem('fillParkId');
    }
    
    const searchForm = document.getElementById('searchForm');
    
    // Initialize Google Places Autocomplete
    if (document.getElementById('citySearch')) {
        let selectedPlace = null;  // Store the selected place
        const autocomplete = new google.maps.places.Autocomplete(
            document.getElementById('citySearch'),
            {
                types: ['(cities)'],
                componentRestrictions: { country: 'us' },  // Restrict to USA only
                fields: ['place_id', 'geometry', 'formatted_address', 'name']
            }
        );

        // Optional: Handle place selection
        autocomplete.addListener('place_changed', function() {
            const place = autocomplete.getPlace();
            if (place.geometry) {
                selectedPlace = place;  // Store the selected place
            }
        });

        // Handle search button click
        document.querySelector('.search-city-button').addEventListener('click', function() {
            if (selectedPlace && selectedPlace.geometry) {
                const lat = selectedPlace.geometry.location.lat();
                const lng = selectedPlace.geometry.location.lng();
                // Fetch nearby campsites
                fetch('/search_campsites', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        latitude: lat,
                        longitude: lng
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Create and show campsite list
                        const campsiteList = document.createElement('div');
                        campsiteList.className = 'campsite-list';
                        
                        // Create results container
                        const resultsContainer = document.createElement('div');
                        resultsContainer.className = 'campsite-results';
                        
                        // Create the map div
                        const mapDiv = document.createElement('div');
                        mapDiv.className = 'area-map';
                        
                        // Initialize the map
                        const map = new google.maps.Map(mapDiv, {
                            center: { lat: lat, lng: lng },
                            zoom: 9,
                            mapTypeId: 'terrain',
                            mapTypeControl: true,
                            zoomControl: true,
                            scrollwheel: true
                        });
                        
                        // Add markers for each campsite
                        data.campsites.forEach(site => {
                            const marker = new google.maps.Marker({
                                position: { 
                                    lat: parseFloat(site.latitude), 
                                    lng: parseFloat(site.longitude) 
                                },
                                map: map,
                                title: site.name
                            });
                            
                            // Add info window for each marker
                            const infoWindow = new google.maps.InfoWindow({
                                content: `
                                    <div style="padding: 10px;">
                                        <h3 style="margin: 0 0 5px 0;">${site.name}</h3>
                                        <p style="margin: 0;">ID: ${site.id}</p>
                                    </div>
                                `
                            });
                            
                            marker.addListener('click', () => {
                                infoWindow.open(map, marker);
                            });
                        });
                        
                        const headerContainer = document.createElement('div');
                        headerContainer.className = 'campsite-header';
                        headerContainer.innerHTML = `
                            <h3>Campsites near ${selectedPlace.formatted_address}</h3>
                            <span class="click-note">click to populate park ID</span>
                        `;
                        
                        // Add header and results to results container
                        resultsContainer.appendChild(headerContainer);
                        
                        data.campsites.forEach(site => {
                            const siteElement = document.createElement('div');
                            siteElement.className = 'campsite-item';
                            // Make the campsite info clickable to populate park ID
                            const siteInfo = document.createElement('div');
                            siteInfo.className = 'campsite-info';
                            siteInfo.innerHTML = `
                                <span class="campsite-name">${site.name}</span>
                                <span class="campsite-id">ID: ${site.id}</span>
                            `;
                            siteInfo.addEventListener('click', function() {
                                document.getElementById('parkId').value = site.id;
                                // Save to history
                                const history = JSON.parse(localStorage.getItem('campsiteHistory') || '[]');
                                const newEntry = {
                                    city: selectedPlace.formatted_address,
                                    parkName: site.name,
                                    parkId: site.id,
                                    timestamp: new Date().toISOString()
                                };
                                
                                // Remove any duplicate entries for this park
                                const filteredHistory = history.filter(item => item.parkId !== site.id);
                                
                                // Add new entry at the beginning
                                filteredHistory.unshift(newEntry);
                                
                                // Keep only the last 10 entries
                                if (filteredHistory.length > 10) {
                                    filteredHistory.pop();
                                }
                                
                                localStorage.setItem('campsiteHistory', JSON.stringify(filteredHistory));
                            });
                            siteElement.appendChild(siteInfo);
                            resultsContainer.appendChild(siteElement);
                        });
                        
                        // Append both map and results container to campsite list
                        campsiteList.appendChild(mapDiv);
                        campsiteList.appendChild(resultsContainer);
                        
                        // Insert results after the city search form group
                        const citySearchGroup = document.getElementById('citySearch').closest('.form-group');
                        // Remove any existing campsite list
                        const existingList = document.querySelector('.campsite-list');
                        if (existingList) {
                            existingList.remove();
                        }
                        // Insert the new list after the city search group
                        citySearchGroup.insertAdjacentElement('afterend', campsiteList);
                    } else {
                        alert('Error fetching campsites: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while searching for campsites');
                });
            } else {
                alert('Please select a city from the dropdown first');
            }
        });
    }

    if (searchForm) {  // Only on index page
        // Set default dates when page loads
        setDefaultDates();

        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = getFormData();
            // Store form data in sessionStorage
            sessionStorage.setItem('searchData', JSON.stringify(formData));
            // Navigate to results page
            window.location.href = '/results';
        });
    } else {  // On results page
        // Get stored form data and perform search
        const searchData = JSON.parse(sessionStorage.getItem('searchData'));
        if (searchData) {
            performSearch(searchData);
        }
    }

    function getFormData() {
        return {
            parkId: document.getElementById('parkId').value,
            startDate: document.getElementById('startDate').value,
            endDate: document.getElementById('endDate').value,
            nights: document.getElementById('nights').value,
            searchPreference: document.querySelector('input[name="searchPreference"]:checked').value,
            notify: document.getElementById('notify').checked
        };
    }

    function performSearch(formData) {
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateResults(data.results);
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while searching');
        });
    }

    function updateResults(results) {
        console.log("Received results:", results);
        // Get search data at the start of updateResults
        const searchData = JSON.parse(sessionStorage.getItem('searchData'));

        // Create container for results sections
        const sectionsContainer = document.createElement('div');
        sectionsContainer.className = 'sections-container';
        document.querySelector('.results-container').innerHTML = '';  // Clear previous results
        
        // Add campground name if available
        if (results.campground_name) {
            const campgroundName = document.createElement('div');
            campgroundName.className = 'campground-name';
            // Create link element
            const campgroundLink = document.createElement('a');
            campgroundLink.href = `https://www.recreation.gov/camping/campgrounds/${searchData.parkId}`;
            campgroundLink.target = '_blank';  // Open in new tab
            campgroundLink.onclick = function(e) {
                e.preventDefault();  // Prevent default navigation
                if (confirm('Would you like to visit Recreation.gov to make a reservation?\n\nNote: You will need to enter your dates on Recreation.gov')) {
                    window.open(this.href, '_blank');
                }
            };
            campgroundLink.textContent = results.campground_name;
            campgroundName.appendChild(campgroundLink);
            document.querySelector('.results-container').appendChild(campgroundName);
        }
        
        document.querySelector('.results-container').appendChild(sectionsContainer);

        // Determine which sections to show based on search preference
        const searchPreference = searchData ? searchData.searchPreference : 'all';
        let sectionsToShow = [];
        
        switch(searchPreference) {
            case 'weekends':
                sectionsToShow = ['priority'];  // Only Weekend (Priority) results
                break;
            case 'flexible':
                sectionsToShow = ['priority', 'regular'];  // Weekend and Weekend Flexible results
                break;
            case 'all':
                sectionsToShow = ['priority', 'regular', 'ignored'];  // All sections
                break;
        }

        // Update only the selected sections
        sectionsToShow.forEach(section => {
            // Only create sections that have results
            if (results[section] && results[section].length > 0) {
                const sectionElement = document.createElement('div');
                sectionElement.className = 'results-section';
                // Map section names to display titles
                const sectionTitles = {
                    'priority': 'Weekend',
                    'regular': 'Weekend Flexible',
                    'ignored': 'Weekday'
                };
                sectionElement.innerHTML = `
                    <h2>${sectionTitles[section]}</h2>
                    <div class="results-content"></div>
                `;
                sectionsContainer.appendChild(sectionElement);

                const contentElement = sectionElement.querySelector('.results-content');
                results[section].forEach(result => {
                    const resultElement = document.createElement('div');
                    resultElement.className = 'result-item';

                    // Split the result text at " --> " to separate the date range from the availability info
                    const parts = result.text.split(' --> ');
                    const dateRange = parts[0].trim();
                    const siteInfo = parts.length === 2 ? parts[1].trim() : '';

                    // Split the formatted date range back into start and end parts
                    // Since our formatDateRange returns "28 Feb 25 (Fri) - 2 Mar 25 (Sun)",
                    // we can split on the " - " delimiter.
                    const dateParts = formatDateRange(dateRange).split(' - ');
                    const startDateFormatted = dateParts[0] || '';
                    const endDateFormatted = dateParts[1] || '';

                    resultElement.innerHTML = `
                        <div class="result-card">
                            <div class="result-date-line">
                                <span class="result-icon">📅</span>
                                <span class="result-date-text">${startDateFormatted}</span>
                                <span class="result-arrow">→</span>
                                <span class="result-date-text">${endDateFormatted}</span>
                                <div class="result-availability">${siteInfo}</div>
                            </div>
                        </div>
                    `;
                    // Add click handler after creating the element
                    const availabilityDiv = resultElement.querySelector('.result-availability');
                    availabilityDiv.addEventListener('click', function() {
                        if(confirm(`Would you like to visit Recreation.gov to make a reservation?\n\nRemember these dates:\n${startDateFormatted} → ${endDateFormatted}`)) {
                            window.open(`https://www.recreation.gov/camping/campgrounds/${searchData.parkId}`, '_blank');
                        }
                    });
                    contentElement.appendChild(resultElement);
                });
            }
        });

        // If no results in any section
        if (!sectionsToShow.some(section => results[section] && results[section].length > 0)) {
            const noResults = document.createElement('p');
            noResults.className = 'no-results';
            noResults.textContent = 'No available dates found';
            sectionsContainer.appendChild(noResults);
        }
    }

    // Set default dates
    function setDefaultDates() {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        const threeMonthsLater = new Date();
        threeMonthsLater.setMonth(threeMonthsLater.getMonth() + 3);
        
        // Format dates as YYYY-MM-DD
        const formatDate = (date) => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        };
        
        document.getElementById('startDate').value = formatDate(tomorrow);
        document.getElementById('endDate').value = formatDate(threeMonthsLater);
    }
}); 