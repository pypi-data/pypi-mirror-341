#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2025 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Gather statisticxs  from container in osdf scaling tests
"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import csv
import re
from datetime import datetime
from pathlib import Path
import logging

from htcondor import JobEventLog
from htcondor2 import JobEventType
from htcondor2 import JobEvent


class ProcessLog:
    """
    Represents a logged job as defined by cluster ID and ProcessID
    """
    def __init__(self, path, event, logger=None):
        """
        :param Path|str: path condor log file
        :param JobEvent event: first event seen with this cluster id
`        :param logging.Logger logger: use caller's or create error only
        """
        self.path = path
        self.terminate = None
        self.terminated_normally = None
        self.execute = None
        self.execute_host = None
        self.execute_history = list()
        self.submit = None
        self.submit_host = ''
        self.glide_in_slot = 'N/A'
        self.log_notes = ''
        self.submit_history = list()
        self.held = list()
        self.cluster = event.cluster
        self.process = event.proc
        self.logger = logger
        self.memory_usage = list()
        self.exit_code = None
        self.exit_who = None
        self.exit_by_signal = False
        self.aborted = None
        self.memory_use = None
        self.memory_request = None
        self.memory_allocated = None
        self.disk_use = None
        self.disk_request = None
        self.disk_allocated = None

        self.sent_bytes = None
        self.received_bytes = None
        self.evicted = list()
        self.in_transfer_times = list()
        self.in_transfer_error = False
        self.out_transfer_times = list()
        self.out_transfer_error = False

        self.disconnected = list()
        self.reconnect_failed = list()
        self.reconnected = list()

        self.run_local_usage = None

        if self.logger is None:
            self.logger = logging.getLogger('ProcessLog')
            self.logger.setLevel(logging.ERROR)

        self.update(event)
        pass

    def update(self, event):
        """
        Updateobject  with what we want to keep

        :param JobEvent event: A single event from a job log
        :return: None
        """

        event_text = str(event)

        if event.type == JobEventType.SUBMIT:
            if self.submit is None:
                self.submit = event.timestamp
                self.submit_host = event.get('SubmitHost')
                self.log_notes = event.get('LogNotes')

            submit_dict = {'time': event.timestamp, 'host': self.submit_host, 'notes': self.log_notes}
            self.execute_history.append(submit_dict)
        elif event.type == JobEventType.EXECUTE:
            m = re.match('^.*addrs=([\\d\\.]+).*alias=([^&]+)', event.get('ExecuteHost'))
            if m:
                host = (m.group(1), m.group(2))
            else:
                host = event.get('ExecuteHost')
            if self.execute is None:
                self.execute = event.timestamp
                self.execute_host = host
            exe_dict = {'time': event.timestamp, 'host': host}
            self.execute_history.append(exe_dict)
        elif event.type == JobEventType.IMAGE_SIZE:
            self.memory_usage.append((event.get('MemoryUsage'), event.timestamp))
        elif event.type == JobEventType.JOB_TERMINATED:
            self.terminate = event.timestamp
            toe = event.get('ToE')
            if toe is not None:
                try:
                    self.exit_by_signal = toe['ExitBySignal']
                    self.exit_code = toe['ExitCode']
                    self.exit_who = toe['Who']
                    self.memory_usage.append((event.get('Memory'), event.timestamp))
                    self.sent_bytes = event.get('SentBytes')
                    self.received_bytes = event.get('ReceivedBytes')
                    toe_str = str(event)
                    for line in toe_str.splitlines():
                        mem_match = re.match('^.*Memory[^\\d]+(\\d+)[^\\d]+(\\d+)[^\\d]+(\\d+)', line)
                        if mem_match:
                            self.memory_use = mem_match.group(1)
                            self.memory_request = int(mem_match.group(2))
                            self.memory_allocated = mem_match.group(3)
                        disk_match = re.match('^.*Disk[^\\d]+(\\d+)[^\\d]+(\\d+)[^\\d]+(\\d+)', line)
                        if disk_match:
                            self.disk_use = disk_match.group(1)
                            self.disk_request = int(disk_match.group(2))
                            self.disk_allocated = disk_match.group(3)

                except KeyError:
                    pass
            else:
                self.exit_code = event.get('ReturnValue')
                self.terminated_normally = event.get('TerminatedNormally')
                self.received_byteXs = event.get('TotalReceivedBytes')
                self.sent_bytes = event.get('TotalSentBytes')
                self.run_local_usage = event.get('RunLocalUsage')
            self.logger.debug(f'Job terminated event data has {len(list(event.keys()))} keys')
            spaces = ' ' * 4
            for k, v in event.items():
                self.logger.debug(f'{spaces}Key {k}: {v}')
        elif event.type == JobEventType.JOB_ABORTED:
            self.aborted = event.get('Reason')
        elif event.type == JobEventType.JOB_EVICTED:
            self.evicted.append(event.timestamp)
        elif event.type == JobEventType.JOB_HELD:
            self.held.append((event.get('HoldReasonCode'), event.get('HoldReasonsubCode'), event.timestamp))
            if 'transfer input files failure' in event_text:
                self.in_transfer_error = True
            elif 'transfer output files failure' in event_text:
                self.out_transfer_error = True
        elif event.type == JobEventType.JOB_DISCONNECTED:
            self.disconnected.append(event.timestamp)
        elif event.type == JobEventType.JOB_RECONNECT_FAILED:
            self.reconnect_failed.append(event.timestamp)
        elif event.type == JobEventType.JOB_AD_INFORMATION:
            # dump of selected job information
            self.logger.error(f'Job AD information event has {len(list(event.keys()))} keys')
            try:
                glide_in_slot = self.get_item("JOB_GLIDEIN_SiteWMS_Slot", event.items())
                self.logger.info(f'Job AD information event has JOB_GLIDEIN_SiteWMS_Slot = '
                                 f'{glide_in_slot}')
                if '$$' not in glide_in_slot:
                    self.glide_in_slot = glide_in_slot
            except KeyError:
                pass
        elif event.type == JobEventType.REMOTE_ERROR:
            self.logger.error(f'Remote error event has {len(list(event.keys()))} keys\n   {event_text}')
        elif event.type == JobEventType.JOB_RECONNECTED:
            self.reconnected.append(event.timestamp)
        elif event.type == JobEventType.FILE_TRANSFER:
            if self.multiline_in("input files", event_text.lower()):
                if self.multiline_in("started", event_text.lower()):
                    xfer_type = 'start'
                elif self.multiline_in("finished", event_text.lower()):
                    xfer_type = 'finish'
                else:
                    xfer_type = 'unknown'
                    self.in_transfer_error = True

                self.in_transfer_times.append((event.timestamp, xfer_type))

            if self.multiline_in("output files", event_text.lower()):
                if self.multiline_in("started", event_text.lower()):
                    xfer_type = 'start'
                elif self.multiline_in("finished", event_text.lower()):
                    xfer_type = 'finish'
                else:
                    xfer_type = 'unknown'
                    self.out_transfer_error = True
                self.out_transfer_times.append((event.timestamp, xfer_type))

        else:
            self.logger.error(f'Unexpected job event type: {event.type.name}')

    def multiline_in(self, pattern, text):
        """
        Search the text line by line for the pattern
        :param str pattern: regex to look for
        :param str text: text to search, usually event text
        :return bool: true if the substring is there
        """
        ret = False
        for line in text.splitlines():
            if re.search(pattern, line):
                ret = True
                break
        return ret

    def get_item(self, key, items):
        """
        Event aux info is storedi a list of tuples. Search for te key, return value or raise exceptn
        :param str key: search key
        :param list[tple[str, str]]items: list to earch
        :return str: value
        :raises KeyError: key not found
        """
        for k, v in items:
            if k == key:
                return v
        raise KeyError(f'{key} not in list of {len(items)} items')

    def summary(self, indent=3):
        """
        Prodce a summary of the job
        :param int indent: indent all lines, for inclusion in another report
        :return str: summary of what we know about the job
        """
        ret = ''
        spaces = ' ' * indent
        if self.log_notes is not None:
            ret += f'{spaces}Log notes:{self.log_notes}\n'
        if self.exit_code is not None:
            ret += f'{spaces}ExitCode: {self.exit_code}'
            if self.terminated_normally is not None:
                ret += f' TerminatedNormally: {self.terminated_normally}\n'
        if self.exit_by_signal:
            ret += f'{spaces}ExitBySignal: {self.exit_by_signal}'
        if self.submit is not None and self.execute is not None:
            ret += f'{spaces}Submit to execute: {self.execute - self.submit} seconds\n'
        if self.terminate is not None and self.execute is not None:
            ret += f'{spaces}Execution time: {self.terminate - self.execute} seconds\n'
        if self.memory is not None:
            ret += f'{spaces}Memory usage: {self.memory} MB\n'
        if self.memory_usage is not None:
            ret += f'{spaces}Memory usage: {self.memory_usage} MB\n'
        if self.run_local_usage is not None:
            ret += f'{spaces}Run local usage: {self.run_local_usage}\n'
        return ret

    @staticmethod
    def get_col_labels():
        """
        return list of labels for status information
        :return list[str]: the labels
        """
        return ['Path', 'Name', 'Submitted', 'ClusterID', 'N-exec', 'First EP', 'Glide-in slot',
                'Q-time', 'Run-time', 'Exit-code', 'N-holds',
                'Memory use MB', 'Memory request MB', 'Memory allocated MB',
                'Disk use GB', 'Disk request GB', 'Disk allocated GB',
                'Local Uni', 'Signal', 'Aborted',
                'Disconnected count', 'Evicted count', 'Reconnected count', 'Reconnect_failed',
                'Terminated normally', 'N-xfer', 'in Xfer time', 'in Xfer error', 'out Xfer time', 'out Xfer error',
                ]

    def get_stats(self):
        """
        Summarize the job statistics
        :return list[str]: the statistics
        """
        ret = [str(self.path.absolute())]
        name = self.log_notes
        name = f'{self.cluster}.{self.process:03d}' if name is None else name
        name = name.replace('DAG Node:', '')
        ret.append(name)
        if self.submit is None:
            sub_time = 'NAN'
        else:
            submit_dt = datetime.fromtimestamp(self.submit)
            sub_time = submit_dt.strftime('%Y-%m-%d %H:%M:%S')
        ret.append(sub_time)
        ret.append(self.cluster)
        nexec = len(self.execute_history)
        ret.append(f'{nexec}')
        if self.execute is None:
            ret.append('N/A')
        else:
            ret.append(f'{self.execute_host[0]} - {self.execute_host[1]}')
        ret.append(self.glide_in_slot)
        if isinstance(self.execute, (int, float)) and isinstance(self.submit, (int, float)):
            qtime = f"{self.execute - self.submit:.1f}"
        else:
            qtime = 'nan'
        ret.append(qtime)
        if self.terminate is not None and self.execute is not None:
            etime = f"{self.terminate - self.execute:.0f}"
        else:
            etime = 0
        ret.append(etime)
        ret.append(self.exit_code)
        ret.append(f'{len(self.held)}')
        if self.memory_usage is None:
            ret.append('N/A')
            ret.append('N/A')
            ret.append('N/A')
        else:
            ret.append(f'{self.memory_use}')
            ret.append(f'{self.memory_request}')
            ret.append(f'{self.memory_allocated}')
        if self.disk_use is None:
            ret.append('N/A')
            ret.append('N/A')
            ret.append('N/A')
        else:
            ret.append(f'{int(self.disk_use) / 1e6:.3f}')
            ret.append(f'{int(self.disk_request) / 1e6:.3f}')
            ret.append(f'{int(self.disk_allocated) / 1e6:.3f}')

        local_job = 1 if self.run_local_usage is not None else 0
        ret.append(f'{local_job}')
        exit_by_signal = 1 if self.exit_by_signal else 0
        ret.append(f'{exit_by_signal}')
        aborted = 1 if self.aborted else 0
        ret.append(f"{aborted}")
        ret.append(f'{len(self.disconnected)}')
        ret.append(f'{len(self.evicted)}')
        ret.append(f'{len(self.reconnected)}')
        ret.append(f'{len(self.reconnect_failed)}')
        terminated_normally = 1 if self.terminated_normally is not None or self.exit_code == 0 else 0
        ret.append(f'{terminated_normally}')
        xfer_count = len(self.in_transfer_times) + len(self.out_transfer_times)
        ret.append(f'{xfer_count}')
        xfer_start = None
        xfer_end = None
        xfer_err = False

        for time, typ in self.in_transfer_times:
            if typ == 'start':
                xfer_start = time if xfer_start is None or xfer_start < time else xfer_start
            elif typ == 'finish':
                xfer_end = time if xfer_end is None or time > xfer_end else xfer_end
            else:
                xfer_err = True
                xfer_time = 'nan'

        if xfer_start is not None and xfer_end is not None:
            xfer_time = xfer_end - xfer_start
        elif xfer_start is None and xfer_end is None:
            xfer_time = 'nan'
        else:
            xfer_time = 'nan'
            xfer_err = True

        xfer_err |= self.in_transfer_error
        ret.append(f'{xfer_time} s')
        ret.append(f'{xfer_err}')

        xfer_start = None
        xfer_end = None
        xfer_err = False
        for time, typ in self.out_transfer_times:
            if typ == 'start':
                xfer_start = time if xfer_start is None or xfer_start < time else xfer_start
            elif typ == 'finish':
                xfer_end = time if xfer_end is None or time > xfer_end else xfer_end
            else:
                xfer_err = True
        if xfer_start is not None and xfer_end is not None:
            xfer_time = xfer_end - xfer_start
        elif xfer_start is None and xfer_end is None:
            xfer_time = 'nan'
        else:
            xfer_err = True
            xfer_time = 'nan'

        xfer_err |= self.out_transfer_error
        ret.append(f'{xfer_time} s')
        ret.append(f'{xfer_err}')

        return ret


class JobStatistics:
    """
    Create and try to be efficient writing stats on the job
    """
    def __init__(self, path=None, logger=None):
        """

        :param Path|str path: output csv file
        :param logger logger: logger to use
        """
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.jobs = list()

        if self.logger is None:
            self.logger = logging.getLogger('CondorLog')
            self.logger.setLevel(logging.ERROR)

    def add(self, job: ProcessLog):
        """
        Extrct what we need from the job
        :param ProcessLog job:
        :return None:
        """
        self.jobs.append(job)

    def write(self):
        """
        Write the file
        :return:
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            labels = ProcessLog.get_col_labels()
            writer.writerow(labels)

            for job in self.jobs:
                stats = job.get_stats()
                writer.writerow(stats)


class ClusterLogFile():
    """
    Parse the logfile of a cluster of htCondor job that may contain multiple processes.
    """
    processes: dict[tuple[str, str]: JobEvent]

    def __init__(self, path=None, logger=None):
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.processes = dict()
        if self.logger is None:
            self.logger = logging.getLogger('ClusterLogFile')
            self.logger.setLevel(logging.ERROR)

    def process_log(self, path=None):
        """
        Scan the job (BLISTER) log file keeping stats on each process separately
        :return:  None
        """
        if path is None:
            path = self.path

        jel = JobEventLog(str(path))

        event: JobEvent
        for event in jel.events(stop_after=0):
            job_key = (event.cluster, event.proc)
            if job_key not in self.processes:
                self.logger.debug(f'New job_key job: {job_key}')
                self.processes[job_key] = ProcessLog(path, event, logger=self.logger)
            self.processes[job_key].update(event)

        pass

    def print(self, path=None):
        """
        print a list of each job/process seen
        :param str|Path|None path: optional output csv file
        :return:
        """
        labels = ProcessLog.get_col_labels()
        lines = [", ".join(labels)]
        proc_keys = list(self.processes.keys())
        proc_keys.sort()
        for proc_key in proc_keys:
            proc = self.processes[proc_key]
            data = proc.get_stats()
            line = ''
            for column in data:
                line += f'{column}, '
            if len(lines) > 1000:
                self.optional_print(path, lines)
                lines = []
            lines.append(line)
        self.optional_print(path, lines)

    def optional_print(self, out, lines):
        """
        Print text to STDOUT and to file if specified
        :param str|Path|None out: optional output file
        :param list(str) lines: ines to print
        :return: None
        """
        for line in lines:
            print(line)
        if out is not None:
            with Path(out).open('a') as f:
                for line in lines:
                    print(line, file=f)
