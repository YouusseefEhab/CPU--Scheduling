from Process import Process
from GanttChart import GanttChart


if __name__ == "__main__":
    processN = int(input("Please Enter number of Processes: "))
    processList = []
    for i in range(processN):
        arrivalTime = int(input(f"Process {i + 1} Arrival Time: "))
        burstTime = int(input(f"Process {i + 1} Burst Time: "))
        priority = int(input(f"Process {i + 1} Priority: "))
        print()

        processList.append(Process(i + 1, arrivalTime, burstTime, priority))

    ganttChart = GanttChart(processList)

    ganttList = ganttChart.getGanttChartList()
    ganttStr = ganttChart.getGanttChartString()

    print(ganttStr)
