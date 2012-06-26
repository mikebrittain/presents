import time
import re

from logster_helper import MetricObject, LogsterParser
from logster_helper import LogsterParsingException

from logster_helper import percentile

class PerfLogster(LogsterParser):

    def __init__(self, option_string=None):
        # Perf data that we want to track for each log entry.
        self.signed_in_ms = []
        self.signed_out_ms = []
        
        # Pattern to match lines we are interested in and capturing fields.
        self.reg = re.compile('.* (?P<display_mode>\w+) (?P<user_id>[\d\-]+) (?P<php_bytes>\d+) (?P<php_usec>\d+) (?P<apache_usec>\d+)$')

    def parse_line(self, line):
        '''Digest the contents of log file one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            # Apply regular expression to each line...
            regMatch = self.reg.match(line)

            if regMatch:
                fields = regMatch.groupdict()
                php_ms = int(fields['php_usec']) / 1000
                user_id = fields['user_id']
                if (user_id == "-"):
                    self.signed_out_ms.append(php_ms)
                else:
                    self.signed_in_ms.append(php_ms)

            else:
                raise LogsterParsingException, "regmatch failed to match"

    except Exception, e:
        raise LogsterParsingException, "regmatch or contents failed with %s" % e


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''
        self.duration = duration

        self.signed_in_ms.sort()
        self.signed_out_ms.sort()

        # Return a list of metrics objects (for output)
        return [
            MetricObject("signed_out_reqs",      len(self.signed_out_ms), "Requests"),
            MetricObject("signed_out_ms_min",    self.signed_out_ms[0], "ms"),
            MetricObject("signed_out_ms_median", percentile(self.signed_out_ms, 0.5), "ms"),
            MetricObject("signed_out_ms_perc95", percentile(self.signed_out_ms, 0.95), "ms"),
            MetricObject("signed_out_ms_max",    self.signed_out_ms[-1], "ms"),
            
            MetricObject("signed_in_reqs",       len(self.signed_in_ms), "Requests"),
            MetricObject("signed_in_ms_min",     self.signed_in_ms[0], "ms"),
            MetricObject("signed_in_ms_median",  percentile(self.signed_in_ms, 0.5), "ms"),
            MetricObject("signed_in_ms_perc95",  percentile(self.signed_in_ms, 0.95), "ms"),
            MetricObject("signed_in_ms_max",     self.signed_in_ms[-1], "ms"),
        ]
