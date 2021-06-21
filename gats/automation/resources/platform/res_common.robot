
*** Settings ***
Library    OperatingSystem
Library    BuiltIn
Library    Collections
Library    String
Library    ${EXECDIR}/../automation_helpers/common_log.py
Library    ${EXECDIR}/../automation_helpers/Common.py
Library    ${EXECDIR}/../automation_helpers/YamlUtils.py
Library    interrupts.Interrupts
Variables  ${EXECDIR}/../../../variables/variables_framework.yaml

*** Keywords ***
Set Iteration Path
    [Arguments]    ${iteration_path}
    ${prev_level}    Set Log Level    NONE
    Set Test Message  *HTML* <br/><b>Result Path:</b> <a href=file://${iteration_path}>${dict.testcase_name_and_iter_path}</a><br/>    append=${true}
    Set Log Level    ${prev_level}

Check Devices
    Log To Console    "Entered check devices"
    ${adb_res}    ${msg}     check_adb_devices
    Run Keyword If              ${adb_res} == True
    ...  Log To Console         ${msg}
    ...  ELSE
    ...  Should Be True         ${adb_res}
    ...  msg=${msg}

Fetch Device ID
    [Arguments]     ${arg1}=${DEVICE_ID}
    assign_device_id     ${arg1}

Device Teardown
    [Documentation]             Closes all the application running
    tear_down

Setup Log
    #[Arguments]                ${arg1}=${PROJECT_NAME}    ${arg2}=${MILESTONE}    ${arg3}=${SESSION_NAME}    ${arg4}=${DEVICE_NAME}    ${arg5}=${TEST_ITERATION}    ${arg6}=${SUITE_NAME}    ${arg7}=${AUTOMATION_ID}
    [Arguments]                 ${arg1}=${dict.project}      ${arg2}=${dict.session}    ${arg3}=${dict.device}    ${arg4}=${dict.iter}    ${arg5}=${dict.suite}   ${arg6}=@{TEST TAGS}[0]
    Log                         Inside setup log keyword
    #Run Keyword                 Check Stop Execution Status
    setup_logging               ${arg1}  ${arg2}  ${arg3}  ${arg4}  ${arg5}  ${arg6}

Check Stop Execution Status
    Read Text File
    Get Stop Execution Status

Remove Log Handler
    remove_script_log_handler

Read Text File
    ${TextFileContent}=  OperatingSystem.Get File  ${STOP_EXECUTION_FILE.FILE_NAME}
    @{TextFileContent}=  Split To Lines    ${TextFileContent}
    Set Global Variable    ${TextFileContent}
    Log    ${TextFileContent}

Get Stop Execution Status
    log to console  ${TextFileContent}
    Run Keyword If  ${True}==${TextFileContent[0]}  Generate Interrupt

Generate Interrupt
    ${self_id} =  interrupts.Interrupts.Get_Process_Id
    set suite variable  ${self_id}
    log    Execution was stopped from dashboard
    ${output} =  Run Keyword    interrupts.Interrupts.send_signal      ${self_id}
    [Teardown]     interrupts.Interrupts.send_signal      ${self_id}



Execute ADB Command
    [Documentation]     Execute adb command To check the brightness
    [Arguments]     ${command}
    ${res}      run_adb_cmd     ${command}
    Log To Console      ${res}
    [return]    ${res}
