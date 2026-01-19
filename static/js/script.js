/* base.html에 있는 주석 확인해주세요 */
/* static/js/script.js - 수정된 버전 */

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. 요소 가져오기
    const pwInput = document.getElementById("id_password");
    const pwCheckInput = document.getElementById("id_password_check");
    const feedbackDiv = document.getElementById("password-feedback");
    const submitBtn = document.querySelector(".btn-submit");

    // [핵심 수정] 
    // 비밀번호 입력창(pwInput)이 "있을 때만" 버튼을 비활성화합니다.
    // 게임 페이지에는 pwInput이 없으므로 이 코드가 무시되어 버튼이 살아납니다.
    if (submitBtn && pwInput) {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5"; 
        submitBtn.style.cursor = "not-allowed"; 
    }

    // 2. 비밀번호 검사 함수
    function validatePassword() {
        if (!pwInput || !pwCheckInput) return; // 입력창 없으면 중단

        const pw = pwInput.value;
        const pwCheck = pwCheckInput.value;

        // 1) 비밀번호 확인 칸이 비어있을 때
        if (pwCheck === "") {
            feedbackDiv.textContent = ""; 
            disableButton(); 
            return;
        }

        // 2) 비밀번호가 일치할 때
        if (pw === pwCheck) {
            feedbackDiv.textContent = "비밀번호가 일치합니다. ✅";
            feedbackDiv.style.color = "#4CAF50"; 
            enableButton(); 
        } 
        // 3) 비밀번호가 다를 때
        else {
            feedbackDiv.textContent = "비밀번호가 일치하지 않습니다. ❌";
            feedbackDiv.style.color = "#FF5252";
            disableButton(); 
        }
    }

    // 버튼 활성화 함수
    function enableButton() {
        if (!submitBtn) return;
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1"; 
        submitBtn.style.cursor = "pointer"; 
    }

    // 버튼 비활성화 함수
    function disableButton() {
        if (!submitBtn) return;
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5"; 
        submitBtn.style.cursor = "not-allowed"; 
    }

    // 3. 입력할 때마다 검사 실행
    if (pwCheckInput) {
        pwCheckInput.addEventListener("input", validatePassword);
    }
    if (pwInput) {
        pwInput.addEventListener("input", validatePassword);
    }
});