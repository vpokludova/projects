# Tram Timetables Application

## Overview

This application provides a user-friendly interface for accessing tram timetable information. It allows users to view the full timetable for selected tram lines, departures from a specified stop, and the next ten departures from a chosen stop at a selected time. The program is designed for ease of use, offering dropdown menus for tram stops, days, hours, minutes, and actions. Outputs are displayed within the same window, ensuring a seamless user experience.

## Features

- **Graphical User Interface:** Utilizes dropdown menus for selection and displays output in a textbox with scrolling capabilities.
- **Multiple Viewing Options:** Users can view entire tram timetables, specific departures from a stop, or upcoming departures.
- **Flexible Time Selection:** Supports selection of day, hour, and minute for detailed timetable inquiries.

## Usage

1. **Start the Application:** Upon launching, the program automatically selects the first option in each dropdown menu.
2. **Make Your Selections:** Choose a tram stop, day, time, and action from the dropdown menus.
3. **View the Results:** Press the "Enter" button to execute the selected action and view the results in the application window.

## Data Representation and Algorithm

The program is optimized for memory efficiency and quick access to timetable data:

- **Minimal Data Storage:** Only essential tram departure times and durations are stored.
- **Efficient Data Representation:** Input data includes departures from terminal stops and ride durations to each stop.
- **Quick Timetable Generation:** The chosen algorithm efficiently generates timetables based on user selections.

## Programming Details

- **Classes and Methods:** Includes classes for handling time calculations, data storage, and timetable generation.
- **Data Preparation:** Input data is structured to facilitate easy timetable creation and modification.
- **Graphical Output:** Utilizes wxWidgets for the graphical interface, offering a clear and intuitive user experience.


