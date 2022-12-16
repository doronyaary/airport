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

Once these are installed, we would need to create a configuration file for Airport. The configration file is a simple JSON text file which must contain several base configrations and then contain one document for each service/andpoint you would like to expose. This is a basic configuration example:

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

**port** - Specifies the port number that Airport will listen to.

**bind** - The binding of the service to your network (use "0.0.0.0" to listen to all interfaces)

**adminenabled** - Should Airport display the admin console (uses the "/manager" URL)

**endpoints** - Lists the API endpoints to listen to (see below more details)


Let's assume for this example, that the config file is called "/etc/airport.conf".
