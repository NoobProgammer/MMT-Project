# MMT-Project

## Introduction

A basic networking course Python project to demonstrate the use of sockets and the TCP Protocol.

## Overview

A simple booking application that allows users to book a table for a restaurant. The application has the following features:
- The server can accept multiple connections
- Implements a database to store the menu and the bookings
- Users can view the menu (with image) and make bookings
- Implements a payment system to allow users to pay for their bookings

*LATER: Add screenshots of the application*

## How to run the application?

The application comes with a pre-populated menu in the database and images of the menu. Custom run is not implemented yet *(will update later)*

1. Run the server:

    ```
    cd ./server
    python3 server.py
    ```
2. Run the client on a different terminal:

    ```
    cd ./client
    python3 App.py
    ```
3. Type in the ip address and the port number of the server:

    ```
    Enter the server IP: *IP goes here*
    Enter the server port: *PORT goes here*
    ```

## Contributors:

Many thanks to the following people for their contributions:

- **Nguyen Ho Trung Hieu** - 20126038
- **Vu Hoai Nam** - 20126045
- **Truong Do Truong Thinh** - 20126056