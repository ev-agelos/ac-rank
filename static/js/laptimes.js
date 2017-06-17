function _set_select_options(options){
    var pre_value = this.value;
    var option_html = "<option value=''>Select " + this.name + "</option>";
    for (var i = 0; i < options.length; i++) {
        option_html += "<option value='" + options[i] + "'>" + options[i] + "</option>";
    };
    $('#' + this.id).empty();
    $('#' + this.id).append(option_html);

    if (options.includes(pre_value)){
        this.value = pre_value;
    }else{
        this.selectedIndex = 0;
    };
};


function set_brand() {
    if (this.selectedIndex !== 0){
        var model_element = document.getElementById('id_model');
        _set_select_options.call(model_element, this.models_per_brand[this.value]);
        model_element.disabled = false;
    }else{
        $('#id_model')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_model').prop('disabled', true);
        $('#id_upgrade')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_upgrade').prop('disabled', true);
    };
};


function set_model() {
    var selected_brand = document.getElementById('id_brand').value;
    var selected_model = this.value;
    if (this.selectedIndex !== 0 && selected_brand+selected_model in this.upgrades_per_car){
        var upgrade_element = document.getElementById('id_upgrade');
        _set_select_options.call(upgrade_element, this.upgrades_per_car[selected_brand+selected_model]);
        upgrade_element.disabled = false;
    }else{
        $('#id_upgrade')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_upgrade').prop('disabled', true);
    };
};


function set_track() {
    if (this.selectedIndex !== 0 && this.value in this.layouts_per_track){
        var layout_element = document.getElementById('id_layout');
        _set_select_options.call(layout_element, this.layouts_per_track[this.value]);
        layout_element.disabled = false;
        $('#id_layout').prop('required', true);
    }else{
        $('#id_layout')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_layout').prop('disabled', true);  // Disable layout select
    };
};
