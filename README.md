
## Project Overview

This is a lightweight, full-stack appointment scheduling application built to help small teams manage their daily schedules. It provides a simple, interactive board to view, add, update, complete, and cancel appointments. The backend is powered by Python and Flask, utilizing SQLite for data management.

### Features and Capabilities

* **Full Scheduling Control:** Users can efficiently create, read, update, and cancel daily appointments.


* **Smart Conflict Detection:** The backend strictly prevents two appointments from using the same time slot.


* **Dynamic Filtering:** The dashboard allows users to easily filter active or historical records by date and status.


* **Status Tracking:** Appointments can be seamlessly marked as completed to log finished tasks.


* **Instant Review:** The application automatically seeds sample appointments upon the first database creation so the board can be reviewed immediately.



### Technical Assumptions

* **Cancellation Handling:** Cancelled appointments remain visible on the board and are clearly marked as cancelled. Once cancelled, they automatically release their reserved time slot to allow new bookings.


* **Completion State:** Completed appointments permanently lock their time slot to retain accurate historical booking integrity.
* **Architecture Scope:** The system logic is designed around a single shared team calendar where concurrent, overlapping active tasks are not permitted.



Local Setup Guide
Clone the repository locally using git clone [https://github.com/Rupx003/appointment-board-task.git](https://github.com/Rupx003/appointment-board-task.git).

Navigate into the newly created directory and generate a virtual environment by running python -m venv venv.

Activate the virtual environment (venv\Scripts\activate on Windows, or source venv/bin/activate on macOS/Linux).

Install all required project dependencies by running pip install -r requirements.txt.

Start the local Flask server by executing python app.py.

Open your preferred web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the application.
