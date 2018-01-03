
import pprint

from jchart import Chart
from jchart.config import Axes, DataSet

from testspeed.models import Result, Client, Server


class TimeSeriesChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }

    def get_datasets(self, **kwargs):

        results = Result.objects.all()

        lines = {}
        for result in results:
            key = "{0}:{1}".format(result.client_id, result.server_id)
            entry = (result.upload, result.download, result.ping)
            if key in lines:
                # print("LINES: Found {0}; adding {1}".format(key, entry))
                if result.timestamp in lines[key]:
                    # print("Wow: {0} in {1}!".format(result.timestamp,
                    #                                 lines[key]))
                    lines[key][result.timestamp].append(entry)
                else:
                    lines[key][result.timestamp] = [entry]
            else:
                lines[key] = {result.timestamp: [entry]}

        print()
        pp = pprint.PrettyPrinter(indent=4, width=150)
        pp.pprint(lines)
        print()

        # transform
        datasets = []
        for label in lines.keys():
            print(label)
            (client_id, separator, server_id) = label.partition(":")
            client = Client.objects.get(id=client_id)
            server = Server.objects.get(id=server_id)
            fancy_label = "From {0} (in {1}) to {2} (in {3})".format(
                client.ip, client.country.name,
                server.host, server.country.name)

            print(lines[label])
            line = []
            for key in lines[label].keys():
                upload = 0
                for entry in lines[label][key]:
                    upload += entry[0]
                upload = upload / len(lines[label][key])
                line.append({'x': str(key), 'y': upload})

            print(line)
            datasets.append(DataSet(type='line',
                                    label = fancy_label,
                                    borderColor="green",
                                    data=line))

        print()
        pp = pprint.PrettyPrinter(indent=4, width=150)
        pp.pprint(datasets)
        print()

        return datasets

        # red = [{'y': 0, 'x': '2017-01-02T00:00:00'},
        #         {'y': 1, 'x': '2017-01-03T00:00:00'},
        #         {'y': 4, 'x': '2017-01-04T00:00:00'},
        #         {'y': 9, 'x': '2017-01-05T00:00:00'},
        #         {'y': 16, 'x': '2017-01-06T00:00:00'},
        #         {'y': 25, 'x': '2017-01-07T00:00:00'},
        #         {'y': 36, 'x': '2017-01-08T00:00:00'},
        #         {'y': 49, 'x': '2017-01-09T00:00:00'},
        #         {'y': 64, 'x': '2017-01-10T00:00:00'},
        #         {'y': 81, 'x': '2017-01-11T00:00:00'},
        #         {'y': 100, 'x': '2017-01-12T00:00:00'},
        #         {'y': 121, 'x': '2017-01-13T00:00:00'},
        #         {'y': 144, 'x': '2017-01-14T00:00:00'},
        #         {'y': 169, 'x': '2017-01-15T00:00:00'},
        #         {'y': 196, 'x': '2017-01-16T00:00:00'},
        #         {'y': 225, 'x': '2017-01-17T00:00:00'},
        #         {'y': 256, 'x': '2017-01-18T00:00:00'},
        #         {'y': 289, 'x': '2017-01-19T00:00:00'},
        #         {'y': 324, 'x': '2017-01-20T00:00:00'},
        #         {'y': 361, 'x': '2017-01-21T00:00:00'},
        #         {'y': 400, 'x': '2017-01-22T00:00:00'},
        #         {'y': 441, 'x': '2017-01-23T00:00:00'},
        #         {'y': 484, 'x': '2017-01-24T00:00:00'},
        #         {'y': 529, 'x': '2017-01-25T00:00:00'},
        #         {'y': 900, 'x': '2017-02-01T00:00:00'}]
        #
        # green = [{'y': 1000, 'x': '2017-01-02T00:00:00'},
        #         {'y': 1001, 'x': '2017-01-03T00:00:00'},
        #         {'y': 1004, 'x': '2017-01-04T00:00:00'},
        #         {'y': 1009, 'x': '2017-01-05T00:00:00'},
        #         {'y': 1016, 'x': '2017-01-06T00:00:00'},
        #         {'y': 1025, 'x': '2017-01-07T00:00:00'},
        #         {'y': 1036, 'x': '2017-01-08T00:00:00'},
        #         {'y': 1049, 'x': '2017-01-09T00:00:00'},
        #         {'y': 1064, 'x': '2017-01-10T00:00:00'},
        #         {'y': 1081, 'x': '2017-01-11T00:00:00'},
        #         {'y': 1100, 'x': '2017-01-12T00:00:00'},
        #         {'y': 1121, 'x': '2017-01-13T00:00:00'},
        #         {'y': 1144, 'x': '2017-01-14T00:00:00'},
        #         {'y': 1169, 'x': '2017-01-15T00:00:00'},
        #         {'y': 1196, 'x': '2017-01-16T00:00:00'},
        #         {'y': 1225, 'x': '2017-01-17T00:00:00'},
        #         {'y': 1256, 'x': '2017-01-18T00:00:00'},
        #         {'y': 1289, 'x': '2017-01-19T00:00:00'},
        #         {'y': 1324, 'x': '2017-01-20T00:00:00'},
        #         {'y': 1361, 'x': '2017-01-21T00:00:00'},
        #         {'y': 1400, 'x': '2017-01-22T00:00:00'},
        #         {'y': 1441, 'x': '2017-01-23T00:00:00'},
        #         {'y': 1484, 'x': '2017-01-24T00:00:00'},
        #         {'y': 1529, 'x': '2017-01-25T00:00:00'},
        #         {'y': 1900, 'x': '2017-02-01T00:00:00'}]

