odoo.define('system_gestion_notariale.ComboBox', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldSelection = require('web.basic_fields').FieldSelection;

    var ComboBox = FieldSelection.extend({
        events: _.extend({}, FieldSelection.prototype.events, {
            'keydown input': '_onKeyDown',
        }),

        _onKeyDown: function (event) {
            if (event.key === 'Enter') {
                var value = this.$input.val();
                if (value) {
                    this.$input.append(new Option(value, value));
                    this._setValue(value);
                }
            }
        },
    });

    fieldRegistry.add('combo', ComboBox);
});
