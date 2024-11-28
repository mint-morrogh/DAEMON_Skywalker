# Skywalker: Automated Astrophotography 

## Description
Skywalker is a Python script designed to automate the joining of astrophotography missions on [Slooh](https://www.slooh.com/). The script ensures missions are captured even when the computer is asleep or logged out. It operates as a system-level daemon, requiring proper permissions and system configurations to wake up the computer and execute the script. Mission details are logged into a `mission.log` file for easy tracking.

## Installation

1. **Install Dependencies:**
   Ensure you have Python 3.x installed along with the required libraries. Install dependencies using:
   ```sh
   pip install playwright
   playwright install
   ```
   
2. **Set Up Configuration:**
   Create a config.py file in the same directory as the script and add your Slooh login credentials:
  ```sh
  USERNAME = "your-email@example.com"
  PASSWORD = "yourpassword"
  ```

3. **Set Up Permissions:**
   Ensure the script has the appropriate read and write permissions:
   ```sh
   chmod +x skywalker.py
   ```
   
4. **System Daemon Setup:**
   Schedule the script to run at a specific time using a system-level task scheduler (e.g., cron on macOS/Linux or Task Scheduler on Windows). For macOS
   ```sh
   sudo pmset schedule wakeorpoweron "03:00:00"
   ```
   Then add either a cronjob, a launch daemon on Mac, whatever you choose to set this script to run at your interval, in the above case, I would set it for 03:01:00

## Usage

**Daemonized Execution**  
Configure the script to run automatically via the system-level scheduler (see Installation). or run it locally

**Logs**  
- `skywalker.log`: Detailed execution logs for debugging.
- `mission.log`: Logs missions that have been joined, with timestamps.

## Configuration/Settings

### `config.py`
The `config.py` file stores your Slooh username and password, you would just add this to the root directory where your python script lives:
USERNAME = "your-email@example.com"
PASSWORD = "yourpassword"


   
