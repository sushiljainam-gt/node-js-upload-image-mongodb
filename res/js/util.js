function getStats() {
    $.ajax({
        url: 'stats',
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        type: 'get',
        success: (response) => {
            console.log(response);
            $('#stats').html('');
            $.each(response, function (key, data) {							
                if (key === 'persons') {
                    $('#stats').append('Registered persons (' + response[key].length + '):<br/>');
                    response[key].forEach(({ name, imageCount }) => {
                        $('#stats').append(name + ' has ' + imageCount + ' images.<br/>');
                    });
                } else {
                    if (key !== 'message') {
                        $('#stats').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#stats').append(data + '<br/>');
                    }
                }
            })
        },
        error: console.error,
    });
}