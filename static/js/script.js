/* static/js/script.js */

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. 요소 가져오기 (회원가입 폼에 있는 모든 인풋)
    const nameInput = document.getElementById("id_nickname"); // 이름(first_name)
    const idInput = document.getElementById("id_username");   // 아이디
    const pwInput = document.getElementById("id_password");   // 비번
    const pwCheckInput = document.getElementById("id_password_check"); // 비번 확인
    
    const feedbackDiv = document.getElementById("password-feedback");
    const submitBtn = document.querySelector(".btn-submit");

    // [중요 방어 코드] 
    // 이 스크립트는 base.html에 있어서 로그인 페이지에서도 실행됩니다.
    // 하지만 로그인 페이지에는 '비밀번호 확인(pwCheckInput)' 칸이 없죠.
    // 따라서, 회원가입 페이지가 아니면(요소가 없으면) 이 아래 코드를 실행하지 않고 멈춥니다.
    if (!pwCheckInput || !nameInput) {
        return; 
    }

    // 2. 초기 상태: 버튼 비활성화 (시작하자마자 잠금)
    if (submitBtn) {
        disableButton();
    }

    // 3. 통합 검사 함수 (이름, 아이디, 비번 모두 검사)
    function validateSignup() {
        // 값 가져오기 (공백 제거)
        const nameValue = nameInput.value.trim();
        const idValue = idInput.value.trim();
        const pwValue = pwInput.value.trim();
        const pwCheckValue = pwCheckInput.value.trim();

        let isPwMatch = false;

        // 1) 비밀번호 일치 여부 확인 로직
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
        // 조건: 이름 입력됨 AND 아이디 입력됨 AND 비밀번호 일치함(isPwMatch가 true면 비번도 입력된 것)
        if (nameValue.length > 0 && idValue.length > 0 && isPwMatch) {
            enableButton();
        } else {
            disableButton();
        }
    }

    // 버튼 활성화 함수
    function enableButton() {
        if(submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1"; // 진하게
            submitBtn.style.cursor = "pointer"; // 손가락 모양
            submitBtn.style.backgroundColor = "#935555"; // 원래 갈색
        }
    }

    // 버튼 비활성화 함수
    function disableButton() {
        if(submitBtn) {
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.5"; // 흐릿하게
            submitBtn.style.cursor = "not-allowed"; // 금지 모양
        }
    }

    // 4. 이벤트 리스너 연결 
    // 4개의 칸 중 하나라도 입력할 때마다 검사 함수 실행
    nameInput.addEventListener("input", validateSignup);
    idInput.addEventListener("input", validateSignup);
    pwInput.addEventListener("input", validateSignup);
    pwCheckInput.addEventListener("input", validateSignup);
});