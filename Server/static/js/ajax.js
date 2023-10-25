// AJAX(Asynchronous Javascript and XML)
// Web page의 일부분만 변경하는 방법
function changeWeather() {
    let addr = $('#profileAddr').text();
    $.ajax({
        type: 'GET',
        url: '/weather',
        data: {addr: addr},
        success: function(result) {
            $('#weather').html(result);
        }
    });
}
/*  영수증 업로드 */
function processReceipt() {
    const input = document.getElementById('receiptInput');
    const resultDiv = document.getElementById('result');
  
    const file = input.files[0];
  
    if (!file) {
      alert('Please select a file.');
      return;
    }
  
    const reader = new FileReader();
  
    reader.onload = function (e) {
      const image = new Image();
      image.src = e.target.result;
  
      image.onload = function () {
        Tesseract.recognize(              /* 영수증 OCR 구현시 : Tesseract 모듈이용 */
          image,
          'kor', // Language code for Korean
          {
            logger: (info) => {
              if (info.status === 'recognizing text') {
                console.log(`Progress: ${info.progress * 100}%`);
              }
            }
          }
        ).then(({ data: { text } }) => {
          resultDiv.innerText = text;
          text_list = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣\\n]', '', text).split('\n')
          text_list
        });
      }
    }

    reader.readAsDataURL(file);
  }

  /* 영수증 결과 보내기 */
  function sendOCRResults(text) {
    // Define the URL where you want to send the data
    const url = 'https://example.com/endpoint'; // Replace with your actual endpoint
  
    // Prepare the data to be sent
    const data = {
      text: text
    };
  
    // Send a POST request with the data
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Data sent successfully:', data);
    })
    .catch(error => {
      console.error('Error sending data:', error);
    });
  }


function getProfile() {
    $('#profileModal').modal('show');
    $.ajax({
        type: 'GET',
        url: '/changeProfile',
        data: ' ',
        success: function(result) {
            let profile = JSON.parse(result);
            $('#hiddenEmail').val(profile[0]);
            $('#modalEmail').val(profile[0]);
            $('#hiddenImage').val(profile[1]);
            $('#modalStateMsg').val(profile[2]);
            $('#modalGithub').val(profile[3]);
            $('#modalInsta').val(profile[4]);
            $('#modalAddr').val(profile[5]);
        } 
    })
}

function changeProfile() {
    $('#profileModal').modal('hide');
    let email = $('#hiddenEmail').val();
    let imageInputVal = $('#modalImage')[0];
    let stateMsg = $('#modalStateMsg').val();
    let github = $('#modalGithub').val();
    let insta = $('#modalInsta').val();
    let addr = $('#modalAddr').val();
    let hiddenImage = $('#hiddenImage').val();
    let formData = new FormData();
    formData.append('email', email);
    formData.append('image', imageInputVal.files[0]);
    formData.append('stateMsg', stateMsg);
    formData.append('github', github);
    formData.append('insta', insta);
    formData.append('addr', addr);
    formData.append('hiddenImage', hiddenImage);
    $.ajax({
        type: 'POST',
        url: '/changeProfile',
        data: formData,
        processData: false,
        contentType: false,
        success: function(result) {     
            let profile = JSON.parse(result);
            let filename = '/static/profile/' + profile[6] + '.png';
            if (profile[7] != 0)    // profile image가 변화하면 mtime 값이 바뀜
                filename += '?q=' + profile[7];
            $('#profileImage').attr({'src': filename});
            $('#profileStateMsg').text(profile[2]);
            $('#profileGithub').text(profile[3]);
            $('#profileInsta').text(profile[4]);
            $('#profileAddr').text(profile[5]);
            let needRefresh = profile[8];
            if (needRefresh == 1)   // github, insta, addr이 새로이 생성되면 needRefresh가 1이 됨
                window.location.reload();
        }
    });
}