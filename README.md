![Alt text](airport.png?raw=true)

Airport is a lightweight API endpoint manager written in Python. Its main purpose is to enable simple exposure of API endpoints when each endpoint invokation actually executes a shell command in the background and returns the output.

## General Overview
Airport is released under the MIT license and was developed by Doron Yaary (@MaorSystems.co.il) in order to solve some IT/Ops issues that can be easily resolved by a simeple API running a shell command in the background. Running a shell command gives you the chioce of which code you want to run by either calling compiled programs or running a script file with the right preproccessor (e.g. #!/bin/bash for example). Airport will execute the command and return the standard output response. Its important to mention that the execution rights belong to the user that runs Airport so if you execute it with root you need to carefully consider the risks.

## Installation & Configuration
Airport is built using Python3 so you need to perform several steps. Though there are no RPMs at this stage, it is on my roadmap for later. The installation steps where performed and tested on RockyLinux 8. Let's start with making sure you already have python:

```bash
python3 -V
```

You should see a response with the version of Python you have

```bash
Python 3.9.13
```

If you need to install python3, please install it using YUM or DNF:

```bash
dnf install python3 python3-pip
```

Then, we will need to install Flask using PIP. You can do it by executing the following command:

```bash
pip install flask
```

Once these are installed, we would need to create a configuration file for Airport. The configration file is a simple JSON text file which must contain several base configrations and then contain one document for each service/andpoint you would like to expose. Let's assume for this example, that the config file is called "/etc/airport.conf" This is a basic configuration example:

```json
{
  "port": "8080",
  "bind": "0.0.0.0",
  "adminenabled": "1",
  "endpoints": [
    {
      "path": "/",
      "type": "cmd",
      "command": "/usr/bin/dp_something.sh",
      "enabled": "1",
      "method": "GET",
      "mime": "text/plain",
      "silent": "1",
      "name": "General Webservice Request"
    }
  ]
}
```

Lets go over the basic parameters:

- **port** - Specifies the port number that Airport will listen to.
- **bind** - The binding of the service to your network (use "0.0.0.0" to listen to all interfaces)
- **adminenabled** - Should Airport display the admin console (uses the "/manager" URL)
- **endpoints** - Lists the API endpoints to listen to (see below more details)

The "endpoints" represent an array of JSON documents that describes the endpoints and commands that will be executed once consumed by a web request. Let's review the parameters/keys for each document:

- **path** - Specifies the URL that will be used/listened to.
- **type** - The type of the action that will be performed. Currently supporting "cmd". More options will be added in future versions.
- **command** - The shell command to execute (runs with the linux permissions of the user that runs Airport)
- **enabled** - Determines if the service is available, accepts "1" or "0".
- **method** - The web request method. Currently accepts only "GET" or "POST" or "GET,POST". Other methods will be added in the future.
- **mime** - The response mime type to return.
- **silent** - If silent, than the standard output of the shell command is not returned back at all.
- **name** - The general name of this endpoint. More usefull for display purposes on the manager web site.

In order to start the service, you would need to run Airport in one of two ways. As I mentioned before, you can always take the code itself and run it thought my roadmap is to create an RPM package for ease of installation. Let's examine the two options.

### Running from source code

You can always just use the python3 executable to run Airport in the following way:

```bash
python3 airport.py --config=/etc/airport.conf
```

Once the binary would be available, you can run Airport like this as well:

```bash
airport --config=/etc/airport.conf
```

Its important to mention that the "--config" option is mandatory and Airport has no default for this parameter. That is done in order to prevent common errors or to enable Airport to be executed in parallel with different configurations and ports in the same machine if needed.

## Airport Manager
if you have configured the "adminenabled" to "1" than the url "/manager" will be exposed with a very basic and simple information about the system usage. See the following example:

![Alt text](airportmanager2.png?raw=true)

The top four numbers include the following:

- **Valid Calls Count** - this number indicates the count of the calls that where validated and executed (where URLs matched)
- **Invalid Calls Count** - this number indicates the count of the calls that didn't match any valid endpoint
- **Active Endpoints** - the number of the configured endpoints in the configuration file
- **Uptime** - the uptime minutes of the Airport service

Then, you will see a list of endpoints the the followiing columns:

- **Path/URL** - The URL/web path of the published endpoint
- **Name/Description** - The value of the key "name" in the endpoint document in the JSON configuration
- **Methods** - The allowed methods for this endpoint (either GET or POST or GET,POST)
- **Enabled** - Shows if the endpoint is enabled or not

## Valid Use Cases
TBD


