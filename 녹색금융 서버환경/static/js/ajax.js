// AJAX(Asynchronous Javascript and XML)
// Web page의 일부분만 변경하는 방법
function changeQuote() {
    $.ajax({
        type: 'GET',
        url: '/change_quote', 
        data: ' ',              // 서버로 전달할 데이터
        success: function(msg) {        // msg: 서버로부터 받은 데이터
            $('#quoteMsg').html(msg);   // html id로 보냄, .html(msg) < msg를 바꿈.
        }
    });
}
function changeAddr() {
    $('#addrInput').attr('class', 'mt-2');      // input box가 보이게, d-none을 제거
}
function addrSubmit() {
    $('#addrInput').attr('class', 'mt-2 d-none');   // input box가 안보이게, d-none을 보내줌. addAttribute 비슷
    let addr = $('#addrInputTag').val();    // input tag면 .val()로 읽어 줌. value 가져옴.
    $.ajax({
        type: 'GET',
        url: '/change_addr',
        data: {addr: addr},         // /change_addr?addr=서울시 강남구 {key, value}
        success: function(msg) {    // 성공이면 base.html의 #addr 바꿔줌.
            $('#addr').html(msg);
        }
    });
}
function changeWeather() {
    let addr = $('#addr').text();       // 1) 누르면 data 가져옴.
    $.ajax({                            // 2) ajax로 넘겨서
        type: 'GET',                    // 3) get 방식으로 주소창에서
        url: '/weather',                // 4) /weather?addr=서울시 영등포구
        data: {addr: addr},             // 5) addr에 서울시 영등포구 넣어줘서
        success: function(result) {     // 6) 성공하면 app.py에서 받은 값
            $('#weather').html(result); // 7) 해당 아이디에 result를 넘긴다.
        }
    });
}

function changeProfile() {
    $('#imageInput').attr('class', 'mt-2');
}
function imageSubmit() {
    let imageInputVal = $('#image')[0];
    let formData = new FormData();
    formData.append('image', imageInputVal.files[0]);
    $.ajax({
        type: 'POST',
        url: '/change_profile',
        data: formData,
        processData: false,
        contentType: false,
        success: function(result) {
            $('#imageInput').attr('class', 'mt-2 d-none');
            let fname = 'http://127.0.0.1:5000/static/data/profile.png?q=' + result;
            $('#profile').attr('src', fname);
        }
    });
}
function submit_gu_status() {
    console.log($('#column :selected').val());
    console.log($('#colormap :selected').val());
    let column = $('#column :selected').val();
    let colormap = $('#colormap :selected').val();
    $.ajax({
        type: 'POST',
        url: '/map/cctv_pop',
        data: {column:column, colormap:colormap},
        dataType: 'html',
        success: function(result) {
            $('#gu_status').html(result);
        }
    });
}
function submit_station() {
    let station1 = $('#station1').val();
    let station2 = $('#station2').val();
    let station3 = $('#station3').val();
    let station4 = $('#station4').val();
    let station5 = $('#station5').val();
    $.ajax({
        type: 'POST',
        url: '/map/station',
        data: {station1: station1, station2: station2, station3: station3, station4: station4, station5: station5},
        dataType: 'html',
        success: function(result) {
            $('#station_status').html(result);
        }
    });
}