import csv

import setting.mode as mode

keys = ['levelset', 'modeset', 'aivelo', 'monochrome', 'scron', 'sfxon', 'nocnt', 'mod', 'highscore']
default = [0, 0, 1, 0, 1, 1, 0, 0, 0]


def init():
    file = open('./src/modelist.csv', 'w', encoding='utf-8')
    wtr = csv.writer(file)

    mode.levelset = 0
    mode.modeset = 0
    mode.aivelo = 1
    mode.monochrome = 0
    mode.scron = 1
    mode.sfxon = 1
    mode.nocnt = 0
    mode.mod = 0
    mode.highscore = 0

    for i in range(9):
        wtr.writerow([keys[i], default[i]])

    file.close()


def readstatus():
    file = open('./src/modelist.csv', 'r', encoding='utf-8')
    rdr = csv.reader(file)

    r = list(rdr)
    mode.levelset = int(r[0][1])
    mode.modeset = int(r[1][1])
    mode.aivelo = int(r[2][1])
    mode.monochrome = int(r[3][1])
    mode.scron = int(r[4][1])
    mode.sfxon = int(r[5][1])
    mode.nocnt = int(r[6][1])
    mode.mod = int(r[7][1])
    mode.highscore = int(r[8][1])

    file.close()


def savestatus():
    file = open('./src/modelist.csv', 'w', encoding='utf-8')
    wtr = csv.writer(file)

    status = []
    status.append(mode.levelset)
    status.append(mode.modeset)
    status.append(mode.aivelo)
    status.append(mode.monochrome)
    status.append(mode.scron)
    status.append(mode.sfxon)
    status.append(mode.nocnt)
    status.append(mode.mod)
    status.append(mode.highscore)

    for i in range(9):
        wtr.writerow([keys[i], status[i]])

    file.close()
