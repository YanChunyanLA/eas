import web
import json
import numpy as np

c_config_file = './config.json'
c_log_dir = '../storages/logs'


def t_debug(*args):
    print('debug', *args)


def u_read_json(file):
    with open(file, 'r') as fp:
        data = json.load(fp)
    return data


def u_file_lines(file):
    with open(file, 'r') as fp:
        num = len(fp.readlines())
    return num


def u_file_data_by_lines(file, lines):
    data = np.loadtxt(file, dtype=float, delimiter=',')
    return data[lines]


config_cache = None


def config(seq, dft=None):
    global config_cache

    if config_cache is None:
        config_cache = u_read_json(c_config_file)

    result = config_cache
    for key in seq.split('.'):
        t_debug(key)
        if key in result:
            result = result[key]
            t_debug(result)
        else:
            return dft

    return result


render = web.template.render('./templates/')


class index:
    def GET(self):
        title = config('app.name')
        functions = list(set(map(lambda d: d['function'], config('result', []))))

        return render.index(title, functions)


class get_algorithm:
    def __init__(self):
        web.header('Content-Type', 'application/json')

    def GET(self):
        query = web.input()
        function_name = query['functionName']

        result = list(set(list(map(lambda d: d['algorithm'],
                                   filter(lambda d: d['function'] == function_name,
                                          config('result', []))))))
        t_debug(result)
        return json.dumps(result)


class get_log_file:
    def __init__(self):
        web.header('Content-Type', 'application/json')

    def GET(self):
        query = web.input()
        t_debug('query', query)
        function_name = query['functionName']
        algorithms = json.loads(query['algorithms'])

        t_debug(function_name, algorithms)

        records = list(filter(lambda d: d['algorithm'] in algorithms,
                             filter(lambda d: d['function'] == function_name,
                                    config('result', []))))

        def wrap(d):
            d['numOfLines'] = u_file_lines(c_log_dir + '/' + d['filename'])
            return d

        records = list(map(wrap, records))

        return json.dumps(records)


class get_graph_data:
    def __init__(self):
        web.header('Content-Type', 'application/json')

    def GET(self):
        query = web.input()
        line_sets = json.loads(query['lineSets'])
        # [{filename: '', algorithm: 'GA', lines: []}, ...]
        t_debug('line_sets', line_sets)

        result = []
        for i, line_set in enumerate(line_sets):
            t_debug('line_set', line_set)
            data = u_file_data_by_lines(c_log_dir + '/' + line_set['filename'], np.array(line_set['lines']) - 1)
            for line, d in zip(line_set['lines'], data.tolist()):
                result.append({
                    'legend': line_set['algorithm'] + '-' + str(i) + '-' + str(line),
                    'data': d,
                })

        return json.dumps(result)


if __name__ == "__main__":
    urls = (
        '/', 'index',
        '/get_algorithm', 'get_algorithm',
        '/get_log_file', 'get_log_file',
        '/get_graph_data', 'get_graph_data',
    )
    app = web.application(urls, globals())
    app.run()

