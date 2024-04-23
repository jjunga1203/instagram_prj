const formTags = document.querySelectorAll('.likes-form')
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value

formTags.forEach((formTag) => {
    const likeUrl = formTag.action
    formTag.addEventListener('submit', (event) =>{
        event.preventDefault()

        axios({
            method: 'post',
            url : likeUrl,
            headers : {'X-CSRFToken': csrfToken},
            // mode: 'same-origin'
        }).then((resp) => {
            responseData = resp.data
            const isLiked = responseData.is_liked

            // console.log(likeCntTag)
        }).catch((error) => {
            console.log(error)
        })
    })
    
});
