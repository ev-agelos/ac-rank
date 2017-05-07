function _set_select_options(options, first_option){
    var pre_value = this.value;
    var option_html = "<option value=''>" + first_option + "</option>";
    for (var i = 0; i < options.length; i++) {
        option_html += "<option value='" + options[i] + "'>" + options[i] + "</option>";
    };
    $('#' + this.id).empty();
    $('#' + this.id).append(option_html);
    this.value = pre_value;
};


function set_models_from_brand() {
    if (this.selectedIndex !== 0){
        var model_select = document.getElementById('id_model');
        var options = this.models_per_brand[this.value];
        _set_select_options.call(model_select, options, 'Select car brand');
        model_select.disabled = false;
    }else{
        $('#id_model')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_model').prop('disabled', true);
    };
};


function set_layouts_from_circuit() {
    if (this.selectedIndex !== 0 && this.value in this.layouts_per_circuit){
        var options = this.layouts_per_circuit[this.value];
        var layout_select = document.getElementById('id_layout');
        _set_select_options.call(layout_select, options, 'Select track layout');
        layout_select.disabled = false;
        $('#id_layout').prop('required', true);  // Disable layout select
    }else{
        $('#id_layout')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_layout').prop('disabled', true);  // Disable layout select
    };
};
