odoo.define('your_module.priority_five_stars', function (require) {
    "use strict";

    var FieldPriority = require('web.basic_fields').FieldPriority;

    FieldPriority.include({
        init: function () {
            this._super.apply(this, arguments);
            this.max_stars = 5;  // Set to 5 stars
        },
    });
});
