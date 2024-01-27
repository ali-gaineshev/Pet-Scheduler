
# Family Pet Scheduler

Family Pet Scheduler is a monolithic Flask application built in Python to help families manage and organize pet-related activities. Whether it's scheduling walks, feeding times, or veterinary appointments, this app simplifies the coordination of tasks between family members related to family pets (in theory)

## Features

- **Simple Interface**: Easily manage and view scheduled tasks
- **Activity Tracking For All Members**: Keep track of various pet-related activities such as walks, feeding, grooming, and veterinary appointments for all members.
- **Family Collaboration**: Collaborate with family members to ensure everyone is on the same page when it comes to pet care. Members are able to assign tasks to themselves, unassign or complete them after.
- **Digital Ocean Hosting**: The application is hosted on Digital Ocean.
- **Postgres Database**: Utilizes Postgres as the database to store and retrieve scheduling information.

## Getting Started

### Prerequisites

- Python : 3.11 
- psql
- for the rest see below
### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ali-gaineshev/Pet-Scheduler.git
    cd pet-scheduler
    ```
2. Set up virtual enivronment

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    ```
    cd db
    createdb -U <username> pet_scheduler_db
    psql -U <username> -d pet_scheduler_db -f db.sql
    psql -U <username> -d pet_scheduler_db
    ```
    - Create `db_secret.txt` file with your database credentials.

4. Run the application:
    ```bash
    python3 main.py
    ```

5. Access the application in your web browser at `http://localhost:5000`.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to help improve this project.

## TO DO

1. Add an interactive calendar. At this moment, this is just a bunch of text with dates. 
2. More error catching
3. Update the design