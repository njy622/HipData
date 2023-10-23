/**
 * calendar.js
 * 		calendar.html 에서 사용하였던 자바스크립트 코드
 */

var schedClicked = false;		// 동작을 구분만 해주기 위하여 설정
var annivClicked = false;		// anniv, sched가 있는 날짜에 칸만 클릭하기 위하여 설정
 
function cellClick(date) {
	if (schedClicked)			// sched가 있는 곳에 클릭되면 false로 바꾸고 그냥 빠져 나옴.
		schedClicked = false;	// schedClick(sid)와 같이 눌리면 우선권을 schedClick에 주기 위하여
	else if (annivClicked)
		annivClicked = false;
	else {
		date = date + '';		// number type을 문자열로 변환
		const dateForm = date.substring(0,4)+'-'+date.substring(4,6)+'-'+date.substring(6,8);
		let t = new Date();				// 현재 시간과 비슷한 시간과 분을 찾아감.
		let hour = t.getHours();		// js Date() 시간 가져옴.
		let minute = t.getMinutes();
		if (minute < 30)
			minute = 30;
		else {
			minute = 0; hour = (hour + 1) % 24;
		}
		const startStr = ((hour >= 10) ? ''+hour : '0'+hour) + ':' + ((minute == 0) ? '00' : '30');
		const endStr = ((hour >= 9) ? ''+(hour+1) : '0'+(hour+1)) + ':' + ((minute == 0) ? '00' : '30'); // 종료시간은 시작시간 + 1
		$('#startDate').val(dateForm);
		$('#startTime').val(startStr);
		$('#endDate').val(dateForm);
		$('#endTime').val(endStr);
		$('#addModal').modal('show');
	}
}

function schedClick(sid) {
	schedClicked = true;
	$.ajax({
		type: 'GET',
		url: '/schedule/detail/' + sid,
		success: function(jsonSched) {
			let sched = JSON.parse(jsonSched);
			$('#sid2').val(sched.sid);
			$('#title2').val(sched.title);
			if (sched.isImportant == 1)
				$('#importance2').prop('checked', true);
			$('#startDate2').val(sched.startTime.substring(0,10));
			$('#startTime2').val(sched.startTime.substring(11,16));
			$('#endDate2').val(sched.endTime.substring(0,10));
			$('#endTime2').val(sched.endTime.substring(11,16));
			$('#place2').val(sched.place);
			$('#memo2').val(sched.memo);
			$('#updateModal').modal('show');
		}
	});
}

function deleteSchedule() {
	let sid = $('#sid2').val();
	const answer = confirm('정말로 삭제하시겠습니까?');
	if (answer) {
		location.href = '/schedule/delete/' + sid;
	}
}

function addAnniversary() {
	$('#addAnnivModal').modal('show');
}

function annivClick(aid) {
	annivClicked = true;
	$.ajax({
		type: 'GET',
		url: '/schedule/detailAnniv/' + aid,
		success: function(jsonAnniv) {
			let anniv = JSON.parse(jsonAnniv);
			$('#aid').val(anniv.aid);
			$('#uid').val(anniv.uid);
			$('#aname2').val(anniv.aname);
			if (anniv.isHoliday == 1)
				$('#holiday2').prop('checked', true);		// id=holiday2 checkbox에 checked를 true로 추가
			let day = anniv.adate;
			$('#annivDate2').val(day.substring(0,4) + '-' + day.substring(4,6) + '-' + day.substring(6));	// 6부터 마지막까지
			$('#updateAnnivModal').modal('show');
		}
	});
}

function deleteAnniv() {
	let aid = $('#aid').val();
	let uid = $('#uid').val();
	const answer = confirm('정말로 삭제하시겠습니까?');
	if (answer) {
		location.href = `/schedule/deleteAnniv/${aid}/${uid}`;
	}
}