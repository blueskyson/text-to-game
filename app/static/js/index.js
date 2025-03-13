function deleteGame(gameId) {
    const url = `/delete_game/${gameId}`;

    if (confirm('Are you sure you want to delete this game?')) {
        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                // Redirect to the homepage after successful deletion
                window.location.href = '/';
            } else {
                console.error('Failed to delete the game');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}