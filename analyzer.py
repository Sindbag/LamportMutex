import glob

legal_previous = {
    'request': ['request', 'release'],
    'acquire': ['request'],
    'release': ['acquire']
}

if __name__ == "__main__":
    for file in glob.glob('logs/*.log'):
        print(file)

        with open(file) as f:
            tmp = ('request', 0.0, -1)

            for l in f:
                action, time, logictime, pid = l.split()

                if tmp[0] not in legal_previous[action]:
                    print(file, action, tmp[0], 'Incorrect order of actions')

                if int(logictime) < tmp[2]:
                    print(file, logictime, tmp[2], 'Incorrect logic time')

                if float(time) < tmp[1]:
                    print(file, time, tmp[1], 'Incorrect real time')

                tmp = (action, float(time), int(logictime))

    print('OK')
