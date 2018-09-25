#! python

import sys, os, time
from stat import *
from colorama import init
from termcolor import colored


def follow(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def getLogStats(logfile):
    try:
        logfileInfo = os.stat(logfile)
    except IOErrror:
        print("Unable to retrieve Log File Stats")
    else:
        print("Log File Size: ", logfileInfo[ST_SIZE])
        print("Last Modified Timestamp: " + time.asctime(time.localtime(logfileInfo[ST_MTIME])))
        print()


def processClear(logfile):
    deleteExisting = input("Do you want to delete the contents of the log? (Y/[N]): ")

    if (deleteExisting.upper() == "Y"):
        with open(logfile, "w"):
            pass
        print("Logfile has been cleared.")


def displayMenu(logFileList):
    options = logFileList.keys()

    print()
    print("Available Log Files:")
    for entry in options:
        print(entry, '-', logFileList[entry])

    print()


def getLogFileList():
    logCount = 0
    logFileList = {}

    # for file in os.listdir("C:\\VisualStudio2010\\Bonton.LoveStyleRewards\\LoveStyleRewards.HelloWorld.Updater\\bin\\Debug"):
    for file in os.listdir(os.getcwd()):
        if file.lower().endswith("log"):
            logCount += 1
            logFileList.update({logCount: file})

    # add an exit
    logFileList.update({logCount + 1: "Exit"})

    return (logFileList)


def main(argv):
    init()

    HighLightWordList = ['elapsed', 'reply code', 'opening test case', 'total coupon savings', 'passed']
    FatalWordList = ['exception', 'fatal', 'error', 'failed']

    print(colored("**** Python Log Watcher ****", 'red'))
    # logfileName = "C:\\VisualStudio2010\\Bonton.LoveStyleRewards\\LoveStyleRewards.HelloWorld.Updater\\bin\\Debug\\LsrHwUpdater.log"
    logfileName = ""

    listOfLogFiles = getLogFileList()

    if len(listOfLogFiles) > 0:
        while True:
            displayMenu(listOfLogFiles)
            print()
            logSelection = input("Enter the Number of the Log you would like to watch: ")

            try:
                logFileSelected = listOfLogFiles[int(logSelection)]
            except:
                print("** Invalid selection **")
            else:
                if logFileSelected == "Exit":
                    return
                print("You selected", logFileSelected)

                getLogStats(logFileSelected)
                processClear(logFileSelected)

                # start watching the log
                print()
                print("Watching the", logFileSelected, "log...")
                print("Press ^C to stop the watcher.")
                logfile = open(logFileSelected)

                loglines = follow(logfile)
                for line in loglines:
                    if any(x in line.lower() for x in FatalWordList):
                        print(colored(line, 'red', attrs=['bold']), end="")
                    elif any(x in line.lower() for x in HighLightWordList):
                        print(colored(line, 'green', attrs=['bold']), end="")
                    else:
                        print(line, end="")

                return
    else:
        print("** There are no Log Files available **")
        return


if __name__ == "__main__":
    main(sys.argv)
