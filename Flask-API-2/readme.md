# Flask Link Bookmarking API

This project is a Flask-based API that allows users to save and manage bookmarks for links they want to check out in the future. The API provides endpoints for user account creation, login, bookmark creation, retrieval, and statistics tracking.

## Features

- User Registration: Users can create new accounts by providing their credentials.
- User Login: Registered users can log in to the API and receive access and refresh tokens.
- Token Authentication: Access to protected endpoints requires a valid access token.
- Token Refresh: Users can refresh their access token using a refresh token to stay logged in.
- Bookmark Creation: Users can add bookmarks by providing a long URL, which is shortened and stored.
- Bookmark Retrieval: Users can retrieve their list of bookmarks, including the short URL and visit statistics.
- URL Shortening: Long URLs are automatically shortened by the API, allowing for better tracking of visits.
- Visit Tracking: The API keeps track of the number of times a bookmarked URL has been visited.
- API Documentation: The API is documented using Swagger, enabling easy integration with other developers' applications.

## Requirements

To run the Flask Link Bookmarking API, the following dependencies are required:

- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-Restful
- Swagger UI (for documentation)

## Installation

- Clone the repository: git clone url
- Navigate to the project directory: cd flask-link-bookmarking-api
- Install the dependencies: pip install -r requirements.txt

```bash
pip install -r requirements.txt
```

## Usage

- Start the API server: python app.py
- Access the API documentation at http://localhost:5000/docs to explore the available endpoints and their usage.
- Use tools like Postman to make requests to the API endpoints and interact with the functionality.

## Initial Work

- [cryce truly](https://github.com/CryceTruly)

We hope you find this project useful and enjoy working with the Flask Link Bookmarking API!
