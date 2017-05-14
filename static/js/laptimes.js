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


function set_models_from_brand() {
    if (this.selectedIndex !== 0){
        var model_select = document.getElementById('id_model');
        _set_select_options.call(model_select, this.models_per_brand[this.value]);
        model_select.disabled = false;
    }else{
        $('#id_model')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_model').prop('disabled', true);
    };
};


function set_layouts_from_track() {
    if (this.selectedIndex !== 0 && this.value in this.layouts_per_track){
        var layout_select = document.getElementById('id_layout');
        _set_select_options.call(layout_select, this.layouts_per_track[this.value]);
        layout_select.disabled = false;
        $('#id_layout').prop('required', true);
    }else{
        $('#id_layout')[0].selectedIndex = 0;  // Reset to 1st option
        $('#id_layout').prop('disabled', true);  // Disable layout select
    };
};
