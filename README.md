# py-diner

A simple booking application that allows users to book a table for a restaurant. This project was done as part of the course work for the module CSC10008 - Networking at HCMUS. This project is built with Python to demonstrate the use of sockets and the TCP Protocol.

## Features

The application has the following features:

-   The server can accept multiple connections.
-   Implements built-in SQLite database to store the menu and the bookings.
-   Users can view the menu (with images) and make bookings.
-   Implements a payment system to allow users to pay for their bookings

## Quick start

1. Locate to server folder and run the db.py to populate the database:

    ```bash
    python3 db.py
    ```

3. Run the server:

    ```bash
    python3 server.py
    ```

4. Locate to the client folder and run the App.py file on a different terminal:

    ```bash
    python3 App.py
    ```
    
5. Type in the ip address and the port number of the server:

    ```bash
    Enter the server IP: *IP goes here*
    Enter the server port: *PORT goes here*
    ```

## Contributions:

Many thanks to the following people for their contributions:

-   [Vu Hoai Nam](https://github.com/namhoai1109)
-   [Truong Do Truong Thinh](https://github.com/td2thinh)
