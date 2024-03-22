const sortButton = document.getElementById('sort-button');
    sortButton.addEventListener('click', handleSortClick);

    const genreButton = document.getElementById('')

    function sortByDate(a, b){
        const releaseDateA = new Date(a.dataset.releaseDate);
        const releaseDateB = new Date(b.dataset.releaseDate);
        
        return releaseDateB - releaseDateA;
    }

    function sortByPopularity(a,b){
        const popularityA = a.dataset.popularity
        const popularityB = b.dataset.popularity

        return popularityB - popularityA;
    }

    function sortByTitle(a, b) {
        const titleA = a.dataset.title;
        const titleB = b.dataset.title;
        if (titleA < titleB) return -1;
        if (titleA > titleB) return 1;
        return 0;
    }

    function sortMoviesByCriteria(sortFunc){
        const resultsContainer = document.getElementById('movies-container');
        const results = Array.from(resultsContainer.querySelectorAll('.movie-card'));
        
        results.sort(sortFunc);
    
        // Clear the container
        resultsContainer.innerHTML = '';
    
        // Append the sorted results to the container
        results.forEach(result => resultsContainer.appendChild(result));
    }

    function handleSortClick() {
        const sortSelect = document.getElementById('sort-select');
        const selectedOption = sortSelect.value;
    
        switch (selectedOption) {
            case 'popularity':
                sortMoviesByCriteria(sortByPopularity);
                break;
            case 'release_date':
                sortMoviesByCriteria(sortByDate);
                break;
            case 'title':
                sortMoviesByCriteria(sortByTitle);
                break;
            default:
                // No sorting or default sorting logic
                break;
        }
    }

    document.getElementById('filter-button').addEventListener('click', function() {
    const genreFilters = document.querySelectorAll('#genre-filter input[type="checkbox"]:checked');
    const selectedGenreIds = Array.from(genreFilters).map(input => parseInt(input.value));
    const releaseDateFilters = document.querySelectorAll('#release-date-filter input[type="checkbox"]:checked');
    const languageFilters = document.querySelectorAll('#language-filter input[type="checkbox"]:checked');

    const filteredReleaseDates = Array.from(releaseDateFilters).map(input => input.value);
    const filteredLanguages = Array.from(languageFilters).map(input => input.value);

    const movies = document.querySelectorAll('.movie-card');

    movies.forEach(movie => {
        // Parse the movie's data-genre attribute into an array of integers
        const movieGenreIds = movie.getAttribute('data-genre').split(',').map(Number);
        
        // Check if the movie's genre list contains any of the selected genres
        const isGenreMatch = selectedGenreIds.length === 0 || selectedGenreIds.some(id => movieGenreIds.includes(id));
        
        const movieReleaseDate = new Date(movie.getAttribute('data-release-date'));
        const movieLanguage = movie.getAttribute('data-language');

        // For language matching, ensure the comparison accounts for any language
        const isLanguageMatch = filteredLanguages.length === 0 || filteredLanguages.includes(movieLanguage);
        
        // Release date matching logic remains the same
        const isReleaseDateMatch = filteredReleaseDates.length === 0 || filteredReleaseDates.some(filter => {
            const today = new Date();
            const monthsAgo = new Date(today.getFullYear(), today.getMonth() - parseInt(filter), today.getDate());
            return movieReleaseDate >= monthsAgo;
        });

        if (isGenreMatch && isLanguageMatch && isReleaseDateMatch) {
            movie.style.display = 'inline-block';
        } else {
            movie.style.display = 'none';
        }
        if (isGenreMatch && isLanguageMatch && isReleaseDateMatch) {
            movie.style.display = 'inline-flex'; // Make sure to match the initial display style
        } else {
            movie.style.display = 'none';
        }

        // If you have specific styles that need to be reapplied to visible cards, do it here
        reapplyStyles(movie); // Assuming this function is defined to reapply dynamic styles
    });
});
    function reapplyStyles(movieCard) {
        // This is a placeholder for any style re-application logic
        // For example, if you need to reset certain styles to ensure consistency after filtering:
        movieCard.style.height = '380px'; // Resetting height, if dynamically changed
        // Other style adjustments can be made here
    }