class SectionLight:
    def __init__(self, m, tl, gg, rr):
        self.m = []  # empty list for marking
        self.f = []  # empty list with flows
        self.m.append(m)  # fill that empty list with the first mark

        self.maxcar = 60
        self.q = 100
        self.r = 80
        self.h = 0.3

        """
        Traffic light.

        Each traffic light follows the same principle:
        green light (gg)  -> normal flow
        red light (rr)    -> flow equals zero
        green to red (gr) -> flow represents the number of cars that passed in that amber window
        red to green (rg) -> flow represents the number of cars that passed in that acceleration window 
        """
        self.tl = tl  # boolean for traffic light?
        self.gg = gg  # green light (steps)
        self.rr = rr  # red light (steps)
        self.alfa = 3  # interval of time inside Delta that represents the Green to red transition
        self.beta = 2  # interval of time inside Delta that represents the Red to green transition
        self.lstate = [0]  # vector to save the state of the traffic light
        """Variable used to iterate the different traffic loop states."""
        self.cnt = 0


"""
This function is to apply the inverse sequence in the perpendicular section of the traffic light
"""


def invert_trafficlight(x, y):
    y.gg = x.rr
    y.rr = x.gg
    y.lstate = [2]


"""
This function is to invert the next state
"""


def invert_nextstate(i):
    j = 0
    if i == 0:
        j = 2
    elif i == 1:
        j = 3
    elif i == 2:
        j = 0
    elif i == 3:
        j = 1
    return j


"""CALCULATE FLOW"""


def new_flow_horizontal_blind(section, i, lambd, delta):
    for j in range(0, len(section)):
        if j < len(section) - 1:
            f = lambd[j] * min(section[j].m[i] / section[j].q, section[j].h, (section[j].maxcar - section[j+1].m[i]) / section[j+1].r)
            if section[j].tl:
                if section[j].lstate[i] == 1:
                    f = f * section[j].alfa / (2 * delta)
                elif section[j].lstate[i] == 2:
                    f = 0
                elif section[j].lstate[i] == 3:
                    f = f * section[j].beta / (2 * delta)
            section[j].f.append(f)
        else:
            f = lambd[j] * min(section[j].m[i] / section[j].q, section[j].h)
            if section[j].tl:
                if section[j].lstate[i] == 1:
                    f = f * section[j].alfa / (2 * delta)
                elif section[j].lstate[i] == 2:
                    f = 0
                elif section[j].lstate[i] == 3:
                    f = f * section[j].beta / (2 * delta)
            section[j].f.append(f)


def new_flow_vertical_blind(section, i, lambd, delta):
    for l in range(0, len(section)):
        for j in range(0, len(section[0])):
            if j < len(section[0]) - 1:
                f = lambd[j] * min(section[l][j].m[i] / section[l][j].q, section[l][j].h, (section[l][j].maxcar - section[l][j+1].m[i]) / section[l][j+1].r)
                if section[l][j].tl:
                    if section[l][j].lstate[i] == 1:
                        f = f * section[l][j].alfa / (2 * delta)
                    elif section[l][j].lstate[i] == 2:
                        f = 0
                    elif section[l][j].lstate[i] == 3:
                        f = f * section[l][j].beta / (2 * delta)
                section[l][j].f.append(f)
            else:
                f = lambd[j] * min(section[l][j].m[i] / section[l][j].q, section[l][j].h)
                if section[l][j].tl:
                    if section[l][j].lstate[i] == 1:
                        f = f * section[l][j].alfa / (2 * delta)
                    elif section[l][j].lstate[i] == 2:
                        f = 0
                    elif section[l][j].lstate[i] == 3:
                        f = f * section[l][j].beta / (2 * delta)
                section[l][j].f.append(f)


def new_flow_horizontal_mpc(section, i, lambd, delta, sequence, m):
    for j in range(0, len(section)):
        if j < len(section) - 1:
            f = lambd[j] * min(section[j].m[i+m] / section[j].q, section[j].h, (section[j].maxcar - section[j+1].m[i+m]) / section[j+1].r)
            if section[j].tl:
                if sequence[m] == 1:
                    f = f * section[j].alfa / (2 * delta)
                elif sequence[m] == 2:
                    f = 0
                elif sequence[m] == 3:
                    f = f * section[j].beta / (2 * delta)
            section[j].f.append(f)
        else:
            f = lambd[j] * min(section[j].m[i+m] / section[j].q, section[j].h)
            if section[j].tl:
                if sequence[m] == 1:
                    f = f * section[j].alfa / (2 * delta)
                elif sequence[m] == 2:
                    f = 0
                elif sequence[m] == 3:
                    f = f * section[j].beta / (2 * delta)
            section[j].f.append(f)


def new_flow_vertical_mpc(section, i, lambd, delta, sequence, m):
    for l in range(0, len(section)):
        for j in range(0, len(section[0])):
            if j < len(section[0]) - 1:
                f = lambd[j] * min(section[l][j].m[i+m] / section[l][j].q, section[l][j].h, (section[l][j].maxcar - section[l][j+1].m[i+m]) / section[l][j+1].r)
                if section[l][j].tl:
                    if sequence[m] == 1:
                        f = f * section[l][j].alfa / (2 * delta)
                    elif sequence[m] == 2:
                        f = 0
                    elif sequence[m] == 3:
                        f = f * section[l][j].beta / (2 * delta)
                section[l][j].f.append(f)
            else:
                f = lambd[j] * min(section[l][j].m[i+m] / section[l][j].q, section[l][j].h)
                if section[l][j].tl:
                    if sequence[m] == 1:
                        f = f * section[l][j].alfa / (2 * delta)
                    elif sequence[m] == 2:
                        f = 0
                    elif sequence[m] == 3:
                        f = f * section[l][j].beta / (2 * delta)
                section[l][j].f.append(f)


"""CALCULATE MARKING"""


def new_marking_horizontal_blind(section, inputcars, i, delta):
    for j in range(0, len(section)):
        if j == 0:
            section[j].m.append(section[j].m[i] + delta * inputcars[i] - delta * section[j].f[i])
        else:
            section[j].m.append(section[j].m[i] + delta * section[j-1].f[i] - delta * section[j].f[i])


def new_marking_vertical_blind(section, inputcars, i, delta):
    for l in range(0, len(section)):
        for j in range(0, len(section[0])):
            if j == 0:
                section[l][j].m.append(section[l][j].m[i] + delta * inputcars[i] - delta * section[l][j].f[i])
            else:
                section[l][j].m.append(section[l][j].m[i] + delta * section[l][j-1].f[i] - delta * section[l][j].f[i])


def new_marking_horizontal_mpc(section, inputcars, i, delta, m):
    for j in range(0, len(section)):
        if j == 0:
            section[j].m.append(section[j].m[i+m] + delta * inputcars[m] - delta * section[j].f[i+m])
        else:
            section[j].m.append(section[j].m[i+m] + delta * section[j-1].f[i+m] - delta * section[j].f[i+m])


def new_marking_vertical_mpc(section, inputcars, i, delta, m):
    for l in range(0, len(section)):
        for j in range(0, len(section[0])):
            if j == 0:
                section[l][j].m.append(section[l][j].m[i+m] + delta * inputcars[m] - delta * section[l][j].f[i+m])
            else:
                section[l][j].m.append(section[l][j].m[i+m] + delta * section[l][j-1].f[i+m] - delta * section[l][j].f[i+m])


"""STATE MACHINE, 0=gg=green, 1=gr=green to red, 2=rr=red, 3=rg=red to green"""


def state_machine(section, i):
    if section.lstate[i] == 0:
        section.cnt += 1
        if section.cnt == section.gg:
            section.cnt = 0
            section.lstate.append(1)
        else:
            section.lstate.append(0)
    if section.lstate[i] == 1:
        section.lstate.append(2)
    if section.lstate[i] == 2:
        section.cnt += 1
        if section.cnt == section.rr:
            section.cnt = 0
            section.lstate.append(3)
        else:
            section.lstate.append(2)
    if section.lstate[i] == 3:
        section.lstate.append(0)


"""
INPUT CARS
Takes the next 4 incoming flow of cars
"""


def inputcars(inputcar, i):
    return [inputcar[i], inputcar[i + 1], inputcar[i + 2], inputcar[i + 3]]


def inputcntcars(x):
    return [x, x, x, x]


"""
REMOVES THE APPENDED MARKING AND FLOW
"""


def remove(sectionH, sectionV):
    for i in range(0, 4):
        for j in range(len(sectionH)):
            sectionH[j].m.pop()
            sectionH[j].f.pop()
        for j in range(len(sectionV)):
            for m in range(len(sectionV[0])):
                sectionV[j][m].m.pop()
                sectionV[j][m].f.pop()