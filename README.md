
# Music Streaming App

A simple web application for uploading and streaming music files organized into playlists. Built with Flask for the backend and jQuery for the frontend, this application provides a user-friendly interface for music uploads and retrieval.

## Features

- **Upload Music**: Users can upload `.mp3` files along with a specified playlist ID.
- **View Playlists**: Users can enter a playlist ID to load and play music files associated with that playlist.
- **Toast Notifications**: Users receive feedback through toast notifications when music uploads are successful.
- **Responsive Design**: The application is designed to be user-friendly with a clean interface.

## Technologies Used

- **Backend**: 
  - Flask (Python) for creating RESTful API endpoints.
  - Amazon DynamoDB for storing music metadata and playlists.
  
- **Frontend**:
  - HTML, CSS, and JavaScript for the user interface.
  - jQuery for handling AJAX requests and DOM manipulation.
  
- **Deployment**: 
  - Docker (if applicable) for containerization and easy deployment.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- boto3 (for AWS SDK)
- jQuery
- Docker (optional, if you are using Docker for deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/music-streaming-app.git
   cd music-streaming-app
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your AWS credentials for DynamoDB (if applicable):
   - Ensure your AWS credentials are configured in `~/.aws/credentials`.

4. Run the Flask application:
   ```bash
   python app.py
   ```

### Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Use the **Upload Music** form to select an `.mp3` file and enter a playlist ID.
3. Click **Upload** to upload the music file.
4. Enter a playlist ID in the **Playlists** section and click **Load Music** to view and play the music associated with that playlist.

### Example API Endpoints

- **Upload Music**:
  - **POST** `/upload`: Accepts a music file and playlist ID.

- **Retrieve Music by Playlist**:
  - **GET** `/playlist/<playlist_id>`: Returns the list of music associated with the given playlist ID.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bugs you find.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - For creating the backend framework.
- [jQuery](https://jquery.com/) - For simplifying JavaScript operations.
- [AWS DynamoDB](https://aws.amazon.com/dynamodb/) - For scalable NoSQL database solutions.
