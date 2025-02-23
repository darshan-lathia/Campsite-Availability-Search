# Campsite Availability Search

A web application that helps users find and book available campsites on Recreation.gov. This tool simplifies the camping trip planning process by providing an intuitive interface to search for campgrounds and check their availability.

## Features

- 🏕 Search for campgrounds within 200 miles of any US city
- 🗺 Interactive map showing campground locations
- 📅 Filter for weekend-only or flexible date availability
- 🔍 Search history tracking for quick access to previous searches
- 🔗 Direct links to Recreation.gov for booking
- 📱 Responsive design for both desktop and mobile

## Demo

Visit [rerecreation.us](https://rerecreation.us) to try the application.

## Installation

### Prerequisites

- Python 3.12+
- pip
- Nginx
- Google Maps API key
- Recreation.gov API key

### Setup

1. Clone the repository

git clone https://github.com/yourusername/Campsite-Availability-Search.git
cd Campsite-Availability-Search


2. Create and activate virtual environment

python -m venv camping_reservation_env
source camping_reservation_env/bin/activate  # On Windows: .\camping_reservation_env\Scripts\activate


3. Install dependencies

cd website
pip install -r requirements.txt


4. Create .env file with your API keys

touch .env


Add the following to .env:

MAPS_API_KEY=your_google_maps_api_key
RECREATION_API_KEY=your_recreation_gov_api_key


5. Configure Nginx

server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


6. Start the application

chmod +x manage.sh
./manage.sh start


## Usage

1. Enter a city name to find nearby campgrounds
2. Click on a campground marker or list item to select it
3. Choose your date range and preferences:
   - Weekend Only (Friday-Sunday)
   - Flexible Weekend (Thursday-Monday)
   - All Available Dates
4. Set the number of consecutive nights needed
5. Click "Search Availability" to see available dates
6. Click on any available date to book through Recreation.gov

## Development

### Project Structure

website/
├── app.py              # Flask application
├── static/
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/         # HTML templates
├── manage.sh          # Server management script
└── requirements.txt   # Python dependencies


### Management Script Commands

./manage.sh start    # Start the server
./manage.sh stop     # Stop the server
./manage.sh restart  # Restart the server
./manage.sh status   # Check server status
./manage.sh logs     # View logs


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Recreation.gov](https://www.recreation.gov/) for providing the campsite data
- [Google Maps Platform](https://cloud.google.com/maps-platform/) for mapping services

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Security

Please do not commit any API keys or sensitive information. Use environment variables for all sensitive data.


You can now copy this content into your README.md file. Would you like me to explain any section in more detail?
