*** Settings ***
Library    OperatingSystem
Library    BuiltIn
Library    Collections
Library    String
Library    interrupts.Interrupts
Variables  ${EXECDIR}/../../../variables/variables_framework.yaml
Library    ${EXECDIR}/../cellular_automation_helpers/common_helper_functions/common_functions.py
Library    ${EXECDIR}/../cellular_automation_helpers/common_helper_functions/device_reports.py
Library    ${EXECDIR}/../cellular_automation_helpers/common_helper_functions/excel_sheet.py

Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Reboot_TC01.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_APM_TC02.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC03.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC04.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC05.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC06.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC07.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC08.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC09.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC10.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC11.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC12.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC13.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC14.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC15.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC16.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC17.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC18.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC19.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC20.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC21.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC22.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC23.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_VT_TC24.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_DOU_TC40.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Concurrency_TC27.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Concurrency_TC28.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Concurrency_TC29.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC08.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC09.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC10.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Volte_TC11.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_browser_TC33.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Camera_TC34.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Camera_TC35.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Camera_TC36.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Camera_TC37.py
Library    ${EXECDIR}/../cellular_automation_helpers/Airtel_stability/Stability_Live_Camera_TC38.py

*** Keywords ***
Start device Log
    [Arguments]        ${yamlData}    ${log_type}
    Log To Console    "Starting Modem Logs" 
    device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    START

Stop device Log
    [Arguments]        ${yamlData}    ${log_type}
    Log To Console    "Stopping Modem Logs" 
    device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    STOP

Fill Excel
    [Arguments]        ${log_type}
    Log    "Creating Excel Sheet"
    create_excel    ${log_type}

Reboot Validate Attach
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Checking Attach after Reboot"
    ${adb_res}    ${msg}    reboot_attach_validation    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

APM Validate Attach
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Checking Attach after APM"
    ${adb_res}    ${msg}    apm_attach_validation    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Short Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte short call"
    ${adb_res}    ${msg}    volte_call_short    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Conn Disconn
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte connect and disconnect"
    ${adb_res}    ${msg}    volte_call_conn_disconn    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Hold
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte call hold and unhold"
    ${adb_res}    ${msg}    perform_hold    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Swap
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte call put call on hold at MT side"
    ${adb_res}    ${msg}    swap_volte_call  ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Conf Volte Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte call put call on hold at MT side"
    ${adb_res}    ${msg}    volte_conf_call  ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Grade1
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade1_volte    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Grade2
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade2_volte    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Grade3
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade3_volte    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Grade4
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte call and up/down grade from mo"
    ${adb_res}    ${msg}    grade4_volte    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Send Sms MO
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing Volte call send sms"
    ${adb_res}    ${msg}    volte_sms_1    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Send Sms MT
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing Volte call send sms"
    ${adb_res}    ${msg}    volte_sms_2    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Short Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte short call"
    ${adb_res}    ${msg}    vt_rcv_mo    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Conn Disconn
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte connect and disconnect"
    ${adb_res}    ${msg}    vt_call_conn_disconn    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Hold
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing VT call hold and unhold"
    ${adb_res}    ${msg}    perform_vt_hold    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Swap
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing VT call swap"
    ${adb_res}    ${msg}    swap_volte_call  ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Conf VT Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing volte call put call on hold at MT side"
    ${adb_res}    ${msg}    vt_conference_call1  ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Grade1
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade1_vt    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Grade2
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade2_vt    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Grade3
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade3_vt    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Grade4
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call and up/down grade from mo"
    ${adb_res}    ${msg}    grade4_vt    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Send Sms MO
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call send sms"
    ${adb_res}    ${msg}    vt_sms_1    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Send Sms MT
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing vt call send sms"
    ${adb_res}    ${msg}    vt_sms_2    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Conf Long Volte Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing long volte conf call"
    ${adb_res}    ${msg}    long_volte_conf1  ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Conf Long VT Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing long vt conf call"
    ${adb_res}    ${msg}    long_vt_conf1  ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Long Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing long Volte call "
    ${adb_res}    ${msg}    long_volte_call    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Long Call
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing long VT call "
    ${adb_res}    ${msg}    long_vt_call    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Stream Youtube
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing Volte call send sms"
    ${adb_res}    ${msg}    youtube_video_streaming    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Stability Wifi
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Checking Wifi Stability"
    ${adb_res}    ${msg}    wifi_enable_disable    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Volte Call Wifi
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing Volte call over Wifi"
    ${adb_res}    ${msg}    volwan_audio    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

VT Call Wifi
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing VT call over Wifi"
    ${adb_res}    ${msg}    volwan_video    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Mobile Browsing 
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing Mobile Browsing"
    ${adb_res}    ${msg}    browser_cache    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Capturing Picture
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Capturing Picture"
    ${adb_res}    ${msg}    capture_picture    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Camera Switch Video
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Switching between camera and video mode"
    ${adb_res}    ${msg}    switch_camera_to_video    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Recording Video
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Recording video"
    ${adb_res}    ${msg}    record_video    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Play Video
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing video play"
    ${adb_res}    ${msg}    video_play    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

Play Audio
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing audio play"
    ${adb_res}    ${msg}    audio_play    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Log    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}

DOU
    [Arguments]    ${tst}    ${yamlData}    ${log_type}
    Log To Console    "Performing DOU"
    ${adb_res}    ${msg}    dou_test    ${tst}    ${yamlData}
    Fetch_result    ${TEST NAME}    ${adb_res}
    Log    ${adb_res}
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  device_logging      ${yamlData}    ${TEST NAME}    ${log_type}    RESTART
    Should Be True         ${adb_res}    msg=${msg}