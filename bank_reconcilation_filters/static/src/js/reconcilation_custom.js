odoo.define('custom_reconcilation.StatementModel', function (require) {
"use strict";

var reconciliationModel = require('account.ReconciliationModel');

reconciliationModel.StatementModel.include({

   _performMoveLine: function (handle, mode) {
        var line = this.getLine(handle);
        var excluded_ids = _.map(line.reconciliation_proposition, function (prop) {
            return _.isNumber(prop.id) ? prop.id : null;
        }).filter(id => id != null);
        var filter = line['filter_'+mode] || "";
        var limit = this.limitMoveLines;
        var offset = line.offset;
        if (line.limit_override) {
            // If we have a limit_override, it means we are either adding/removing
            // a line from the matching table, hence keep same number of displayed
            // proposition below by setting offset to 0 and limit to the current
            // number of proposition loaded
            offset = 0;
            limit = line.limit_override;
        }console.log(line,'***************')
        return this._rpc({
                model: 'account.reconciliation.widget',
                method: 'get_move_lines_for_bank_statement_line',
                args: [line.id, line.st_line.partner_id, excluded_ids, filter, offset, limit, mode === 'match_rp' ? 'rp' : 'other',line.st_line.journal_id],
                context: this.context,
            })
            .then(this._formatMoveLine.bind(this, handle, mode));
    },
});
});
