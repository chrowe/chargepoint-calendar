# ChargePoint to Google Calendar

This project uses the `python_chargepoint` package to download home charging sessions that finished since the last download and add them to a Google Calendar. GitHub Actions is used to automate the process.

## Setup

1. Clone the repository
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google Calendar API credentials and save the `credentials.json` file in the root directory. [Instructions to get `credentials.json`](docs/get_credentials.md)
4. Set up environment variables in GitHub repository secrets:
    - `CHARGEPOINT_USERNAME` - Your ChargePoint username
    - `CHARGEPOINT_PASSWORD` - Your ChargePoint password
    - `GOOGLE_CALENDAR_ID` - Your Google Calendar ID. [Instructions to get your Google Calendar ID](docs/get_calendar_id.md)

## Usage

The script will automatically run daily using GitHub Actions and update your Google Calendar with the latest home charging sessions.
