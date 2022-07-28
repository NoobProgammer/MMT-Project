# MMT-Project

## Introduction

A basic networking course Python project to demonstrate the use of sockets and the TCP Protocol.

## Overview

A simple booking application that allows users to book a table for a restaurant. The application has the following features:

-   The server can accept multiple connections
-   Implements a database to store the menu and the bookings
-   Users can view the menu (with images) and make bookings
-   Implements a payment system to allow users to pay for their bookings

## How to run the application?
1. Locate to server folder and run the db.py to populate the database:
    ```
    python3 db.py
    ```
2. Run the server:

    ```
    python3 server.py
    ```
3. Locate to the client folder and run the App.py file on a different terminal:

    ```
    python3 App.py
    ```
4. Type in the ip address and the port number of the server:

    ```
    Enter the server IP: *IP goes here*
    Enter the server port: *PORT goes here*
    ```

## Contributors:

Many thanks to the following people for their contributions:

-   **Nguyen Ho Trung Hieu** - 20126038
-   **Vu Hoai Nam** - 20126045
-   **Truong Do Truong Thinh** - 20126056