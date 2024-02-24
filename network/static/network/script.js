function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
  }
  function submithandler(id){
    const content_text = document.getElementById(`textarea_${id}`).value;
    const content = document.getElementById(`content_${id}`);
    fetch(`/edit/${id}`, {
      method: "POST",
      headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
      body: JSON.stringify({
        content: content_text
      })
    })
    .then(response => response.json())
    .then(result => {
      content.innerHTML = result.data;

      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true');
      modal.setAttribute('style', 'display: none');

      const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

      
        document.body,removeChild(modalsBackdrops);
    }
    )
  }
  function likehandler(id, whoYouLiked) {
    const btn = document.getElementById(`btn_${id}`);
    const liked = whoYouLiked.includes(id);

    if (liked) {
        fetch(`/removeLike/${id}`)
            .then(response => response.json())
            .then(result => {
                btn.classList.remove('fa-solid');
                btn.classList.add('fa-thin');
                
                // Find the index of the element in the array and remove it
                const indexToRemove = whoYouLiked.indexOf(id);
                if (indexToRemove !== -1) {
                    whoYouLiked.splice(indexToRemove, 1);
                }
            });
    } else {
        fetch(`/like/${id}`)
            .then(response => response.json())
            .then(result => {
                btn.classList.remove('fa-thin');
                btn.classList.add('fa-solid');

                // Add the id to the array
                whoYouLiked.push(id);
            });
    }
}