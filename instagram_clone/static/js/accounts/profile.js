function change_pw(){
    const password1 = document.querySelector('#password1')
    const password2 = document.querySelector('#password2')
    const warning1 = document.querySelector('#warning1')
    const warning2 = document.querySelector('#warning2')
    let pw_flag = false

    // change 이벤트(input 포커스 아웃)에 비밀번호 검증 로직 추가
    password1.addEventListener('change', function (event) {
        const p1 = event.target.value
        console.log(p1.value)

        var regex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!$@%])[a-zA-Z\d!@#$%^&*()]{6,12}$/;

        if (regex.test(p1) ) {
            console.log('유효함')
            warning1.innerText = ''
        } else {

            console.log('유효하지 않음')
            warning1.innerText = '비밀번호는 영문자,숫자, 특수문자조합(!$@%) 를 포함해야 하며 6자 이상이어야 합니다.'
            password1.focus()

        }
    })

    // 비밀번호 확인시 2개의 비밀번호가 같은지 확인
    password2.addEventListener('change', function (event) {
        const p1 = password1.value
        const p2 = event.target.value

        if (p1 !== p2) {
        warning2.innerText = '비밀번호가 일치하지 않습니다.'
        password2.focus()
        } else {
        warning2.innerText = ''
        }
    })
}

// 모달 창 띄우기
const modal = document.getElementById("modal_add_feed");
const buttonAddFeed = document.getElementById("add_feed");
buttonAddFeed.addEventListener("click", e => {
    console.log('click');
    modal.style.display = "flex";
    document.body.style.overflowY = "hidden"; // 스크롤 없애기
});

// // 패스워드 변경 모달 창 띄우기
// const modal2 = document.getElementById("modal_add_feed_pw");
// const buttonChangePW = document.getElementById("add_feed_pw");
// buttonChangePW.addEventListener("click", e => {
//     console.log('click');
//     modal2.style.display = "flex";

//     change_pw();
//     document.body.style.overflowY = "hidden"; // 스크롤 없애기
// });

// // 패스워드 모달 닫기 코드
// const buttonCloseModal2 = document.getElementById("close_pw_modal");
// buttonCloseModal2.addEventListener("click", e => {
//     modal2.style.display = "none";
//     document.body.style.overflowY = "visible";
// });

// 모달 닫기 코드
const buttonCloseModal = document.getElementById("close_modal");
buttonCloseModal.addEventListener("click", e => {
    modal.style.display = "none";
    document.body.style.overflowY = "visible";
});


const formTags = document.querySelector('.delete_img')
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
const followUrl = formTags.action

const submitFormHandler = (event) => {
    event.preventDefault()
    // console.log(csrfToken)

    axios({
        method: 'post',
        url: followUrl,
        headers: {'X-CSRFToken': csrfToken}
    }).then((resp) => {
        const imgElement = document.querySelector('img')

        const responseData = resp.data
        const profile_url = responseData.profile_url

        imgElement.setAttribute('src', profile_url)

        console.log(resp)
    }).catch((error) => {
        console.log(error)
    })
}





// formElement.addEventListener('submit', submitFormHandler)

