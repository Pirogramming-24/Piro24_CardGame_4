/* static/js/script.js - 최종 정리본 */

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. 요소 가져오기
    const nameInput = document.getElementById("id_nickname"); // 이름
    const idInput = document.getElementById("id_username");   // 아이디
    const pwInput = document.getElementById("id_password");   // 비번
    const pwCheckInput = document.getElementById("id_password_check"); // 비번 확인
    
    const feedbackDiv = document.getElementById("password-feedback");
    const submitBtn = document.querySelector(".btn-submit");

    // [중요 방어 코드]
    // 회원가입 페이지가 아니면(필수 입력창이 없으면) 스크립트 실행 중단
    // (로그인 페이지 등에서 에러 발생하는 것 방지)
    if (!nameInput || !idInput || !pwInput || !pwCheckInput || !submitBtn) {
        return; 
    }

    // 2. 초기 상태: 버튼 비활성화 (페이지 로드 시 무조건 잠금)
    disableButton();

    // 3. 통합 검사 함수 (이름, 아이디, 비번 모두 검사)
    function validateSignup() {
        // 값 가져오기 (양옆 공백 제거)
        const nameValue = nameInput.value.trim();
        const idValue = idInput.value.trim();
        const pwValue = pwInput.value.trim();
        const pwCheckValue = pwCheckInput.value.trim();

        let isPwMatch = false;

        // 1) 비밀번호 일치 여부 확인
        if (pwCheckValue === "") {
            feedbackDiv.textContent = ""; // 비어있으면 메시지 숨김
            isPwMatch = false;
        } else if (pwValue === pwCheckValue) {
            feedbackDiv.textContent = "비밀번호가 일치합니다. ✅";
            feedbackDiv.style.color = "#4CAF50"; // 초록색
            isPwMatch = true;
        } else {
            feedbackDiv.textContent = "비밀번호가 일치하지 않습니다. ❌";
            feedbackDiv.style.color = "#FF5252"; // 빨간색
            isPwMatch = false;
        }

        // 2) 최종 버튼 활성화 조건
        // 이름 입력됨 AND 아이디 입력됨 AND 비밀번호 일치함
        if (nameValue.length > 0 && idValue.length > 0 && isPwMatch) {
            enableButton();
        } else {
            disableButton();
        }
    }

    // [헬퍼 함수] 버튼 활성화
    function enableButton() {
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1"; 
        submitBtn.style.cursor = "pointer"; 
        submitBtn.style.backgroundColor = "#935555"; // 원래 버튼 색상
    }

    // [헬퍼 함수] 버튼 비활성화
    function disableButton() {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5"; 
        submitBtn.style.cursor = "not-allowed"; 
    }

    // 4. 이벤트 리스너 연결 
    // 입력창 4개 중 하나라도 입력할 때마다 검사 함수 실행
    nameInput.addEventListener("input", validateSignup);
    idInput.addEventListener("input", validateSignup);
    pwInput.addEventListener("input", validateSignup);
    pwCheckInput.addEventListener("input", validateSignup);
});