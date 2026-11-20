# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Work around rqt_robot_monitor taking the rqt node away from rqt's executor.

rqt_robot_monitor 1.0.x (Jazzy) calls ``rclpy.spin_once(node)`` from a 1 Hz QTimer in the GUI
thread. ``rclpy.spin_once`` adds the node to the global executor, which removes it from the
executor rqt's RclpySpinner thread is spinning, and never gives it back. From then on the node
is only spun by that timer, one callback per second, shared by every subscription, service and
service client of the node. Service replies then take several seconds (the breaker buttons
report that the power board did not answer) and the dashboard shows old data.

rqt already spins the node, so the stale-check slot is replaced by the same code without the
spin. If the installed rqt_robot_monitor no longer spins there, nothing is changed.
"""

import inspect

from rqt_robot_monitor.robot_monitor import RobotMonitorWidget


def _update_message_state_without_spin(self):
    """Update the display if it's stale (rqt_robot_monitor's slot, minus rclpy.spin_once)."""
    if self._timeline is None:
        return
    if self._timeline.has_messages:
        previous_stale_state = self._is_stale
        self._is_stale = self._timeline.is_stale

        time_diff = int(self._timeline.data_age)
        unit = 'second' if time_diff == 1 else 'seconds'
        self._timeline_pane._msg_label.setText(
            'Last message received %s %s ago' % (time_diff, unit))
        if previous_stale_state != self._is_stale:
            self._update_background_color()
    else:
        self._timeline_pane._msg_label.setText('No messages received')


def apply():
    """Patch RobotMonitorWidget if its stale check spins the node. Returns True if patched."""
    original = RobotMonitorWidget._update_message_state
    if original is _update_message_state_without_spin:
        return True
    try:
        source = inspect.getsource(original)
    except (OSError, TypeError):
        return False
    if 'spin_once' not in source:
        return False
    RobotMonitorWidget._update_message_state = _update_message_state_without_spin
    return True
