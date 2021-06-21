def accept_or_reject_call(self, action):
        """
        Accepts or Rejects a call
        :param action: accept the call or reject
        :return: bool, msg
        :Author: Vishnu Priya
        """
        try:
            if action.lower() == 'accept':
                # Getting the values from yml
                answer_call = YamlUtils.read_yml('Common', 'AnswerCall')
                ongoing_call = YamlUtils.read_yml('Common', 'OngoingCall')
                log.debug("Inside accept_or_reject_call() method")
                self.core.notification_open()
                if self.core.wait_until_the_element_appears(**answer_call):
                    if self.core.ui_element_click(**answer_call):
                        if self.core.ui_element_exists(**ongoing_call):
                            return common_log.return_values(
                                True, "info", "Successfully accepted the call")
                        return common_log.return_values(
                            False, "info", "Call is not accepted")
            elif action.lower() == 'reject':
                # Getting the values from yml
                decline_call = YamlUtils.read_yml('Common', 'DeclineCall')
                android_system = YamlUtils.read_yml('Common', 'AndroidSystem')
                log.debug("Inside accept_or_reject_call() method")
                self.core.notification_open()
                if self.core.ui_element_click(**decline_call):
                    if self.core.ui_element_exists(**android_system):
                        return common_log.return_values(
                            True, "info", "Successfully rejected the call")
                    return common_log.return_values(
                        False, "info", "Call is not rejected")
            else:
                return common_log.return_values(
                    False, "info", "Please give correct action to be done")
        except Exception as generic_except:
            return common_log.return_values(
                False, "error", "Exception occurred due to {}: ".format(generic_except))
