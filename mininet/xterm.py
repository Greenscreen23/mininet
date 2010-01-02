#!/usr/bin/env python
"""XTerm creation and cleanup.

Utility functions to run an xterm (connected via screen(1)) on each host.

Requires xterm(1) and GNU screen(1).
"""

import os
import re
from subprocess import Popen

from mininet.util import quietRun

def makeXterm(node, title):
    '''Run screen on a node, and hook up an xterm.

    @param node Node object
    @param title base title
    @return process created
    '''
    title += ': ' + node.name
    if not node.inNamespace:
        title += ' (root)'
    cmd = ['xterm', '-title', title, '-e']
    if not node.execed:
        node.cmdPrint('screen -dmS ' + node.name)
        cmd += ['screen', '-D', '-RR', '-S', node.name]
    else:
        cmd += ['sh', '-c', 'exec tail -f /tmp/' + node.name + '*.log']
    return Popen(cmd)


def cleanUpScreens():
    '''Remove moldy old screen sessions.'''
    r = r'(\d+.[hsc]\d+)'
    output = quietRun('screen -ls').split('\n')
    for line in output:
        m = re.search(r, line)
        if m:
            quietRun('screen -S ' + m.group(1) + ' -X kill')


def makeXterms(nodes, title):
    '''Create XTerms.

    @param nodes list of Node objects
    @param title base title for each
    @return list of created xterm processes
    '''
    return [makeXterm(node, title) for node in nodes]