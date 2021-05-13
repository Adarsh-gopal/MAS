odoo.define('maintenance_integ_acc.kanban', function (require) {
"use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');

    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');

    var viewRegistry = require('web.view_registry');

    function renderGenerateEquipmentButton() {
        if (this.$buttons) {
            var self = this;
            var lead_type = self.initialState.getContext()['default_type'];
            this.$buttons.on('click', '.o_button_generate_equipements', function () {
                self.do_action({
                    name: 'Generate Equipments',
                    type: 'ir.actions.act_window',
                    res_model: 'generate.asset.equipment',
                    target: 'new',
                    views: [[false, 'form']],
                    // context: {'is_modal': true, 'default_lead_type': lead_type},
                });
            });
        }
    }

    var maintainanceIntegListController = ListController.extend({
        willStart: function() {
            var self = this;
            var ready = this.getSession().user_has_group('base.group_user')
                .then(function (is_sale_manager) {
                    if (is_sale_manager) {
                        self.buttons_template = 'MaintainanceIntegListView.buttons';
                    }
                });
            return Promise.all([this._super.apply(this, arguments), ready]);
        },
        renderButtons: function () {
            this._super.apply(this, arguments);
            renderGenerateEquipmentButton.apply(this, arguments);
        }
    });

    var maintainanceIntegListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: maintainanceIntegListController,
        }),
    });

    var maintainanceIntegKanbanController = KanbanController.extend({
        willStart: function() {
            var self = this;
            var ready = this.getSession().user_has_group('base.group_user')
                .then(function (is_sale_manager) {
                    if (is_sale_manager) {
                        self.buttons_template = 'MaintainanceIntegKanbanView.buttons';
                    }
                });
            return Promise.all([this._super.apply(this, arguments), ready]);
        },
        renderButtons: function () {
            this._super.apply(this, arguments);
            renderGenerateEquipmentButton.apply(this, arguments);
        }
    });

    var maintainanceIntegKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: maintainanceIntegKanbanController,
        }),
    });

    viewRegistry.add('maintenance_integ_with_asset_tree', maintainanceIntegListView);
    viewRegistry.add('maintenance_integ_with_asset_kanban', maintainanceIntegKanbanView);
});
