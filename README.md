# EPS USER GUI - ALBA SYNCHROTRON

This is a GUI to display EPS-PLC information for users

You can open a taurus trend with the attributes that you select, filter the interlock states

This is the [documentation}(https://drive.google.com/file/d/1aZXq4-Z6I6gcxN3wCQvvx5R5tbDZpj_K/view?usp=sharing) for this project.

**__version__ = "1.0.0"**

Application
-----------

- [BPM_USER_GUI](https://git.cells.es/controls/eps-gui)


Requirements
-------------

- [Taurus](https://taurus.readthedocs.io/en/3.7.2/users/index.html)
- CSV

Installation
------------
The latest development version can be obtained from the git repository:

    git clone https://git.cells.es/controls/eps-gui

Conda installation example
--------------------------

> 1 - Create a new conda environment named conda_env for instance:

`conda create -n conda_env`

> 2 - Activate the environment

`conda activate conda_env`

[...]
    
Dependencies using conda and pip
--------------------------------

### Required:

- conda packages:
    * `python=3.9`
    * `PyQt5`

How to test the GUI
-------------------

This GUI is working at ctmodbuslabs machine. To launch it:

> 1 - Open a ssh connection to ctmodbuslabs as sicilia user

`myuser@mymachine $ ssh -X sicilia@ctmodbuslabs`

> 2 - Navigate to the code folder at '/src/eps-gui'

`sicilia@ctmodbuslabs:~> cd src/eps-gui/`

> 3 - To launch the GUI:

`sicilia@ctmodbuslabs:~/src/eps-gui> python Main0.1.py `



LOCAL:
export TANGO_HOST=alba02.cells.es:10000



