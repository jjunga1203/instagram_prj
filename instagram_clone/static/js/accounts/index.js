
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

