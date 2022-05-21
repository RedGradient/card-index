function search() {
    let search_input = document.getElementById("search-input");
    let query = search_input.value

    let host = window.location.host
    window.location = 'search?query=' + query
}