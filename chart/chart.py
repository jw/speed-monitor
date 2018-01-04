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
        """This is very likely way too slow!"""

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
        #   upload    is the number of bits per second in upload
        #   download  is the number of bits per second in download
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
        upload_combined = []
        download_combined = []
        for label in lines.keys():

            # label is <client_id> ":" <server_id>
            (client_id, separator, server_id) = label.partition(":")
            client = Client.objects.get(id=client_id)
            server = Server.objects.get(id=server_id)
            fancy_label = "from {0} (in {1}) to {2} (in {3})".format(
                client.ip, client.country.name,
                server.host, server.country.name)
            logger.debug("Converted label {0} to {1}.".
                         format(label, fancy_label))

            upload_line = []
            download_line = []
            for key in sorted(lines[label].keys()):

                upload = 0
                download = 0

                for entry in lines[label][key]:
                    upload += entry[0]
                    download += entry[1]
                upload = upload / len(lines[label][key])
                download = download / len(lines[label][key])

                upload_line.append({'x': str(key), 'y': upload})
                download_line.append({'x': str(key), 'y': download})
                upload_combined.append({'x': str(key), 'y': upload})
                download_combined.append({'x': str(key), 'y': download})

            datasets.append(DataSet(type='line',
                                    label="Upload " + fancy_label,
                                    borderColor="green",
                                    data=upload_line))

            datasets.append(DataSet(type='line',
                                    label="Download " + fancy_label,
                                    borderColor="blue",
                                    data=download_line))

        datasets.append(DataSet(type='line',
                                label='Upload combined',
                                borderColor='yellow',
                                data=sorted(upload_combined,
                                            key=lambda e: e['x'])))

        datasets.append(DataSet(type='line',
                                label='Download combined',
                                borderColor='red',
                                data=sorted(download_combined,
                                            key=lambda e: e['x'])))

        if logger.isEnabledFor(logging.DEBUG):
            import pprint
            pp = pprint.PrettyPrinter(indent=4, width=150)
            logger.debug(pp.pformat(datasets))

        return datasets
