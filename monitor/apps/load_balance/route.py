from monitor.apps.load_balance.controller.load_balance_controller import LoadBalanceManageController, \
    LoadBalanceItemManageController


def add_routes(api):
    api.add_route('/v1/monitor/load_balance', LoadBalanceManageController())
    api.add_route('/v1/monitor/load_balance/{rid}', LoadBalanceItemManageController())
