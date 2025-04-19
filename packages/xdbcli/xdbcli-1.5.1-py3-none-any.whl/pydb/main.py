import sys
import argparse
from .dbms.constants import DBMS
from .dbms.object_factory import database_factory
from .client import CmdClient
from .reader import Reader
from .exporter import Exporter
from .exporter import SqlScriptExporter


def check_argv(value: str) -> bool:
    return any([True if value in x else False for x in sys.argv])


def main():
    epilog = """example:
    %(prog)s -c 'mysql://user:password@hostname:port/database'
    %(prog)s -c 'mssql://user:password@hostname:port/database -A NTLM -d 'com.microsoft.sqlserver.jdbc.SQLServerDriver' -j /home/user/mssql-jdbc-12.2.0.jre8.jar'
    %(prog)s -c 'oracle://user:password@hostname:port/service_name -m false -l /home/user/instantclient_21_13'
    %(prog)s -c 'postgresql://user:password@hostname:port/database'
    """
    arg_parser = argparse.ArgumentParser(description="pyDB Universal Database client",
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         epilog=epilog,
                                         usage='use "%(prog)s --help" for more information')

    required_group = arg_parser.add_argument_group(title="required arguments")
    required_group.add_argument("-c", dest="connection", required=True, type=str,
                            help=f"%(prog)s -c 'postgresql://user:password@hostname:port/database'")


    non_required_group = arg_parser.add_argument_group(title="non Required arguments")
    non_required_group.add_argument("-a", dest="autocommit", required=False, type=bool, default=True,
                            help='enable cursor autocommit, default=%(default)s' )

    non_interactive_group = arg_parser.add_argument_group(title="non Interactive mode")
    non_interactive_group.add_argument("-i", dest="input", required=False, type=str,
                            help='path to input SQL file' )
    non_interactive_group.add_argument("-o", dest="output", required=check_argv("-i"), type=str,
                            help='path to output CSV file, required -i argument' )

    for arg in sys.argv:
        if DBMS.MSSQL in arg:
            required_group.add_argument('-A', dest="authenticationScheme", required=check_argv(DBMS.MSSQL),
                                        type=str.upper, choices=['NTLM'],
                                        help='Available %(choices)s, '
                                             'read more - https://learn.microsoft.com/ru-ru/sql/connect/jdbc/using-ntlm-authentication-to-connect-to-sql-server?view=sql-server-ver16')
            required_group.add_argument('-d', dest="driverClass", required=check_argv(DBMS.MSSQL), type=str,
                                    help='full class name of jdbc driver, '
                                         'read more - https://github.com/baztian/jaydebeapi')
            required_group.add_argument('-j', dest="driverJarFile", required=check_argv(DBMS.MSSQL), type=str,
                                    help='path to JAR file, '
                                         'read more - https://github.com/baztian/jaydebeapi')
            break

        if DBMS.ORACLE in arg:
            required_group.add_argument('-m', dest="thin_mode", required=False, action="store_false",
                                    help='oracledb Thin mode default=%(default)s, set False to switch into Thick mode, '
                                         'read more - https://python-oracledb.readthedocs.io/en/latest/user_guide/initialization.html')
            required_group.add_argument('-l', dest="lib_dir", required=check_argv("-m"), type=str,
                                    help='path to oracle instantclient, '
                                         'read more - https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#id3')
            break

    cli_args = arg_parser.parse_args()
    db = database_factory.get(**vars(cli_args))

    interactive_mode = True if not ('-i' in sys.argv and '-o' in sys.argv) else False
    if interactive_mode:
        print('Interactive mode')
        client = CmdClient(db=db)
        try:
            client.cmdloop()
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
        finally:
            client.close()
    else:
        print('Non Interactive mode')
        reader = Reader(cli_args.input)
        exporter = Exporter(cli_args.output)
        script_exporter = SqlScriptExporter(db, reader, exporter)
        script_exporter.export()


if __name__ == '__main__':
    main()
