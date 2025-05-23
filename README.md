## IDOR Vulnweb
This repository contains a vulnerable Flask web application showcasing an Insecure Direct Object Reference (IDOR). It is intended for CTF practice and educational demonstrations.

### Overview
The web application simulates a student directory where users can log in, view profiles, download transcripts, export personal data, and send messages to an admin. However, it contains an IDOR vulnerability on profile-based endpoints allowing an authenticated user to access or export any other user’s data by tampering with the user_id in the URL.

### Deployment
1. Clone this repository
```bash
git clone https://github.com/shinyxn/IDOR-Vulnweb
```

2. Configure Environment variables in docker-compose.yml for change flag and port
```
services:
  web:
    build: .
    ports:
      - "56789:5000"  ---> Change port if necessary
    restart: unless-stopped
    environment:
      - SECRET_KEY=supersecretkey ----> Flask secret key
      - FLAG=FLAG{FAKE_FLAG_FOR_TESTING} --> Change this
```

3. Build and run the challenge with Docker Compose
```bash
docker-compose up --build -d
```

The web service will be available on http://localhost:56789.

4. Stop the service
```bash
docker-compose down
```

### Running the Demo
1. Navigate to http://localhost:56789.

2. Log in with any of the provided user credentials (see table below).

| User ID | Username | Password |
| ------- | -------- | -------- |
| 1       | `agus`   | `agus123` |

3. Explore your own profile and functionality.

