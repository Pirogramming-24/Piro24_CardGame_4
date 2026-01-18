/* base.html에 있는 주석 확인해주세요 */

/* static/js/script.js */

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. 요소 가져오기
    const pwInput = document.getElementById("id_password");
    const pwCheckInput = document.getElementById("id_password_check");
    const feedbackDiv = document.getElementById("password-feedback");
    const submitBtn = document.querySelector(".btn-submit");

    // [중요] 처음 시작할 때 버튼 비활성화 (못 누르게 막기)
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5"; // 흐릿하게 보여서 못 누르는 거 티내기
        submitBtn.style.cursor = "not-allowed"; // 마우스 올리면 금지 표시
    }

    // 2. 비밀번호 검사 함수
    function validatePassword() {
        const pw = pwInput.value;
        const pwCheck = pwCheckInput.value;

        // 1) 비밀번호 확인 칸이 비어있을 때
        if (pwCheck === "") {
            feedbackDiv.textContent = ""; // 메시지 숨김
            disableButton(); // 버튼 비활성화
            return;
        }

        // 2) 비밀번호가 일치할 때
        if (pw === pwCheck) {
            feedbackDiv.textContent = "비밀번호가 일치합니다. ✅";
            feedbackDiv.style.color = "#4CAF50"; 
            enableButton(); // 버튼 활성화!
        } 
        // 3) 비밀번호가 다를 때
        else {
            feedbackDiv.textContent = "비밀번호가 일치하지 않습니다. ❌";
            feedbackDiv.style.color = "#FF5252";
            disableButton(); // 버튼 비활성화
        }
    }

    // 버튼 활성화 함수
    function enableButton() {
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1"; // 원래 투명도로 복구
        submitBtn.style.cursor = "pointer"; // 손가락 모양
    }

    // 버튼 비활성화 함수
    function disableButton() {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5"; // 흐릿하게
        submitBtn.style.cursor = "not-allowed"; // 금지 모양
    }

    // 3. 입력할 때마다 검사 실행
    if (pwCheckInput) {
        pwCheckInput.addEventListener("input", validatePassword);
    }
    if (pwInput) {
        pwInput.addEventListener("input", validatePassword);
    }
});