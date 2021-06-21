*** Settings ***
Test Timeout    720 minutes
Library     BuiltIn
Library     Collections
Resource    ${EXECDIR}/../../../resources/platform/res_common.robot
Resource    ${EXECDIR}/../../../resources/cellular/res_common.robot

Variables   ${dict.yaml}/uiconfig.yaml

Test Setup  Run Keywords      Setup Log
...  AND     Start Device Log   ${yamlData}    ${log_type}

Test Teardown  Run Keywords    Set Iteration Path      ${dict.robot_log_path}
...  AND  Stop Device Log    ${yamlData}    ${log_type}
...  AND    Remove Log Handler

Suite Teardown    Run Keyword    Fill Excel    ${log_type}

*** Variables ***
#&{dict}     project=${1}     milestone=${2}     session=${3}     device=${4}    test_iter_count=${5}    testcase_name_and_iter_path=${6}    iteration_path=${7}    suite=${8}
${log_type}    0

*** Test Cases ***
TC_Airtel_Stability_001
    [Documentation]    Validate Attach After Reboot
    [Tags]            TC_Airtel_Stability_001
    Reboot Validate Attach    TC_Airtel_Stability_001     ${yamlData}    ${log_type}

TC_Airtel_Stability_002
    [Documentation]    Validate Attach After APM
    [Tags]            TC_Airtel_Stability_002
    APM Validate Attach    TC_Airtel_Stability_002     ${yamlData}    ${log_type}

TC_Airtel_Stability_003
    [Documentation]    Validate Attach After APM
    [Tags]            TC_Airtel_Stability_003
    Volte Short Call    TC_Airtel_Stability_003     ${yamlData}    ${log_type}

TC_Airtel_Stability_004
    [Documentation]    Performing Volte Connect and Disconnect
    [Tags]            TC_Airtel_Stability_004
    Volte Conn Disconn    TC_Airtel_Stability_004     ${yamlData}    ${log_type}

TC_Airtel_Stability_005
    [Documentation]    Performing Volte Connect and Disconnect
    [Tags]            TC_Airtel_Stability_005
    Volte Hold    TC_Airtel_Stability_005     ${yamlData}    ${log_type}

TC_Airtel_Stability_006
    [Documentation]    Performing Swapping of calls
    [Tags]            TC_Airtel_Stability_006
    Volte Call Swap    TC_Airtel_Stability_006     ${yamlData}    ${log_type}

TC_Airtel_Stability_007
    [Documentation]    Performing conffernences call
    [Tags]            TC_Airtel_Stability_007
    Conf Volte Call    TC_Airtel_Stability_007     ${yamlData}    ${log_type}

TC_Airtel_Stability_008
    [Documentation]    Performing upgrade and downgrade on call @ MO side
    [Tags]            TC_Airtel_Stability_008
    Volte Call Grade1   TC_Airtel_Stability_008     ${yamlData}    ${log_type}

TC_Airtel_Stability_009
    [Documentation]    Performing upgrade and downgrade on call @ MT side
    [Tags]            TC_Airtel_Stability_009
    Volte Call Grade2   TC_Airtel_Stability_009     ${yamlData}    ${log_type}

TC_Airtel_Stability_010
    [Documentation]    Performing upgrade and downgrade on call @ MT side
    [Tags]            TC_Airtel_Stability_010
    Volte Call Grade3   TC_Airtel_Stability_010     ${yamlData}    ${log_type}

TC_Airtel_Stability_011
    [Documentation]    Performing upgrade and downgrade on call @ MT side
    [Tags]            TC_Airtel_Stability_011
    Volte Call Grade4   TC_Airtel_Stability_011     ${yamlData}    ${log_type}

TC_Airtel_Stability_012
    [Documentation]    Performing upgrade and downgrade on call @ MT side
    [Tags]            TC_Airtel_Stability_012
    Volte Call Send Sms MO   TC_Airtel_Stability_012     ${yamlData}    ${log_type}

TC_Airtel_Stability_013
    [Documentation]    Performing upgrade and downgrade on call @ MT side
    [Tags]            TC_Airtel_Stability_013
    Volte Call Send Sms MT   TC_Airtel_Stability_013     ${yamlData}    ${log_type}

TC_Airtel_Stability_014
    [Documentation]    Performing VT call
    [Tags]            TC_Airtel_Stability_014
    VT Short Call   TC_Airtel_Stability_014     ${yamlData}    ${log_type}

TC_Airtel_Stability_015
    [Documentation]    Performing VT Connect and Disconnect
    [Tags]            TC_Airtel_Stability_015
    VT Conn Disconn    TC_Airtel_Stability_015     ${yamlData}    ${log_type}

TC_Airtel_Stability_016
    [Documentation]    Performing VT Call Hold Unhold
    [Tags]            TC_Airtel_Stability_016
    VT Hold    TC_Airtel_Stability_016     ${yamlData}    ${log_type}

TC_Airtel_Stability_017
    [Documentation]    Performing Swapping of VT calls
    [Tags]            TC_Airtel_Stability_017
    VT Call Swap    TC_Airtel_Stability_017     ${yamlData}    ${log_type}

TC_Airtel_Stability_018
    [Documentation]    Performing vt conf call
    [Tags]            TC_Airtel_Stability_018
    VT Conf Call   TC_Airtel_Stability_018     ${yamlData}    ${log_type}

TC_Airtel_Stability_019
    [Documentation]    Performing VT updown
    [Tags]            TC_Airtel_Stability_019
    VT Call Grade1    TC_Airtel_Stability_019     ${yamlData}    ${log_type}

TC_Airtel_Stability_020
    [Documentation]    Performing VT updown
    [Tags]            TC_Airtel_Stability_020
    VT Call Grade2    TC_Airtel_Stability_020     ${yamlData}    ${log_type}

TC_Airtel_Stability_021
    [Documentation]    Performing VT updown
    [Tags]            TC_Airtel_Stability_021
    VT Call Grade3    TC_Airtel_Stability_021     ${yamlData}    ${log_type}

TC_Airtel_Stability_022
    [Documentation]    Performing VT updown
    [Tags]            TC_Airtel_Stability_022
    VT Call Grade4    TC_Airtel_Stability_022     ${yamlData}    ${log_type}

TC_Airtel_Stability_023
    [Documentation]    Sending SmS while in VT call
    [Tags]            TC_Airtel_Stability_023
    VT Call Send Sms MO    TC_Airtel_Stability_023     ${yamlData}    ${log_type}

TC_Airtel_Stability_024
    [Documentation]    Sending SmS while in VT call
    [Tags]            TC_Airtel_Stability_024
    VT Call Send Sms MT    TC_Airtel_Stability_024     ${yamlData}    ${log_type}

TC_Airtel_Stability_025
    [Documentation]    Performing volte Long Conf call
    [Tags]            TC_Airtel_Stability_025
    Volte Long Conf Call   TC_Airtel_Stability_025     ${yamlData}    ${log_type}

TC_Airtel_Stability_026
    [Documentation]    Performing vt long conf call
    [Tags]            TC_Airtel_Stability_026
    VT Long Conf Call   TC_Airtel_Stability_026     ${yamlData}    ${log_type}

TC_Airtel_Stability_027
    [Documentation]    Performing volte long call
    [Tags]            TC_Airtel_Stability_027
    Volte Long Call   TC_Airtel_Stability_027     ${yamlData}    ${log_type}

TC_Airtel_Stability_028
    [Documentation]    Performing VT long call
    [Tags]            TC_Airtel_Stability_028
    VT Long Call   TC_Airtel_Stability_028     ${yamlData}    ${log_type}

TC_Airtel_Stability_029
    [Documentation]    Streaming YouTube Video
    [Tags]            TC_Airtel_Stability_029
    Stream Youtube   TC_Airtel_Stability_029     ${yamlData}    ${log_type}

TC_Airtel_Stability_030
    [Documentation]    Checking Wifi Stability
    [Tags]            TC_Airtel_Stability_030
    Stability Wifi    TC_Airtel_Stability_030     ${yamlData}    ${log_type}

TC_Airtel_Stability_031
    [Documentation]    Voice Over Wifi
    [Tags]            TC_Airtel_Stability_031
    Volte Call Wifi     TC_Airtel_Stability_031     ${yamlData}    ${log_type}

TC_Airtel_Stability_032
    [Documentation]    Vt Over Wifi
    [Tags]            TC_Airtel_Stability_032
    VT Call Wifi    TC_Airtel_Stability_032     ${yamlData}    ${log_type}

TC_Airtel_Stability_033
    [Documentation]    Browsing
    [Tags]            TC_Airtel_Stability_033
    Mobile Browsing    TC_Airtel_Stability_033     ${yamlData}    ${log_type}

TC_Airtel_Stability_034
    [Documentation]    Capturing Picture
    [Tags]            TC_Airtel_Stability_034
    Capturing Picture    TC_Airtel_Stability_034     ${yamlData}    ${log_type}

TC_Airtel_Stability_035
    [Documentation]    Switching Camera Mode
    [Tags]            TC_Airtel_Stability_035
    Camera Switch Video    TC_Airtel_Stability_035     ${yamlData}    ${log_type}

TC_Airtel_Stability_036
    [Documentation]    Recording Video
    [Tags]            TC_Airtel_Stability_036
    Recording Video    TC_Airtel_Stability_036     ${yamlData}    ${log_type}

TC_Airtel_Stability_037
    [Documentation]    Playing Video File
    [Tags]            TC_Airtel_Stability_037
    Play Video    TC_Airtel_Stability_037     ${yamlData}    ${log_type}

TC_Airtel_Stability_038
    [Documentation]    Playing Audio File
    [Tags]            TC_Airtel_Stability_038
    Play Audio    TC_Airtel_Stability_038     ${yamlData}    ${log_type}

TC_Airtel_Stability_040
    [Documentation]    Playing DOU
    [Tags]            TC_Airtel_Stability_040
    DOU    TC_Airtel_Stability_040     ${yamlData}    ${log_type}