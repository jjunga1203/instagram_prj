
// 프로필 편집 클릭했을때
document.querySelector('#save_change').addEventListener('click', function() {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const gender = document.querySelector('#gender').value
    const introduce = document.querySelector('#intro').value

    // event.preventDefault()
    console.log(csrfToken)
    console.log(document.querySelector('#gender').value)
    console.log(document.querySelector('#intro').value)
    console.log('/accounts/profile/{{user.id}}')

    
    axios.post('/accounts/profile/{{user.id}}', {
        'gender': gender,
        'introduce': introduce,
    }, {
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
    })
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.error(error);
    });
});



// formElement.addEventListener('submit', submitFormHandler)

