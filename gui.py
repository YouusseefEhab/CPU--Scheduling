from Process import Process
from GanttChart import GanttChart
import PySimpleGUI as sg

if __name__ == '__main__':
    processN = 0

    sg.set_options(font=('Consolas'))
    width = 800
    height = 300

    # All the stuff inside your window.
    layout = [
        [sg.Text("Enter Number of Processes")],
        [sg.InputText(key='-processN-')],
        [sg.Button('Next', key='-processNNext-'), sg.Button('Cancel')]
    ]

    # Create the Window
    window = sg.Window('Priority Preemptive', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == '-processNNext-':
            try:
                processN = int(values['-processN-'])
            except:
                sg.popup_error('Please Enter Number!')
                continue

            if processN <= 0:
                sg.popup_error('Please Enter Number Above 0!')
                continue

            column = []
            for i in range(processN):
                column.append([sg.Text(f"Process {i + 1} Arrival Time: "), sg.InputText(key=f"-p{i + 1}ArrivalTime-")])
                column.append([sg.Text(f"Process {i + 1} Burst Time: "), sg.InputText(key=f"-p{i + 1}BurstTime-")])
                column.append([sg.Text(f"Process {i + 1} Priority: "), sg.InputText(key=f"-p{i + 1}Priority-")])
                column.append([sg.Text('')])
                column.append([sg.Text('')])
            column.append([sg.Button('Next', key='-processesInputNext-'), sg.Button('Cancel')])

            layout = [
                [sg.Column(column, size=(width, height), scrollable=True, vertical_scroll_only=True)]
            ]
            window.close()
            window = sg.Window('Priority Preemptive', layout)

        if event == '-processesInputNext-':
            failed = False
            for i in range(processN):
                try:
                    values[f'-p{i + 1}ArrivalTime-'] = int(values[f'-p{i + 1}ArrivalTime-'])
                    values[f'-p{i + 1}BurstTime-'] = int(values[f'-p{i + 1}BurstTime-'])
                    values[f'-p{i + 1}Priority-'] = int(values[f'-p{i + 1}Priority-'])
                except:
                    sg.popup_error('Please Enter Numbers Only!')
                    failed = True
                    break

                if values[f'-p{i + 1}ArrivalTime-'] < 0 or \
                    values[f'-p{i + 1}BurstTime-'] < 0 or \
                    values[f'-p{i + 1}Priority-'] < 0:

                    sg.popup_error('Please Enter Number Higher Than 0!')
                    failed = True

            if failed:
                event = '-processNNext-'
                continue

            processList = []
            for i in range(processN):
                processList.append(Process(i + 1, \
                                           values[f'-p{i + 1}ArrivalTime-'], \
                                           values[f'-p{i + 1}BurstTime-'], \
                                           values[f'-p{i + 1}Priority-']))

            ganttChart = GanttChart(processList)
            ganttList = ganttChart.getGanttChartList()
            ganttStr = ganttChart.getGanttChartString()

            size = 5
            numbers = range(len(ganttStr) + 1)

            processText = ''
            spaceText = ''
            numberLineText = ''

            processText += '|'
            for process in ganttList:
                if process.pid != 0:
                    processText += (('-'*(((process.burstTime * size)) // 2)) + \
                                    ('-'*((process.burstTime - 1) // 2)) + \
                                    str(process.pid) + \
                                    ('-'*(((process.burstTime * size)) // 2)) + \
                                    ('-'*((process.burstTime - 1) // 2)) + \
                                    '|')
                else:
                    processText += ((' '*(((process.burstTime * size)) // 2)) + \
                                    (' '*((process.burstTime - 1) // 2)) + \
                                    ' ' + \
                                    (' '*(((process.burstTime * size)) // 2)) + \
                                    (' '*((process.burstTime - 1) // 2)) + \
                                    '|')
                print(process.toString())

            counter = 0
            for num in numbers:
                if num == pow(10, counter + 1):
                    counter += 1
                spaceText += ('|' + ' '*size)
                numberLineText += (str(num) + ' '*(size - counter))

            column = [
                [sg.Text(processText)],
                [sg.Text(spaceText)],
                [sg.Text(numberLineText)],
            ]

            layout = [
                [sg.Text('Gantt Chart', justification='center')],
                [sg.Text('')],
                [sg.Column(column, size=(width, height), scrollable=True)],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Text('Average Turn Around Time: '), sg.Text(str(ganttChart.getAverageTurnAroundTime()))],
                [sg.Text('Average Waiting Time: '), sg.Text(str(ganttChart.getAverageWaitingTime()))],
                [sg.Text('Average Response Time: '), sg.Text(str(ganttChart.getAverageResponseTime()))],
            ]


            window.close()
            window = sg.Window('Priority Preemptive', layout)

    window.close()

