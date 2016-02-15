#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import print_function

import argparse
import sys

from prettytable import PrettyTable

from virtualbmc import exception
from virtualbmc import VirtualBMCManager


def main():
    parser = argparse.ArgumentParser(
        prog='Virtual BMC',
        description='A virtual BMC for controlling virtual instances',
    )
    subparsers = parser.add_subparsers()

    # create the parser for the "add" command
    parser_add = subparsers.add_parser('add', help='Add a new virtual BMC')
    parser_add.set_defaults(command='add')
    parser_add.add_argument('domain_name',
                            help='The name of the virtual machine')
    parser_add.add_argument('--username',
                            dest='username',
                            default='admin',
                            help='The BMC username; defaults to "admin"')
    parser_add.add_argument('--password',
                            dest='password',
                            default='password',
                            help='The BMC password; defaults to "password"')
    parser_add.add_argument('--port',
                            dest='port',
                            type=int,
                            default=623,
                            help='Port to listen on; defaults to 623')
    parser_add.add_argument('--address',
                            dest='address',
                            default='::',
                            help='Address to bind to; defaults to ::')
    parser_add.add_argument('--libvirt-uri',
                            dest='libvirt_uri',
                            default="qemu:///system",
                            help=('The libvirt URI; defaults to '
                                  '"qemu:///system"'))

    # create the parser for the "delete" command
    parser_delete = subparsers.add_parser('delete',
                                          help='Delete a virtual BMC')
    parser_delete.set_defaults(command='delete')
    parser_delete.add_argument('domain_name',
                               help='The name of the virtual machine')

    # create the parser for the "start" command
    parser_start = subparsers.add_parser('start', help='Start a virtual BMC')
    parser_start.set_defaults(command='start')
    parser_start.add_argument('domain_name',
                              help='The name of the virtual machine')

    # create the parser for the "stop" command
    parser_stop = subparsers.add_parser('stop', help='Stop a virtual BMC')
    parser_stop.set_defaults(command='stop')
    parser_stop.add_argument('domain_name',
                             help='The name of the virtual machine')

    # create the parser for the "list" command
    parser_stop = subparsers.add_parser('list', help='list all virtual BMCs')
    parser_stop.set_defaults(command='list')

    # create the parser for the "show" command
    parser_stop = subparsers.add_parser('show', help='Show a virtual BMCs')
    parser_stop.set_defaults(command='show')
    parser_stop.add_argument('domain_name',
                             help='The name of the virtual machine')

    args = parser.parse_args()
    manager = VirtualBMCManager()

    try:
        if args.command == 'add':
            manager.add(username=args.username, password=args.password,
                        port=args.port, address=args.address,
                        domain_name=args.domain_name,
                        libvirt_uri=args.libvirt_uri)

        elif args.command == 'delete':
            manager.delete(args.domain_name)

        elif args.command == 'start':
            manager.start(args.domain_name)

        elif args.command == 'stop':
            manager.stop(args.domain_name)

        elif args.command == 'list':
            ptable = PrettyTable(['Domain name', 'Status', 'Address', 'Port'])
            for bmc in manager.list():
                ptable.add_row([bmc['domain_name'], bmc['status'],
                                bmc['address'], bmc['port']])
            print(ptable)

        elif args.command == 'show':
            bmc = manager.show(args.domain_name)
            for key, val in bmc.items():
                ptable.add_row([key, val])
            print(ptable)

    except (exception.LibvirtConnectionOpenError,
            exception.DomainNotFound) as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()