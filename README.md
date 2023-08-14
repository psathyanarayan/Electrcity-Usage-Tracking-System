# Kerala Electricity Tracking System

Electrify is a Django project designed to compute the electricity readings for each household in the state of Kerala. It provides features to track and analyze electricity consumption data, making it easier for users to monitor and manage their energy usage.

## Overview

The project aims to calculate the electricity usage and cost based on the readings provided by users. It offers various functionalities including:

- Calculating total electricity units and cost over the last two months.
- Providing data for the last 24 hours.
- Inserting new electricity consumption data.
- Fetching all consumption data from the database.
- Plotting graphical representations of consumption data.

## Key Components

### `views.py`

This file contains Django ViewSets that handle different functionalities of the application. The key ViewSets include:

- `TotalUnit`: Calculates the total units and cost of electricity over the last two months.
- `Last24HoursData`: Retrieves the total units and cost of electricity for the last 24 hours.
- `InsertData`: Inserts new electricity consumption data into the database, calculating units and cost.
- `FetchAllData`: Fetches all consumption data from the database.
- `DataGraphPlotter`: Generates and serves graphical plots of electricity consumption data.
- `DataFilterGraphPlotter`: Creates filtered graphical plots based on a specified date range.

### `urls.py`

The `urls.py` file defines the routing for the Django project. The project uses Django's built-in `router` to handle routing for various ViewSets. Notable routes include:

- `/api/admin/`: Django admin interface.
- `/api/db/`: Root URL for the project's APIs.

Additional routes are defined for various ViewSets, such as `/api/db/total-unit/` for the `TotalUnit` ViewSet and so on.

## Usage

To use the Electrify project, you can perform actions like:

- Fetching total units and cost data.
- Inserting new consumption data.
- Generating and viewing graphical plots of consumption data.

Refer to the project's specific ViewSets and URLs for detailed usage instructions.

## Installation

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your Django environment, database, and configuration.
4. Run the Django development server using `python manage.py runserver`.

## Contributing

Contributions to the project are welcome! Feel free to open issues, submit pull requests, or improve the documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
