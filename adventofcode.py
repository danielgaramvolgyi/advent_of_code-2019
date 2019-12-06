import collections
from enum import Enum
from typing import List


# DAY 1 #


def day1_part1(inputFileName):
    lines = map(int, list(open(inputFileName)))
    return sum((x // 3 - 2 for x in lines))


def day1_part2(inputFileName):
    lines = map(int, list(open(inputFileName)))
    total = 0
    for fuel in lines:
        while fuel > 0:
            fuel = fuel // 3 - 2
            total += max(fuel, 0)
    return total


# DAY 2 #


def day2_part1(inputFileName):
    OPCODE_ADD = 1
    OPCODE_MULT = 2
    OPCODE_HALT = 99
    STEPFORWARD = 4

    with open(inputFileName, 'r') as fileStream:
        opcodes = [int(opcode) for opcode in fileStream.read().replace('\n', '').split(',')]
        opcodes[1] = 12
        opcodes[2] = 2
        currentPosition = 0

        while True:
            if opcodes[currentPosition] == OPCODE_ADD:
                opcodes[opcodes[currentPosition + 3]] = opcodes[opcodes[currentPosition + 1]] + opcodes[
                    opcodes[currentPosition + 2]]
            elif opcodes[currentPosition] == OPCODE_MULT:
                opcodes[opcodes[currentPosition + 3]] = opcodes[opcodes[currentPosition + 1]] * opcodes[
                    opcodes[currentPosition + 2]]
            elif opcodes[currentPosition] == OPCODE_HALT:
                break
            else:
                raise Exception

            currentPosition += STEPFORWARD

        return opcodes[0]


def day2_part2(inputFileName):
    OPCODE_ADD = 1
    OPCODE_MULT = 2
    OPCODE_HALT = 99
    STEPFORWARD = 4

    PUZZLE_INPUT = 19690720

    with open(inputFileName, 'r') as fileStream:
        startingOpcodes = [int(opcode) for opcode in fileStream.read().replace('\n', '').split(',')]
        for noun in range(100):
            for verb in range(100):
                opcodes = list(startingOpcodes)  # copy original list

                opcodes[1] = noun
                opcodes[2] = verb
                currentPosition = 0
                while True:
                    if opcodes[currentPosition] == OPCODE_ADD:
                        opcodes[opcodes[currentPosition + 3]] = opcodes[opcodes[currentPosition + 1]] + opcodes[
                            opcodes[currentPosition + 2]]
                    elif opcodes[currentPosition] == OPCODE_MULT:
                        opcodes[opcodes[currentPosition + 3]] = opcodes[opcodes[currentPosition + 1]] * opcodes[
                            opcodes[currentPosition + 2]]
                    elif opcodes[currentPosition] == OPCODE_HALT:
                        break
                    else:
                        raise Exception

                    currentPosition += STEPFORWARD

                if opcodes[0] == PUZZLE_INPUT:
                    return 100 * noun + verb


# DAY 3 #


def dist(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def add(pairA, pairB):
    return tuple((a + b for a, b in zip(pairA, pairB)))


def get_direction(ch):
    if ch == 'U':
        return (0, 1)
    elif ch == 'D':
        return (0, -1)
    elif ch == 'R':
        return (1, 0)
    elif ch == 'L':
        return (-1, 0)
    else:
        raise Exception


def day3_part1(inputFileName):
    wires = []

    with open(inputFileName, 'r') as fileStream:
        for line in fileStream:
            currentWire = [(current[0], int(current[1:])) for current in line.split(',')]
            wires.append(currentWire)

    visitedCoordinates = [set(), set()]

    for i in range(2):
        currentPos = (0, 0)
        for (dir, length) in wires[i]:
            currentDir = get_direction(dir)
            for j in range(length):
                currentPos = add(currentPos, currentDir)
                visitedCoordinates[i].add(currentPos)

    return min(dist((0, 0), coord) for coord in (visitedCoordinates[0] & visitedCoordinates[1]))  # set intersection


def day3_part2(inputFileName):
    wires = []

    with open(inputFileName, 'r') as fileStream:
        for line in fileStream:
            currentWire = [(current[0], int(current[1:])) for current in line.split(',')]
            wires.append(currentWire)

    visitedCoords = [dict(), dict()]

    for i in range(2):
        currentPos = (0, 0)
        stepsTaken = 0
        for (dir, length) in wires[i]:
            currentDir = get_direction(dir)
            for j in range(length):
                stepsTaken += 1
                currentPos = add(currentPos, currentDir)
                if currentPos not in visitedCoords[i]:
                    visitedCoords[i][currentPos] = stepsTaken

    return min(visitedCoords[0][currentPos] + visitedCoords[1][currentPos]
               for currentPos in (visitedCoords[0].keys() & visitedCoords[1].keys()))


# DAY 4 #


def day4_part1():
    RANGE_LOWER = 172930
    RANGE_UPPER = 683082
    total = 0
    for i in range(RANGE_LOWER, RANGE_UPPER):
        numlist = [int(d) for d in str(i)]
        if numlist == sorted(numlist) and len(set(numlist)) < len(numlist):
            total += 1

    return total


def day4_part2():
    RANGE_LOWER = 172930
    RANGE_UPPER = 683082
    total = 0
    for i in range(172930, 683082):
        numlist = [int(d) for d in str(i)]
        if numlist == sorted(numlist):
            frequencyDict = collections.defaultdict(int)
            for d in numlist:
                frequencyDict[d] += 1
            if 2 in frequencyDict.values():
                total += 1

    return total


# DAY 5 #


class Opcodes(Enum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


def number_of_read_parameters(opcode):
    if opcode in [Opcodes.HALT, Opcodes.INPUT]:
        return 0
    elif opcode in [Opcodes.OUTPUT]:
        return 1
    else:
        return 2


def has_write_parameter(opcode):
    return opcode in [Opcodes.INPUT, Opcodes.ADD, Opcodes.MULT, Opcodes.LESS_THAN, Opcodes.EQUALS]


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


def parse_opcode(packedOpcode):
    opcode = Opcodes(packedOpcode % 100)
    parameterModes = [ParameterMode(packedOpcode // 100 % 10),  # hundreds digit
                      ParameterMode(packedOpcode // 1000 % 10)]  # thousands digit
    return opcode, parameterModes


def parse_parameter(opcodes, parameterMode, parameter):
    if parameterMode == parameterMode.IMMEDIATE:
        return parameter
    else:
        return opcodes[parameter]


def run_program(opcodes, inputCode):
    instructionPointer = 0

    while True:
        opcode, parameterModes = parse_opcode(opcodes[instructionPointer])
        firstParam, secondParam, writeParam = 0, 0, 0

        numberOfReadParams = number_of_read_parameters(opcode)
        if numberOfReadParams >= 1:
            firstParam = parse_parameter(opcodes, parameterModes[0], opcodes[instructionPointer + 1])
        if numberOfReadParams >= 2:
            secondParam = parse_parameter(opcodes, parameterModes[1], opcodes[instructionPointer + 2])
        if has_write_parameter(opcode):
            writeParam = opcodes[instructionPointer + numberOfReadParams + 1]
        numberOfParams = numberOfReadParams + int(has_write_parameter(opcode))

        if opcode == Opcodes.ADD:
            opcodes[writeParam] = firstParam + secondParam
            instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.MULT:
            opcodes[writeParam] = firstParam * secondParam
            instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.INPUT:
            opcodes[writeParam] = inputCode
            instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.OUTPUT:
            print(firstParam)
            instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.JUMP_IF_TRUE:
            if firstParam != 0:
                instructionPointer = secondParam
            else:
                instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.JUMP_IF_FALSE:
            if firstParam == 0:
                instructionPointer = secondParam
            else:
                instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.LESS_THAN:
            opcodes[writeParam] = int(firstParam < secondParam)
            instructionPointer += numberOfParams + 1

        elif opcode == Opcodes.EQUALS:
            opcodes[writeParam] = int(firstParam == secondParam)
            instructionPointer += numberOfParams + 1
        else:
            break


def day5_part1(inputFileName):
    with open(inputFileName, 'r') as fileStream:
        opcodes = [int(opcode) for opcode in fileStream.read().replace('\n', '').split(',')]
    INPUT_CODE = 1
    run_program(opcodes, INPUT_CODE)


def day5_part2(inputFileName):
    with open(inputFileName, 'r') as fileStream:
        opcodes = [int(opcode) for opcode in fileStream.read().replace('\n', '').split(',')]
    INPUT_CODE = 5
    run_program(opcodes, INPUT_CODE)


# DAY 6 #


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.parent: str = None
        self.children: List[str] = []

    def __repr__(self):
        return str({"name": self.name, "parent:": self.parent, "children": self.children})

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)


def build_orbit_tree(inputFileName):
    orbitTree = {}

    with open(inputFileName, 'r') as fileStream:
        orbits = [line.replace('\n', '').split(')') for line in fileStream]
    for parent, child in orbits:
        if parent not in orbitTree:
            orbitTree[parent] = TreeNode(parent)
        if child not in orbitTree:
            orbitTree[child] = TreeNode(child)
        orbitTree[parent].add_child(child)
        orbitTree[child].set_parent(parent)

    return orbitTree


def set_descendants(rootName, tree, descendants):
    for child in tree[rootName].children:
        set_descendants(child, tree, descendants)

    root_descendants = sum(descendants[childName] for childName in tree[rootName].children) + len(tree[rootName].children)
    descendants[rootName] = root_descendants


def day6_part1(inputFileName):
    orbitTree = build_orbit_tree(inputFileName)
    descendants = collections.defaultdict(int)
    set_descendants('COM', orbitTree, descendants)
    return sum(descendants.values())


def path_to_root(nodeName, rootName, tree):
    if nodeName == rootName:
        return []
    else:
        return path_to_root(tree[nodeName].parent, rootName, tree) + [tree[nodeName].parent]


def day6_part2(inputFileName):
    orbitTree = build_orbit_tree(inputFileName)

    san_path = set(path_to_root('SAN', 'COM', orbitTree))
    you_path = set(path_to_root('YOU', 'COM', orbitTree))

    return len(san_path ^ you_path)  # symmetric difference


# MAIN #


if __name__ == '__main__':
    print(day6_part2("input.txt"))
