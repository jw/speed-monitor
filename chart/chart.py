import logging

from jchart import Chart
from jchart.config import Axes, DataSet

from testspeed.models import Result, Client, Server

logger = logging.getLogger(__name__)


class TimeSeriesChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }

    def get_datasets(self, **kwargs):

        results = Result.objects.all()

        #
        # lines follows this bnf:
        #
        # { <label> : { <timestamp>: [ < ( upload, download, ping )+ > ] }
        #
        # where:
        #
        #   label     is < client_id > ":" < server_id >
        #   timestamp is the timestamp a measurement was made
        #   upload    is the number of bits where measured in upload
        #   download  is the number of bits where measured in download
        #   ping      is the number of ms taken between the client server ping
        #

        lines = {}
        for result in results:
            logger.debug("Handling {0}...".format(result))
            dt = result.timestamp.isoformat(timespec='seconds')
            key = "{0}:{1}".format(result.client_id, result.server_id)
            entry = (result.upload, result.download, result.ping)
            if key in lines:
                if result.timestamp in lines[key]:
                    logger.debug("Wow! {0} already in {1}. Appending entry...".
                                 format(dt, lines[key]))
                    lines[key][result.timestamp].append(entry)
                else:
                    logger.debug("Adding {{ {0}: {1} }} to {2}.".
                                 format(result.timestamp, entry, key))
                    lines[key][result.timestamp] = [entry]
            else:
                logger.debug("Creating {{ {0}: {1} }} in {2}.".
                             format(dt, entry, key))  # lines[key]))
                lines[key] = {result.timestamp: [entry]}

        if logger.isEnabledFor(logging.DEBUG):
            import pprint
            pp = pprint.PrettyPrinter(indent=4, width=150)
            logger.debug(pp.pformat(lines))

        # transform to chart
        datasets = []
        combined = []
        for label in lines.keys():

            # label is <client_id> ":" <server_id>
            (client_id, separator, server_id) = label.partition(":")
            client = Client.objects.get(id=client_id)
            server = Server.objects.get(id=server_id)
            fancy_label = "From {0} (in {1}) to {2} (in {3})".format(
                client.ip, client.country.name,
                server.host, server.country.name)
            logger.debug("Converted label {0} to {1}.".
                         format(label, fancy_label))

            line = []
            for key in sorted(lines[label].keys()):
                upload = 0
                for entry in lines[label][key]:
                    upload += entry[0]
                upload = upload / len(lines[label][key])
                line.append({'x': str(key), 'y': upload})
                combined.append({'x': str(key), 'y': upload})

            datasets.append(DataSet(type='line',
                                    label=fancy_label,
                                    borderColor="green",
                                    data=line))

        datasets.append(DataSet(type='line',
                                label='Combined',
                                borderColor='red',
                                data=sorted(combined, key=lambda e: e['x'])))

        if logger.isEnabledFor(logging.DEBUG):
            import pprint
            pp = pprint.PrettyPrinter(indent=4, width=150)
            logger.debug(pp.pformat(datasets))

        return datasets
