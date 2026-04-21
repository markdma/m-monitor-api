# coding: utf-8
from __future__ import absolute_import

from monitor.apps.alert.alert_controller import EventCaseController, ShieldListController, AlarmScheController, \
    AlarmScheItemController, AlarmListController, AlarmNoteController, AlarmHistoryListController, \
    AlarmTemplateController, AlarmTemplateCloneController, AlarmStrategyController, AlarmGroupController, \
    AlarmTemplateItemController, AlarmStrategyItemController, AlarmGroupItemController, \
    AlarmTplActionController, AlarmAssetItemController, TplController, TplItemController, \
    ProjectListController, CustomController, CustomActionController, CustomItemController, StrategySearchController, \
    AssetTPLController, AlarmCountController, CounterController


def add_routes(api):
    api.add_route('/v1/monitor/alert_event', EventCaseController())

    api.add_route('/v1/monitor/shield_list', ShieldListController())

    api.add_route('/v1/monitor/alarm_plans', AlarmScheController())
    api.add_route('/v1/monitor/alarm_plans/{rid}', AlarmScheItemController())

    api.add_route('/v1/monitor/alarmlist', AlarmListController())
    api.add_route('/v1/monitor/alarm_historylist', AlarmHistoryListController())
    api.add_route('/v1/monitor/alarmnote', AlarmNoteController())
    api.add_route('/v1/monitor/alarm_count', AlarmCountController())

    # 自定义模板
    api.add_route('/v1/monitor/host_tpl', TplController())
    api.add_route('/v1/monitor/host_tpl/{rid}', TplItemController())

    # 模板
    api.add_route('/api/monitor/alarm_template', AlarmTemplateController())
    api.add_route('/api/monitor/asset_relation', AssetTPLController())  # 资源绑定模板
    api.add_route('/api/monitor/alarm_template/{rid}', AlarmTemplateItemController())

    # 模板克隆
    api.add_route('/api/monitor/alarm_template/clone', AlarmTemplateCloneController())

    # 策略
    api.add_route('/api/monitor/strategy/search', StrategySearchController())
    api.add_route('/api/monitor/alarm_strategy', AlarmStrategyController())
    api.add_route('/api/monitor/alarm_strategy/{rid}', AlarmStrategyItemController())
    api.add_route('/api/monitor/alarm_counter', CounterController())

    # 模板Action
    api.add_route('/api/monitor/alarm/action', AlarmTplActionController())

    # TODO 主机组
    api.add_route('/api/monitor/alarm_group', AlarmGroupController())
    api.add_route('/api/monitor/alarm_group/{rid}', AlarmGroupItemController())

    # 资源 模板绑定、删除资源
    api.add_route('/api/monitor/alarm_asset', AlarmAssetItemController())

    # TODO 项目拉取
    api.add_route('/v1/monitor/projects', ProjectListController())

    # 自定义上报
    api.add_route('/api/monitor/customs', CustomController())
    api.add_route('/api/monitor/customs/{rid}', CustomItemController())

    # 自定义上报告警编辑
    api.add_route('/api/monitor/custom/alarm/{rid}', CustomActionController())
