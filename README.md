SQLite
SQLite is a lightweight, self-contained, serverless, zero-configuration SQL database engine. It is widely used for its simplicity and ease of integration into various applications. Unlike other SQL databases, SQLite does not require a separate server process. Instead, it stores the entire database as a single file on disk, making it an excellent choice for applications that need a small, fast, and portable database.

Key Features:

Self-Contained: All data is stored in a single file, making it easy to back up, share, or transfer.
Serverless: No separate server process is required, simplifying deployment and reducing overhead.
Zero Configuration: No setup or administration is needed, making it ideal for applications where ease of use is crucial.
ACID Compliance: Supports atomic transactions, ensuring data integrity.
Cross-Platform: Works on many different platforms, including Windows, macOS, Linux, and more.


********************************************************************************************************************************************************************************
Project Description:
(Client and Admin)
In this project, we're developing a simple web application using Flask, a lightweight web framework for Python, and SQLite as the database. The application has two main components: Admin Dashboard and Client Dashboard.

Admin Dashboard
Functionality:
Admins can upload PDF files and enter a display name for each file.
Admins can also upload YouTube video links along with a display name.
Uploaded files and video links are stored in the SQLite database, and the files are saved in the 'uploads' directory.
Admins can view all uploaded files and video links, download PDFs, and delete any file or video link.
Security: Access is restricted by an admin password.
Client Dashboard
Functionality:
Clients can view the list of available PDFs and YouTube video links uploaded by the admin.
Clients can view PDFs directly in the browser or download them.
Clients can watch the YouTube videos by clicking on a link.
Technical Details:

Backend: Flask is used to handle HTTP requests, render HTML templates, and manage the SQLite database.
Frontend: HTML templates are used for the admin and client interfaces, with Bootstrap for styling.
Database: SQLite is used to store information about uploaded files and video links, including their display names.
This project is a basic example of a content management system (CMS) with file uploads, video links, and restricted access for administrative functions.
