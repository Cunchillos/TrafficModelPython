import numpy
import matplotlib.pyplot as plt
import TrafficModel
import TrafficModelLight as Tml
import copy
from scipy.stats import uniform


def main_nolight_blind():
    """INITIALIZATION"""
    delta = 8  # Time discretized in periods of delta = 8 seconds.
    samples = 20  # Total samples
    tt = []  # time vector so I can plot events in real time.
    tt1 = []
    for i in range(0, samples + 1):
        tt.append(delta * i)
        tt1.append(delta * i)
    tt1.pop()
    # Input flow of cars horizontally, uniform [0.2, 0.3] cars/s
    hinputcars = uniform.rvs(loc=0, scale=0, size=samples)
    """CREATION OF SECTIONS"""
    hsections = [Tml.SectionLight(40, False, 0, 0), Tml.SectionLight(55, False, 0, 0), Tml.SectionLight(20, False, 0, 0), Tml.SectionLight(0, False, 0, 0)]
    hlambda = [4, 5, 4, 5]
    nhsections = len(hsections)
    print("There are ", nhsections, "horizontal sections")
    """LOOP"""
    for i in range(0, samples):
        """FLOW"""
        Tml.new_flow_horizontal_blind(hsections, i, hlambda, delta)
        """MARKING"""
        Tml.new_marking_horizontal_blind(hsections, hinputcars, i, delta)
    for i in range(len(hsections)):
        hsections[i].m.pop()
    """PLOT"""
    plt.figure(1)
    plt.plot(tt1, hsections[0].m, 'b', tt1, hsections[1].m, 'r', tt1, hsections[2].m, 'g', tt1, hsections[3].m, 'y')
    plt.legend(["m[p1]", "m[p2]", "m[p3]", "m[p4]"])
    plt.ylabel("Marking [cars]")
    plt.xlabel("Time [s]")
    plt.figure(2)
    plt.plot(hsections[0].m, hsections[0].f, 'b')
    plt.legend(["Section1"])
    plt.ylabel("Flow [cars/s]")
    plt.xlabel("Marking [cars]")
    plt.show()


def main_blind():
    """INITIALIZATION"""
    delta = 8  # Time discretized in periods of delta = 8 seconds.
    samples = 50  # Total samples
    tt = []  # time vector so I can plot events in real time.
    tt1 = []
    for i in range(0, samples + 1):
        tt.append(delta * i)
        tt1.append(delta * i)
    tt1.pop()
    # Input flow of cars horizontally, uniform [0.2, 0.3] cars/s
    hinputcars = uniform.rvs(loc=0.2, scale=0.1, size=samples)
    # Input flow of cars vertically, uniform [0.4, 0.6] cars/s
    vinputcars = uniform.rvs(loc=0.5, scale=0.2, size=samples)

    """CREATION OF SECTIONS"""
    hsections = [Tml.SectionLight(15, True, 3, 3), Tml.SectionLight(10, False, 0, 0)]
    hlambda = [4, 5]
    nhsections = len(hsections)
    print("There are ", nhsections, "horizontal sections")

    """For vertical, we have a list of each vertical section group. There's only one horizontal way, 
    but it can have different vertical intersections"""
    vsection0 = [Tml.SectionLight(20, True, 0, 0), Tml.SectionLight(15, False, 0, 0)]
    vlambda = [4, 5]
    vsections = [vsection0]
    nvsections = len(vsections)
    print("With ", nvsections, "intersections")

    """LOOP TO REPLICATE THE TIMING SEQUENCE OF TL IN EACH CROSS SECTION"""
    indexH = []
    for j in range(0, nhsections):
        if hsections[j].tl:
            indexH.append(j)
    for j in range(0, len(indexH)):
        Tml.invert_trafficlight(hsections[indexH[j]], vsections[j][0])

    """LOOP"""
    for i in range(0, samples):

        """FLOW"""
        Tml.new_flow_horizontal_blind(hsections, i, hlambda, delta)
        Tml.new_flow_vertical_blind(vsections, i,vlambda, delta)

        """MARKING"""
        Tml.new_marking_horizontal_blind(hsections, hinputcars, i, delta)
        Tml.new_marking_vertical_blind(vsections, vinputcars, i, delta)

        """STATE MACHINE"""
        for j in range(0, nhsections):
            Tml.state_machine(hsections[j], i)
        for j in range(0, nvsections):
            for m in range(0, len(vsection0)):
                Tml.state_machine(vsections[j][m], i)

    """PLOT"""
    plt.figure(1)
    plt.plot(tt, hsections[0].m, 'b', tt, vsection0[0].m, 'g', tt, hsections[1].m, 'b--', tt, vsection0[1].m, 'g--', tt,
             hsections[0].lstate, 'r+')
    plt.legend(["mH1", "mV1", "mH2", "mV2"])
    plt.ylabel("Marking [cars]")
    plt.xlabel("Time [s]")
    plt.show()


def main_mpc():
    """INITIALIZATION"""
    delta = 8  # Time discretized in periods of delta = 8 seconds.
    samples = 50  # Total samples
    tt = []  # time vector so I can plot events in real time.
    tt1 = []
    for i in range(0, samples + 1):
        tt.append(delta * i)
        tt1.append(delta * i)
    tt1.pop()
    # Input flow of cars horizontally, uniform cars/s
    hinputcars = uniform.rvs(loc=0.2, scale=0.1, size=samples+3)
    # Input flow of cars vertically, uniform cars/s
    vinputcars = uniform.rvs(loc=0.4, scale=0.2, size=samples+3)
    vinputcars2 = uniform.rvs(loc=0.3, scale=0, size=samples+3)

    """CREATION OF SECTIONS"""
    hsections = [Tml.SectionLight(15, True, 3, 3), Tml.SectionLight(10, False, 0, 0)]
    hlambda = [4, 5]
    nhsections = len(hsections)
    print("There are ", nhsections, "horizontal sections")

    """For vertical, we have a list of each vertical section group. There's only one horizontal way, 
    but it can have different vertical intersections"""
    vsection0 = [Tml.SectionLight(20, True, 0, 0), Tml.SectionLight(15, False, 0, 0)]
    vlambda = [4, 5]
    vsections = [vsection0]
    nvsections = len(vsections)
    print("With ", nvsections, "intersections")

    """LOOP TO REPLICATE THE TIMING SEQUENCE OF TL IN EACH CROSS SECTION"""
    indexH = []
    for i in range(0, nhsections):
        if hsections[i].tl:
            indexH.append(i)
    for i in range(0, len(indexH)):
        Tml.invert_trafficlight(hsections[indexH[i]], vsections[i][0])

    """MPC CONTROL
    Control horizon: 4 periods
    
    """
    # Possible combinations starting from green
    greenstart = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 2], [0, 1, 2, 2], [0, 1, 2, 3],
                  [1, 2, 2, 2], [1, 2, 2, 3], [1, 2, 3, 0]]
    redstart = [[2, 2, 2, 2], [2, 2, 2, 3], [2, 2, 3, 0], [2, 3, 0, 0], [2, 3, 0, 1],
                [3, 0, 0, 0], [3, 0, 0, 1], [3, 0, 1, 2]]

    """INITIALIZATION FOR STATE 0"""
    """FLOW"""
    Tml.new_flow_horizontal_blind(hsections, 0, hlambda, delta)
    Tml.new_flow_vertical_blind(vsections, 0, vlambda, delta)

    """MARKING"""
    Tml.new_marking_horizontal_blind(hsections, hinputcars, 0, delta)
    Tml.new_marking_vertical_blind(vsections, vinputcars, 0, delta)

    """LOOP"""
    for i in range(1, samples):  # Iterate among all samples wanted
        """CURRENT STATE = INITIAL STATE"""
        if i < samples/2:
            inputV = Tml.inputcars(vinputcars, i)
        else:
            inputV = Tml.inputcars(vinputcars2, i)
        inputH = Tml.inputcars(hinputcars, i)
        sectionH = copy.deepcopy(hsections)
        sectionV = copy.deepcopy(vsections)
        state = hsections[0].lstate[i-1]
        next_state = 0

        """CALCULATE NEXT STATE"""
        if state == 0 or state == 2:
            # Gets the correct sequence for each traffic light
            if state == 0:
                sequenceH = greenstart
                sequenceV = redstart
            else:
                sequenceH = redstart
                sequenceV = greenstart
            flow = []  # Vector to fill with each flow combination so after I select the maximum

            for j in range(0, len(sequenceH)):  # Iterate among the possible 8 combinations to find the maximum ec 12.
                for m in range(0, len(sequenceH[0])):  # Iteration for the next 4 states
                    """FLOW"""
                    Tml.new_flow_horizontal_mpc(sectionH, i, hlambda, delta, sequenceH[j], m)
                    Tml.new_flow_vertical_mpc(sectionV, i, vlambda, delta, sequenceV[j], m)

                    """MARKING"""
                    Tml.new_marking_horizontal_mpc(sectionH, inputH, i, delta, m)
                    Tml.new_marking_vertical_mpc(sectionV, inputV, i, delta, m)

                """GET FLOW"""
                # appends the flow for each combination so later I know the index of the maximum flow combination
                flow.append(sectionH[1].f[i + 3] + sectionV[0][1].f[i + 3])
                Tml.remove(sectionH, sectionV)

            """GET THE INDEX FOR THE MAXIMUM FLOW COMBINATION"""
            maxflow = max(flow)
            index = 0
            for j in range(0, len(sequenceH)):
                if flow[j] == maxflow: index = j

            """GET THE FIRST STATE OF THAT SEQUENCE"""
            next_state = sequenceH[index][0]

        elif state == 1:  # next state will be red (2)
            next_state = 2
        elif state == 3:  # next state will be green (0)
            next_state = 0

        """APPLY NEXT STATE"""
        hsections[0].lstate.append(next_state)
        vsections[0][0].lstate.append(Tml.invert_nextstate(next_state))

        """CALCULATE NEW FLOW"""
        Tml.new_flow_horizontal_blind(hsections, i, hlambda, delta)
        Tml.new_flow_vertical_blind(vsections, i, vlambda, delta)

        """CALCULATE NEW MARKING"""
        Tml.new_marking_horizontal_blind(hsections, hinputcars, i, delta)
        if i < samples/2:
            Tml.new_marking_vertical_blind(vsections, vinputcars, i, delta)
        else:
            Tml.new_marking_vertical_blind(vsections, vinputcars2, i, delta)
    """PLOT"""
    plt.figure(1)
    plt.plot(tt, hsections[0].m, 'b', tt, vsection0[0].m, 'g', tt, hsections[1].m, 'b--', tt, vsection0[1].m, 'g--', tt1, hsections[0].lstate, 'r+')
    plt.legend(["mH1", "mV1", "mH2", "mV2"])
    plt.ylabel("Marking [cars]")
    plt.xlabel("Time [s]")
    """plt.figure(2)
    plt.plot(tt1, hsections[0].f, 'b', tt1, vsection0[0].f, 'g', tt1, hsections[1].f, 'b--', tt1, vsection0[1].f, 'g--')
    plt.legend(["fH1", "fV1", "fH2", "fV2"])
    plt.ylabel("Flow [cars/s]")
    plt.xlabel("Time [s]")"""
    plt.show()


if __name__ == '__main__':
    # Execution of one intersection with traffic light without any kind of control algorithm
    main_nolight_blind()
    # Execution of one intersection with traffic light with MPC algorithm
