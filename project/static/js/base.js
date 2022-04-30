function search() {
    let search_input = document.getElementById("search");
    let title = search_input.value

    let host = window.location.host
    window.location = 'books?title=' + title
}