function confirmDelete(event) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ? Cette action est irréversible.')) {
        event.preventDefault();
        return false;
    }
    return true;
}