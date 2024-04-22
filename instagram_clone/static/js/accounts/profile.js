// 모달 창 띄우기
const modal = document.getElementById("modal_add_feed");
const buttonAddFeed = document.getElementById("add_feed");
buttonAddFeed.addEventListener("click", e => {
    console.log('click');
    modal.style.display = "flex";
    document.body.style.overflowY = "hidden"; // 스크롤 없애기
});


// 모달 닫기 코드
const buttonCloseModal = document.getElementById("close_modal");
buttonCloseModal.addEventListener("click", e => {
    modal.style.display = "none";
    document.body.style.overflowY = "visible";
});

// <!-- jquery 부분 -->

    $('.modal_image_upload')
        .on("dragover", dragOver)
        .on("dragleave", dragOver)
        .on("drop", uploadFiles);

    function dragOver(e){
        e.stopPropagation();
        e.preventDefault();
        
        if (e.type == "dragover") {
            $(e.target).css({
                "background-color": "black",
                "outline-offset": "-20px"
            });
        } else {
            $(e.target).css({
                "background-color": "white",
                "outline-offset": "-10px"
            });
        }
    }

    function uploadFiles(e){
        e.stopPropagation();
        e.preventDefault();
        
        e.dataTransfer = e.originalEvent.dataTransfer; 
        var files =  e.dataTransfer.files;

        if (files.length > 1) {
            alert('하나만 올려라.');
            return;
        }

        if (files[0].type.match(/image.*/)) {
            $(e.target).css({
                "background-image": "url(" + window.URL.createObjectURL(files[0]) + ")",
                "outline": "none",
                "background-size": "100% 100%"});
        }else{
            alert('이미지가 아닙니다.');
            return;
        }

    }
