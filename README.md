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

Once these are installed, we would need to create a configuration file for Airport.
