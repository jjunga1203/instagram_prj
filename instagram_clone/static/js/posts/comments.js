// 이 함수는 Django 템플릿에서 생성된 CSRF 토큰을 가져옵니다.
function getCSRFToken() {
    const csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfTokenInput) {
        return csrfTokenInput.value;
    } else {
        return null; // 토큰을 찾을 수 없는 경우 예외 처리
    }
}

document.querySelectorAll('.edit-comment-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        let commentId = this.getAttribute('data-comment-id');
        let commentContent = document.getElementById('comment-content-' + commentId).innerText;
        let newContent = prompt('댓글 수정', commentContent);

        // Send AJAX request to update comment
        if (newContent !== null) {
            fetch('/posts/edit_comment/' + commentId + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken() // Django 템플릿에서 가져온 CSRF 토큰
                },
                body: 'content=' + encodeURIComponent(newContent)
            })
            .then(function(response) {
                if (response.ok) {
                    // Update comment content on the page
                    document.getElementById('comment-content-' + commentId).innerText = newContent;
                } else {
                    alert('댓글 수정에 실패했습니다.');
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
                alert('댓글 수정에 실패했습니다.');
            });
        }
    });
});

// Add event listeners for delete comment buttons
document.querySelectorAll('.delete-comment-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        let postId = this.getAttribute('data-post-id');
        let commentId = this.getAttribute('data-comment-id');
        if (confirm('정말로 삭제하시겠습니까?')) {
            // Submit delete form via AJAX
            fetch('/posts/delete_comment/' + postId + '/' + commentId + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken() // Django 템플릿에서 가져온 CSRF 토큰
                },
                body: '' // 빈 문자열로 설정
            })
            .then(function(response) {
                if (response.ok) {
                    // Remove comment element from the page
                    document.getElementById('comment-' + commentId).remove();
                } else {
                    alert('댓글 삭제에 실패했습니다.');
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
                alert('댓글 삭제에 실패했습니다.');
            });
            
        }
    });
});
