## What is this?

This repository simplifies the distribution and activation of images towards switches through Cisco Catalyst Center.

Managing upgrades across multiple sites can be tedious, requiring manual selection of sites, devices, and initiating the upgrade process. This script automates the process by retrieving all switches at a specified site, checking for outdated firmware, and upgrading devices as needed.

You will need to run a CRON job to check if it's time to upgrade specific site(s), provided in the 'schedule.json'.

## TODO

- [x] Authentication toward CCC and token usage
- [x] Convert site hierarchy name ("Global/PEG2/DEV" for example) to SiteID 
- [x] Fetch all switches from that site
- [x] Check if software is outdated (based on the golden image that's tagged on that site from Catalyst Center - manual step)
- [x] Distribution of images towards the devices
- [ ] Change distribution from bulk to individual
- [ ] Add activation function

## How to use?
### Python virtual env
Using a Python virtual environment ensures dependency isolation and prevents conflicts between project-specific packages and system-wide installations.

Create new Python venv:

```bash
python3 -m venv ccc-swim-env
```

Go in the venv

```bash
source ccc-swim-env/bin/activate
```

Navigate to the repo you downloaded/cloned and install packages:

```bash
pip install -r requirements.txt
```

### .env file
Create an .env file in main directory with your Catalyst Center information:

```bash
CCC_BASE_URL=https://10.10.10.10
CCC_USERNAME=admin
CCC_PASSWORD=password
SCHEDULE_FILE=/../file.json (path towards the file)
```

### CRON 
Next, you need to find 3 paths:
1. Search for your Python installation path in Termnial: 'which python3'
2. The path towards your cron_job.py 
3. The path towards your cron_job.log (file does not need to exist)

In terminal, open the crontab file and add the job.
```bash
'crontab -e'
```
Add the job:

```bash
* * * * * /Users/wdeprins/Desktop/sdaac/ccc-swim-venv/bin/python3 /Users/wdeprins/Desktop/sdaac/ccc-swim/cron.py >> /Users/wdeprins/Desktop/sdaac/ccc-swim/cron.log 2>&1
```
### Disclaimer

This script is provided "as is" without any warranties of any kind, either express or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The author does not warrant that the script will be error-free or that it will meet the specific requirements of the user. The user assumes all responsibility for the use of this script and any results obtained from it. In no event shall the author be liable for any damages, including but not limited to direct, indirect, incidental, special, or consequential damages arising out of the use or inability to use this script. Users are advised to test the script thoroughly before relying on it in a production environment.