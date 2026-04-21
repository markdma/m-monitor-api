# coding: utf-8


class Encryption(object):

    DB_USER_PASSWORD = 'DBUserPassword@!'


class EndpointType(object):

    HOST = "host"
    NETWORK = "network"

    ALL_TYPE = [HOST, NETWORK]


class DatabaseServerModel(object):

    UPDATE = "update"
    INSERT = "insert"
    DELETE = "delete"
    AUTO = "auto"
    AUTO_AND_DELETE = "auto_and_delete"
    BATCH_UPDATE = "batch_update"
    BATCH_DELETE = "batch_delete"

    ALL_MODEL = [UPDATE, INSERT, AUTO, AUTO_AND_DELETE, BATCH_UPDATE, BATCH_DELETE, DELETE]


class QueueCmd(object):

    SEND_SMS = "SEND_SMS"

    ALL_CMD_LIST = [
        SEND_SMS
    ]


class NetlineCapacityType(object):

    DayTable = '1'
    WeekTable = '2'

    ALL_TYPE = [DayTable, WeekTable]


class NetlineCapacityFilterStrategyType(object):

    NetInOctetTop20 = '1'
    NetOutOctetTop20 = '2'
    NetInOctetLess20 = '3'
    NetOutOctetLess20 = '4'

    ALL_TYPE = [NetInOctetTop20, NetOutOctetTop20, NetInOctetLess20, NetOutOctetLess20]


class HostCapacityType(object):

    DayTable = '1'
    WeekTable = '2'
    MonthTable = '3'
    LastDaysTable = '4'

    ALL_TYPE = [DayTable, WeekTable, MonthTable, LastDaysTable]


class DatabaseCapacityType(object):

    DayTable = '1'
    WeekTable = '2'
    MonthTable = '3'

    ALL_TYPE = [DayTable, WeekTable, MonthTable]


class DiskCapacityType(object):

    DayTable = 'daily'
    WeekTable = 'weekly'
    MonthTable = 'monthly'

    ALL_TYPE = [DayTable, WeekTable, MonthTable]


class CephCapacityType(object):

    DayTable = 'daily'
    WeekTable = 'weekly'
    MonthTable = 'monthly'

    ALL_TYPE = [DayTable, WeekTable, MonthTable]


class CapacityTreeType(object):

    AzTreeType = '1'
    ProjectTreeType = '2'

    ALL_TYPE = [AzTreeType, ProjectTreeType]


class CapacityFilterStrategy(object):

    MetricExpressionsMaxCount = 4
    OnceSelectMaxCount = 100


class CollectType(object):

    Log = 'LOG'
    Port = 'PORT'
    Proc = 'PROC'

    ALL_TYPE = [Log, Port, Proc]
