from tabulate import tabulate
import json

with open('./json/q_table.json') as json_file:
    data = json.load(json_file)

    headers, table = ['', 'HIT', 'STAND', 'DOUBLE'], []
    for state in data['states']:
        table.append(['state({}, {})'.format(state['state'][0], state['state'][1]),
                      state['hit'], state['stand'], state['double']])

    print tabulate(table, headers, tablefmt="fancy_grid")
