import os
import signal


class Interrupts:
    """

      class name      : Interrupts
      Description     : this class features the function API for sending
                            signal to robot-framework for terminating execution
    """

    def Get_Process_Id(self):
        """
        :function name : Get_Process_Id
        :description : This function returns the Id of the current
                        active process
        :return: pid of the current process
        """
        return os.getpid()

    def send_signal(self, proc):
        """

        :function name : send_signal
        :description : This function sends SIGTERM signal to the process Id
                        provided as proc
        :param proc: process Id
        :return:
        """
        os.kill(proc, signal.SIGTERM)
