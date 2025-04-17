# Copyright 2016 Intel Corporation

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg

from ironic.common.i18n import _
from ironic.conf import auth


VALID_ADD_PORTS_VALUES = {
    'all': _('all MAC addresses'),
    'active': _('MAC addresses of NICs with IP addresses'),
    'pxe': _('only the MAC address of the PXE NIC'),
    'disabled': _('do not create any ports'),
}
VALID_KEEP_PORTS_VALUES = {
    'all': _('keep all ports, even ones with MAC addresses that are not '
             'present in the inventory'),
    'present': _('keep only ports with MAC addresses present in '
                 'the inventory'),
    'added': _('keep only ports determined by the add_ports option'),
}

opts = [
    cfg.IntOpt('status_check_period', default=60,
               help=_('period (in seconds) to check status of nodes '
                      'on inspection')),
    cfg.StrOpt('extra_kernel_params', default='',
               help=_('extra kernel parameters to pass to the inspection '
                      'ramdisk when boot is managed by ironic (not '
                      'ironic-inspector). Pairs key=value separated by '
                      'spaces.')),
    cfg.BoolOpt('power_off', default=True,
                help=_('whether to power off a node after inspection '
                       'finishes. Ignored for nodes that have fast '
                       'track mode enabled.')),
    cfg.StrOpt('callback_endpoint_override',
               help=_('endpoint to use as a callback for posting back '
                      'introspection data when boot is managed by ironic. '
                      'Standard keystoneauth options are used by default.')),
    cfg.BoolOpt('require_managed_boot', default=None,
                help=_('require that the in-band inspection boot is fully '
                       'managed by the node\'s boot interface. Set this to '
                       'True if your installation does not have a separate '
                       '(i)PXE boot environment for node discovery. Set '
                       'to False if you need to inspect nodes that are not '
                       'supported by boot interfaces (e.g. because they '
                       'don\'t have ports).')),
    cfg.StrOpt('add_ports',
               default='pxe',
               help=_('Which MAC addresses to add as ports during '
                      'inspection.'),
               choices=list(VALID_ADD_PORTS_VALUES.items())),
    cfg.StrOpt('keep_ports',
               default='all',
               help=_('Which ports (already present on a node) to keep after '
                      'inspection.'),
               choices=list(VALID_KEEP_PORTS_VALUES.items())),
    cfg.BoolOpt('update_pxe_enabled',
                default=True,
                help=_('Whether to update the ports\' pxe_enabled field '
                       'according to the inspection data.')),
    cfg.StrOpt('default_hooks',
               default='ramdisk-error,validate-interfaces,ports,architecture',
               help=_('A comma-separated lists of inspection hooks that are '
                      'run by default. In most cases, the operators will not '
                      'modify this. The default (somewhat conservative) hooks '
                      'will raise an exception in case the ramdisk reports an '
                      'error, validate interfaces in the inventory, and create'
                      ' ports.')),
    cfg.StrOpt('hooks',
               default='$default_hooks',
               help=_('Comma-separated list of enabled hooks for processing '
                      'pipeline. The default for this is $default_hooks. '
                      'Hooks can be added before or after the defaults '
                      'like this: "prehook,$default_hooks,posthook".')),
]


def register_opts(conf):
    conf.register_opts(opts, group='inspector')
    auth.register_auth_opts(conf, 'inspector',
                            service_type='baremetal-introspection')


def list_opts():
    return auth.add_auth_opts(opts, service_type='baremetal-introspection')
