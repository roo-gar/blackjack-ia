from ia import QMatrix, QMatrixEntry, State, HIT, STAND, DOUBLE

import json


def create_q_matrix():
    with open('./json/q_table.json') as json_file:
        data = json.load(json_file)

        entries = []
        for entry in data['entries']:
            print entry['state']['p'], entry['state']['q'], entry['hit'], entry['stand'], entry['double']
        #     entries.append(QMatrixEntry(State(entry['state']['p'], entry['state']['q']), HIT, entry['hit']))
        #     entries.append(QMatrixEntry(State(entry['state']['p'], entry['state']['q']), STAND, entry['stand']))
        #     entries.append(QMatrixEntry(State(entry['state']['p'], entry['state']['q']), DOUBLE, entry['double']))
        #     return QMatrix(entries)


create_q_matrix()
