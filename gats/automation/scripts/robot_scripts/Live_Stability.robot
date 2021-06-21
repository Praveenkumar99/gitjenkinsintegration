*** Settings ***
Test Timeout    65 minutes
Library     BuiltIn
Library     Collections
Resource    ${EXECDIR}/../../../resources/platform/res_common.robot
Resource    ${EXECDIR}/../../../resources/cellular/res_common.robot
Variables   ${dict.yaml}/uiconfig.yaml


Test Setup  Run Keywords    Setup Log
#...  AND     Start Modem Log   ${yamlData}    ${log_type}

Test Teardown  Run Keywords    Set Iteration Path       ${dict.robot_log_path}
#...  AND     Stop Modem Log    ${yamlData}    ${log_type}
...  AND     Remove Log Handler

*** Variables ***
#&{dict}     project=${1}     milestone=${2}     session=${3}     device=${4}    yaml=${5}    test_iter_count=${6}    testcase_name_and_iter_path=${7}    iteration_path=${8}
#&{dict}     project=${1}     milestone=${2}     session=${3}     device=${4}    test_iter_count=${5}    testcase_name_and_iter_path=${6}    iteration_path=${7}    suite=${8}
${log_type}    0

*** Test Cases ***
TC_Live_Stability_001
    [Documentation]    Performing Volte Call1
    [Tags]            TC_Live_Stability_001
    Volte Call MO    TC_Live_Stability_001     ${yamlData}    ${log_type}

TC_Live_Stability_002

    [Documentation]    Performing Volte Call2
    [Tags]            TC_Live_Stability_002
    Volte Call MT    TC_Live_Stability_002     ${yamlData}    ${log_type}    

TC_Live_Stability_003

    [Documentation]    Performing Volte Hold Call1
    [Tags]            TC_Live_Stability_003
    Volte Call Hold MO    TC_Live_Stability_003     ${yamlData}    ${log_type}    
 

TC_Live_Stability_004

    [Documentation]    Performing Volte Hold Call2
    [Tags]            TC_Live_Stability_004
    ${result}    Volte Call Hold MT    TC_Live_Stability_004     ${yamlData}    ${log_type}    
  

TC_Live_Stability_005

    [Documentation]    Performing Volte Swap Call1
    [Tags]            TC_Live_Stability_005
    ${result}    Volte Call Swap1    TC_Live_Stability_005     ${yamlData}    ${log_type}    
  

TC_Live_Stability_006

    [Documentation]    Performing Volte Swap Call2
    [Tags]            TC_Live_Stability_006
    ${result}    Volte Call Swap2    TC_Live_Stability_006     ${yamlData}    ${log_type}    
  

TC_Live_Stability_007

    [Documentation]    Performing Volte Conf Call1
    [Tags]            TC_Live_Stability_007
    ${result}    Volte Call Conf1    TC_Live_Stability_007     ${yamlData}    ${log_type}    
  

TC_Live_Stability_008

    [Documentation]    Performing Volte Conf Call2
    [Tags]            TC_Live_Stability_008
    ${result}    Volte Call Conf2    TC_Live_Stability_008     ${yamlData}    ${log_type}    
  

TC_Live_Stability_009

    [Documentation]    Performing Volte Long Call
    [Tags]            TC_Live_Stability_009
    ${result}    Volte Call Grade1    TC_Live_Stability_009    ${yamlData}    ${log_type}    
  

TC_Live_Stability_010
    [Documentation]    Performing Volte Call Rejection At MT Side
    [Tags]            TC_Live_Stability_010
    ${result}    Volte Call Grade2    TC_Live_Stability_010     ${yamlData}    ${log_type}    
  


TC_Live_Stability_011
    [Documentation]    Performing Long Volte Conf Call1
    [Tags]            TC_Live_Stability_011
    ${result}    Volte Call Grade3    TC_Live_Stability_011     ${yamlData}    ${log_type}    
  

TC_Live_Stability_012
    [Documentation]    Performing Volte Call Upgrade from MT Downgrade from MO
    [Tags]            TC_Live_Stability_012
    ${result}    Volte Call Grade4    TC_Live_Stability_011     ${yamlData}    ${log_type}
  

TC_Live_Stability_013
    [Documentation]    Performing volte call and sending sms at mo side
    [Tags]            TC_Live_Stability_013
    Volte Call Send Sms MO    TC_Live_Stability_013    ${yamlData}    ${log_type}
  

TC_Live_Stability_014
    [Documentation]    Performing volte call and sending sms at mt side
    [Tags]            TC_Live_Stability_014
    Volte Call Send Sms MT    TC_Live_Stability_014    ${yamlData}    ${log_type}
  

TC_Live_Stability_015
    [Documentation]    Performing volte call and receive vt call
    [Tags]            TC_Live_Stability_015
    Volte Call Receive VT Call    TC_Live_Stability_015    ${yamlData}    ${log_type}
  

TC_Live_Stability_016
    [Documentation]     Performing volte call make vt call
    [Tags]            TC_Live_Stability_016
    Volte Call Make VT Call    TC_Live_Stability_016    ${yamlData}    ${log_type}
  

TC_Live_Stability_017
    [Documentation]    Receive vt call at mo
    [Tags]            TC_Live_Stability_017
    VT Call MO    TC_Live_Stability_017    ${yamlData}    ${log_type}
  

TC_Live_Stability_018
    [Documentation]    Receive vt call at mo
    [Tags]            TC_Live_Stability_018
    VT Call MT    TC_Live_Stability_018    ${yamlData}    ${log_type}
  

TC_Live_Stability_019
    [Documentation]    Performing VT call put call on hold at Mo side
    [Tags]            TC_Live_Stability_019
    VT Call Hold MO    TC_Live_Stability_019    ${yamlData}    ${log_type}
  

TC_Live_Stability_020
    [Documentation]    Performing VT call put call on hold at MT side
    [Tags]            TC_Live_Stability_020
    VT Call Hold MT    TC_Live_Stability_020    ${yamlData}    ${log_type}
  

TC_Live_Stability_021
    [Documentation]    Performing VT Call Swap call 1
    [Tags]            TC_Live_Stability_021
    VT Call Swap1    TC_Live_Stability_021    ${yamlData}    ${log_type}
  

TC_Live_Stability_022
    [Documentation]    Performing VT Call Swap call 2
    [Tags]            TC_Live_Stability_022
    VT Call Swap2   TC_Live_Stability_022    ${yamlData}    ${log_type}
  

TC_Live_Stability_023
    [Documentation]    Performing VT Call Conf 1
    [Tags]            TC_Live_Stability_023
    VT Call Conf1    TC_Live_Stability_023    ${yamlData}    ${log_type}
  

TC_Live_Stability_024
    [Documentation]    Performing VT Call Conf 2
    [Tags]            TC_Live_Stability_024
    VT Call Conf2    TC_Live_Stability_024    ${yamlData}    ${log_type}
  

TC_Live_Stability_025
    [Documentation]    Performing vt call and up/down grade from mo
    [Tags]            TC_Live_Stability_025
    VT Call Grade MO    TC_Live_Stability_025    ${yamlData}    ${log_type}
  

TC_Live_Stability_026
    [Documentation]    Performing vt call and up/down grade from mt
    [Tags]            TC_Live_Stability_026
    VT Call Grade MT    TC_Live_Stability_026    ${yamlData}    ${log_type}
  

TC_Live_Stability_027
    [Documentation]    Performing vt call up and down grade
    [Tags]            TC_Live_Stability_027
    VT call Grade1    TC_Live_Stability_027    ${yamlData}    ${log_type}
  

TC_Live_Stability_028
    [Documentation]    Performing vt call up and down grade
    [Tags]            TC_Live_Stability_028
    VT call Grade2    TC_Live_Stability_028    ${yamlData}    ${log_type}
  



TC_Live_Stability_029
    [Documentation]    Performing VT Call Send SMS AT MO Side
    [Tags]            TC_Live_Stability_029
    VT Call Send Sms MO    TC_Live_Stability_029    ${yamlData}    ${log_type}
  

TC_Live_Stability_030
    [Documentation]    Performing VT Call Send SMS AT MT Side
    [Tags]            TC_Live_Stability_030
    VT Call Send Sms MT    TC_Live_Stability_030    ${yamlData}    ${log_type}
  

TC_Live_Stability_031
    [Documentation]    Performing VT call and receive Volte call
    [Tags]            TC_Live_Stability_031
    VT Call Recv Volte Call    TC_Live_Stability_031    ${yamlData}    ${log_type}
  

TC_Live_Stability_032
    [Documentation]    Performing VT call and make Volte call
    [Tags]            TC_Live_Stability_032
    VT Call Make Volte Call    TC_Live_Stability_032    ${yamlData}    ${log_type}
  

TC_Live_Stability_033
    [Documentation]    Performing long volte Conf call1
    [Tags]            TC_Live_Stability_033
    Long Volte Conf Call1    TC_Live_Stability_033    ${yamlData}    ${log_type}
  

TC_Live_Stability_034
    [Documentation]    Performing long volte Conf call2
    [Tags]            TC_Live_Stability_034
    Long Volte Conf Call2    TC_Live_Stability_034    ${yamlData}    ${log_type}
  

TC_Live_Stability_035
    [Documentation]    Performing long VT Conf call2
    [Tags]            TC_Live_Stability_035
    Long VT Conf Call1    TC_Live_Stability_035    ${yamlData}    ${log_type}
  

TC_Live_Stability_036
    [Documentation]    Performing long VT Conf call2
    [Tags]            TC_Live_Stability_036
    Long VT Conf Call2    TC_Live_Stability_036    ${yamlData}    ${log_type}
  

TC_Live_Stability_037
    [Documentation]    Performing Volte Long Call
    [Tags]            TC_Live_Stability_037
    Volte Long Call    TC_Live_Stability_037    ${yamlData}    ${log_type}
  

TC_Live_Stability_038
    [Documentation]    Performing VT Long Call
    [Tags]            TC_Live_Stability_038
    VT Long Call    TC_Live_Stability_038    ${yamlData}    ${log_type}
  

TC_Live_Stability_039
    [Documentation]    Streaming Youtube videos Continuously
    [Tags]            TC_Live_Stability_039
    Continue Youtube Streaming    TC_Live_Stability_039    ${yamlData}    ${log_type}
  

TC_Live_Stability_041
    [Documentation]    Back to Back IMS registration
    [Tags]            TC_Live_Stability_041
    IMS Registarions B2B    TC_Live_Stability_041    ${yamlData}    ${log_type}
  

TC_Live_Stability_042
    [Documentation]    Short Voice Call Reject Stability
    [Tags]            TC_Live_Stability_042
    Volte Call Reject    TC_Live_Stability_042    ${yamlData}    ${log_type}
  

TC_Live_Stability_043
    [Documentation]    Short Video Call Reject Stability
    [Tags]            TC_Live_Stability_043
    VT Call Reject    TC_Live_Stability_043    ${yamlData}    ${log_type}
  

TC_Live_Stability_046
    [Documentation]    Voice over Wi-Fi Call Stability
    [Tags]            TC_Live_Stability_046
    Voice Over Wlan Stability     TC_Live_Stability_046    ${yamlData}    ${log_type}
  

TC_Live_Stability_047
    [Documentation]    Video over Wi-Fi Call Stability
    [Tags]            TC_Live_Stability_047
    Video Over Wlan Stability    TC_Live_Stability_047    ${yamlData}    ${log_type}
  

TC_Live_Stability_048
    [Documentation]    Launch Browser. The browser caches need to be cleaned each loop. No failures to be observed.
    [Tags]            TC_Live_Stability_048
    Clear Browser Cache    TC_Live_Stability_048    ${yamlData}    ${log_type}
  

TC_Live_Stability_049
    [Documentation]    Capture the Image and Delete the Image
    [Tags]            TC_Live_Stability_049
    Capture Picture    TC_Live_Stability_049    ${yamlData}    ${log_type}
  

TC_Live_Stability_050
    [Documentation]    Switching the Camera and Video mode
    [Tags]            TC_Live_Stability_050
    Switch Camera Mode    TC_Live_Stability_050    ${yamlData}    ${log_type}
  

TC_Live_Stability_051
    [Documentation]    Record Video and Delete the Video
    [Tags]            TC_Live_Stability_051
    Record Video    TC_Live_Stability_051    ${yamlData}    ${log_type}
  

TC_Live_Stability_052
    [Documentation]    Playing 4 Videos from Internal storage
    [Tags]            TC_Live_Stability_052
    Play Video    TC_Live_Stability_052    ${yamlData}    ${log_type}
  

TC_Live_Stability_053
    [Documentation]    Playing 4 Audios from Internal storage
    [Tags]            TC_Live_Stability_053
    Play Audio    TC_Live_Stability_053    ${yamlData}    ${log_type}
  

TC_Live_Stability_054
    [Documentation]    Make Wifi On and OFF
    [Tags]            TC_Live_Stability_054
    Toggle WIFI    TC_Live_Stability_054    ${yamlData}    ${log_type}
  

TC_Live_Stability_055
    [Documentation]    Play Games for 1 Hr, during play receive 10 VoLTE call. Upgrade calls to VT after 5 mins. Check device heating
    [Tags]            TC_Live_Stability_055
    Check Temp Play Game    TC_Live_Stability_055    ${yamlData}    ${log_type}
  

TC_Live_Stability_056
    [Documentation]    During a long VoLTE call(min 1 Hr) send 100 SMS during a a call. Check device heating
    [Tags]            TC_Live_Stability_056
    Check Temp Long Call    TC_Live_Stability_056    ${yamlData}    ${log_type}
  

TC_Live_Stability_057
    [Documentation]    Start Volte call for minimum 30 minutes. Browse youtube(HD)/mobi TV/embms for 1 hr. VT Call for 30 mins. Device should not heat
    [Tags]            TC_Live_Stability_057
    Check Temp Play Youtube    TC_Live_Stability_057    ${yamlData}    ${log_type}
  


