# Social-Network-Application
## Overview
The Social Network Application is a Django-based platform that enables users to connect, send friend requests, and interact with each other. Whether you’re building a small community or a full-fledged social network, this application provides essential features for user engagement.

## Features
### User Registration and Authentication:
Users can sign up with their email, username, and password.</br>
Authentication is handled via both session-based and token-based methods.
### Friend Requests:
Users can send friend requests to other users.</br>
Pending friend requests are tracked, and users can accept or reject them.
### User Search:
Search for users by email, username, or first name.</br>
The search functionality allows users to find and connect with others.
### List Friends:
Retrieve a list of friends for the authenticated user.</br>
Friends are users who have accepted friend requests.
### Rate Limiting:
Friend requests are rate-limited to prevent abuse (e.g., max 3 requests per minute).
## Installation
Follow these steps to set up the application locally:

#### Clone the Repository:
```
git clone https://github.com/your-username/social-network.git
cd social-network
```

#### Create a Virtual Environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies:
```
pip install -r requirements.txt
```
### Database Setup:
Update the DATABASES configuration in settings.py to match your MySQL database settings.
#### Run migrations:
```
python manage.py migrate
```

#### Run the Development Server:
```
python manage.py runserver
```

### Access the Application: Open your browser and navigate to http://localhost:8000/

#### NOTE: you can find samle data in ```API_JSON_data_Collectin.json``` file and You can find exmple in  ```API Examples.txt```
API Endpoints</br>
#### User Registration
Endpoint: POST /api/signup/</br>
Description: Register a new user.</br>
Request Body:

JSON
```
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword",
  "first_name": "New",
  "last_name": "User"
}
```

#### User Login
Endpoint: POST /api/login/</br>
Description: Authenticate and obtain an access token.</br>
Request Body:
JSON
```
{
  "username": "newuser",
  "password": "securepassword"
}
```

#### Response:
JSON
```
{
  "token": "your-access-token"
}
```

#### User Search
Endpoint: GET /api/search/?search=<keyword></br>
Description: Search for users by email, username, or first name.</br>
Example: GET /api/search/?search=johndoe</br>
### Friend Requests
#### Send Friend Request:
Endpoint: POST /api/friend-request/</br>
Request Body:
JSON
```
{
  "to_user_id": 2
}
```

#### Accept or Reject Friend Request:
Endpoint: PUT /api/friend-request/</br>
Request Body (Accept):
JSON
```
{
  "request_id": 1,
  "action": "accept"
}
```

JSON
```
{
  "request_id": 1,
  "action": "reject"
}
```

#### List Friends
Endpoint: GET /api/friends/</br>
Description: List friends of the authenticated user.</br>
#### Pending Requests
Endpoint: GET /api/pending-requests/ </br>
Description: List pending friend requests.</br>
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

Feel free to customize this README further by adding deployment instructions, additional features, or any other relevant information😊🚀