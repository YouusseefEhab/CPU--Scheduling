from Process import Process


class GanttChart:

    def __init__(self, processList: list[Process]) -> None:
        self.processList = processList.copy()
        self.sortByPriority()
        self.createGanttChartList()
        self.calculateProcesses()

    def getGanttChartList(self) -> list[Process]:
        return self.processList

    def sortByPriority(self) -> None:
        sortedList = []
        while len(self.processList) > 0:
            highestPriorityIdx = 0
            highestPriorityProcess = self.processList[highestPriorityIdx]
            for i, process in enumerate(self.processList):
                if process.priority < highestPriorityProcess.priority:
                    highestPriorityProcess = process
                    highestPriorityIdx = i

            sortedList.append(self.processList.pop(highestPriorityIdx))

        self.processList = sortedList.copy()
        return

    def getNextProcessIdx(self, currentTime: int) -> int:
        idx = -1
        while idx == -1:
            for i, process in enumerate(self.processList):
                if process.arrivalTime <= currentTime:
                    idx = i
                    break
            currentTime += 1
        return idx

    def createGanttChartList(self) -> None:
        ganttList = [self.processList.pop(self.getNextProcessIdx(0))]
        ganttList[0].startTime = ganttList[0].arrivalTime

        if ganttList[0].arrivalTime > 0:
            ganttList.insert(0, Process(0, 0, ganttList[0].arrivalTime, 0))
            ganttList[0].startTime = 0

        while len(self.processList) > 0:
            nextProcessIdx = self.getNextProcessIdx(ganttList[-1].startTime + \
                                                    ganttList[-1].burstTime)
            timeTillNextProcess = self.processList[nextProcessIdx].arrivalTime - (ganttList[-1].startTime + ganttList[-1].burstTime)
            # Check if previous process is still running AND next process priority is higher
            if ganttList[-1].startTime + ganttList[-1].burstTime > self.processList[nextProcessIdx].arrivalTime \
                and ganttList[-1].priority > self.processList[nextProcessIdx].priority:

                splitProcess = ganttList[-1].split(self.processList[nextProcessIdx].arrivalTime)
                self.processList.append(splitProcess)
                self.sortByPriority()

                ganttList.append(self.processList.pop(nextProcessIdx))
                ganttList[-1].startTime = ganttList[-2].startTime + ganttList[-2].burstTime

            # Check if there is time between previous process and next process
            elif timeTillNextProcess > 0:
                ganttList.append(Process(0, \
                                         ganttList[-1].arrivalTime, \
                                         timeTillNextProcess, \
                                         0))
                ganttList[-1].startTime = ganttList[-2].startTime + ganttList[-2].burstTime

                ganttList.append(self.processList.pop(nextProcessIdx))
                ganttList[-1].startTime = ganttList[-2].startTime + ganttList[-2].burstTime

            else:
                ganttList.append(self.processList.pop(nextProcessIdx))
                ganttList[-1].startTime = ganttList[-2].startTime + ganttList[-2].burstTime

        self.processList = ganttList.copy()


    def getGanttChartString(self) -> str:
        ganttStr = ""
        for process in self.processList:
            ganttStr += str(str(process.pid)*process.burstTime)

        translateTable = str.maketrans('0', '-')
        return ganttStr.translate(translateTable)

    def calculateProcesses(self) -> None:
        for process in self.processList:
            startProcess = Process(0,0,0,0)
            endProcess = Process(0,0,0,0)
            startingBurstTime = 0

            for testProcess in self.processList:
                if testProcess.pid == process.pid:
                    startProcess = testProcess
                    break

            for testProcess in self.processList:
                if testProcess.pid == process.pid:
                    endProcess = testProcess
                    startingBurstTime += testProcess.burstTime

            process.turnAroundTime = endProcess.startTime + endProcess.burstTime - startProcess.arrivalTime
            process.waitingTime = process.turnAroundTime - startingBurstTime
            process.responseTime = startProcess.startTime - startProcess.arrivalTime

    def getAverageTurnAroundTime(self) -> float:
        doneProcessPIDs = []
        totalProcesses = 0
        totalTurnAroundTime = 0
        for process in self.processList:
            if process.pid not in doneProcessPIDs:
                totalProcesses += 1
                totalTurnAroundTime += process.turnAroundTime
                doneProcessPIDs.append(process.pid)

        return totalTurnAroundTime / totalProcesses

    def getAverageWaitingTime(self) -> float:
        doneProcessPIDs = []
        totalProcesses = 0
        totalWaitingTime = 0
        for process in self.processList:
            if process.pid not in doneProcessPIDs:
                totalProcesses += 1
                totalWaitingTime += process.waitingTime
                doneProcessPIDs.append(process.pid)

        return totalWaitingTime / totalProcesses

    def getAverageResponseTime(self) -> float:
        doneProcessPIDs = []
        totalProcesses = 0
        totalResponseTime = 0
        for process in self.processList:
            if process.pid not in doneProcessPIDs:
                totalProcesses += 1
                totalResponseTime += process.responseTime
                doneProcessPIDs.append(process.pid)

        return totalResponseTime / totalProcesses
