﻿# GES test automation framework

## Getting Started
 Test automation framework for EnE testing of Google Pixel Devices which includes Python based testing using Robot Framework
### Prerequisites

1. Hardware and OS requirements
   <pre>
   1. Ubuntu 16.04 64 bit
   2. RAM of 4 GB or more
   3. Android device with Android version 8 or 9. Preferably 9.
   </pre>
2. Software
   <pre>
   1. Python 3.5 or higher version must be installed
   2. UI automator must be installed
   </pre>
### Installations

A step by step series of examples that tell you how to get a development env running

###Step1. Clone AMDEF Repository
```shell
   $  git clone http://gitlab.globaledgesoft.com:81/root/Testing_Capability.git
   $  cd Testing_Capability
   $  git checkout -b <branch_name> origin/amdef_dev_phase1
```

###Step2. Check release package contents
```shell
   ~AMDEF]$ ls -l
   Package contains below folders and files:
├── automation
│   ├── inputs
│   │   └── images
│   │       ├── camera
│   │       │   ├── photo
│   │       │   ├── portrait
│   │       │   └── video
│   │       └── voice_recorder
│   ├── resources
│   │   └── platform
│   │       ├── res_audio.robot
│   │       ├── res_camcorder.robot
│   │       ├── res_camera.robot
│   │       ├── res_common.robot
│   │       ├── res_musicplayer.robot
│   │       ├── res_video_player.robot
│   │       └── res_video.robot
│   ├── scripts
│   │   ├── libraries
│   │   │   ├── automation_helpers
│   │   │   │   ├── audio.py
│   │   │   │   ├── camcorder.py
│   │   │   │   ├── camera_config.py
│   │   │   │   ├── common_log.py
│   │   │   │   ├── Common.py
│   │   │   │   ├── core_apis.py
│   │   │   │   ├── environment.py
│   │   │   │   ├── globalconstants.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── logs.py
│   │   │   │   ├── music_config.py
│   │   │   │   ├── MusicPlayer.py
│   │   │   │   ├── reference_coordinate.py
│   │   │   │   ├── VideoPlayer.py
│   │   │   │   ├── Video.py
│   │   │   │   └── YamlUtils.py
│   │   │   └── framework_utils
│   │   │       ├── database_query.py
│   │   │       ├── db_poller.py
│   │   │       ├── device_info.py
│   │   │       ├── framework_logger.py
│   │   │       ├── ftp_file_upload.py
│   │   │       ├── __init__.py
│   │   │       ├── interrupts.py
│   │   │       ├── logger.py
│   │   │       ├── log_utils.py
│   │   │       ├── main_file_queue.py
│   │   │       ├── pythonListener.py
│   │   │       ├── read_copy.json
│   │   │       ├── read.json
│   │   │       ├── ref_image_database.py
│   │   │       ├── runner.py
│   │   │       └── scheduler.py
│   │   └── robot_scripts
│   │       ├── audio.robot
│   │       ├── camcorder.robot
│   │       ├── camera.robot
│   │       ├── Gallery.robot
│   │       ├── music_player_module.robot
│   │       └── video_player.robot
│   └── variables
│       ├── android_version_8
│       │   └── LGE
│       │       └── Nexus5X
│       │           └── bullhead
│       │               └── uiconfig.yaml
│       ├── android_version_9
│       │   └── Google
│       │       ├── Pixel
│       │       │   └── sailfish
│       │       │       └── uiconfig.yaml
│       │       └── PixelXL
│       │           └── marlin
│       │               └── uiconfig.yaml
│       ├── variables_common.yaml
│       └── variables_framework.yaml
├── Configuration-FW.txt
├── Installer.sh
└── README.md
```

###Step3. Installing dependencies packages for Gats framework
```shell
  ~AMDEF]$./Installer.sh
```

###Step4. Updating uiconfig.yaml with required data before execution
Update **uiconfig.yaml** files with Android Device details, Timeout values and Directory Paths.    
```shell
   ~AMDEF] cd automation/variables/android_version_9/Google/Pixel/sailfish/
   ~AMDEF] cd automation/variables/android_version_9/Google/PixelXL/marlin/
```   
Edit the device_id, test cases list in read.json.
```shell   
   ~/AMDEF]$ gedit read.json 
```

   Connect the Android device, on which testing need to be performed.
   
Note:
The DEVICE_ID can be obtained by executing the below command:
```shell   
   adb devices 
```

###Step6. Execute the scheduler to start the automation
   1. Navigate to ```framework_utils```
```shell 
    cd GATS/automation/scripts/libraries/framework_utils
```
   2. Make sure the Android device is connected and execute the following command:
```shell
   ~/framework_utils]$ python3 scheduler.py
```

    
##Uninstalling the packages installed 
  1. Execute the following command to uninstall the tool.
```shell
   ~GATS]$./Installer.sh clean
```
