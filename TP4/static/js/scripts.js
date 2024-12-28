document.addEventListener('DOMContentLoaded', function () {
    /**
     * Affiche une fenêtre d'alerte pour signaler une erreur
     * @param {string} message - Le message d'erreur à afficher
     */
    function showErrorAlert(message) {
        alert(message); // Utilise une alerte JavaScript classique
    }

    /**
     * Gère la soumission d'un formulaire avec fetch
     * @param {HTMLFormElement} form - Le formulaire à soumettre
     * @param {string} url - L'URL cible
     * @param {Function} onSuccess - Callback en cas de succès
     * @param {Function} onError - Callback en cas d'erreur
     */
    async function handleFormSubmit(form, url, onSuccess, onError) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: new URLSearchParams(new FormData(form)),
            });

            if (response.ok) {
                const result = await response.json();
                onSuccess(result);
            } else {
                const error = await response.json();
                onError(error.error || "Une erreur s'est produite.");
            }
        } catch (err) {
            onError("Erreur réseau. Veuillez réessayer.");
        }
    }

    // Gestion de la soumission du formulaire de modification de pièce
    const editPieceForm = document.querySelector('#edit-piece-form');
    if (editPieceForm) {
        editPieceForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Empêche le comportement par défaut du formulaire

            const formData = new FormData(editPieceForm);

            try {
                const response = await fetch('/modifier_piece', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log("Modification réussie :", result.message);
                    // Recharge la page pour refléter les changements
                    window.location.reload();
                } else {
                    const error = await response.json();
                    console.error("Erreur lors de la modification :", error.error);
                    showErrorAlert(error.error || "Une erreur s'est produite.");
                }
            } catch (err) {
                console.error("Erreur réseau :", err);
                showErrorAlert("Erreur réseau. Veuillez réessayer.");
            }
        });
    }

    // Gestion de la modale d'édition des pièces
    const editPieceModal = document.getElementById('editPieceModal');
    if (editPieceModal) {
        editPieceModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            // Chargement des données depuis les attributs data-*
            const id = button.getAttribute('data-id');
            const nom = button.getAttribute('data-nom');
            const x = button.getAttribute('data-x');
            const y = button.getAttribute('data-y');
            const z = button.getAttribute('data-z');

            // Remplissage des champs du formulaire dans la modale
            editPieceModal.querySelector('#edit-piece-id').value = id;
            editPieceModal.querySelector('#edit-piece-nom').value = nom;
            editPieceModal.querySelector('#edit-piece-x').value = x;
            editPieceModal.querySelector('#edit-piece-y').value = y;
            editPieceModal.querySelector('#edit-piece-z').value = z;
        });
    }

    // Gestion de la modale d'ajout des capteurs
    const addCapteurModal = document.getElementById('addCapteurModal');
    if (addCapteurModal) {
        addCapteurModal.addEventListener('show.bs.modal', function () {
            const form = addCapteurModal.querySelector('form');
            form.reset(); // Réinitialise le formulaire lorsque la modale est ouverte

            // Définit la date maximale pour aujourd'hui
            const dateInput = form.querySelector('#date-installation');
            if (dateInput) {
                const today = new Date().toISOString().split('T')[0];
                dateInput.max = today;
            }
        });
    }

    // Gestion de la modale d'édition des capteurs
    const editCapteurModal = document.getElementById('editCapteurModal');
    if (editCapteurModal) {
        editCapteurModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            // Chargement des données depuis les attributs data-*
            const id = button.getAttribute('data-id');
            const ref = button.getAttribute('data-ref');
            const typeId = button.getAttribute('data-type');
            const date = button.getAttribute('data-date');

            // Remplissage des champs du formulaire dans la modale
            editCapteurModal.querySelector('#capteur-id').value = id;
            editCapteurModal.querySelector('#edit-ref-commerciale').value = ref;
            editCapteurModal.querySelector('#edit-id-type').value = typeId;
            editCapteurModal.querySelector('#edit-date-installation').value = date;

            // Définit la date maximale pour aujourd'hui
            const dateInput = editCapteurModal.querySelector('#edit-date-installation');
            if (dateInput) {
                const today = new Date().toISOString().split('T')[0];
                dateInput.max = today;
            }
        });
    }

    // Gestion de la soumission des formulaires pour ajouter une pièce
    const addPieceForm = document.querySelector('form[action*="ajouter_piece"]');
    if (addPieceForm) {
        addPieceForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const logementId = window.location.href.split('/').pop();
            handleFormSubmit(addPieceForm, `/ajouter_piece/${logementId}`,
                () => window.location.reload(),
                showErrorAlert
            );
        });
    }

    // Gestion de la soumission des formulaires pour ajouter un capteur
    const addCapteurForm = document.querySelector('#add-capteur-form');
    if (addCapteurForm) {
        addCapteurForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const pieceId = window.location.href.split('/').pop();
            handleFormSubmit(addCapteurForm, `/ajouter_capteur/${pieceId}`,
                () => window.location.reload(),
                showErrorAlert
            );
        });
    }

    // Gestion de la soumission des formulaires pour ajouter un logement
    const addLogementForm = document.querySelector('#add-logement-form');
    if (addLogementForm) {
        addLogementForm.addEventListener('submit', function (event) {
            event.preventDefault();
            handleFormSubmit(addLogementForm, '/ajouter_logement',
                () => {
                    window.location.reload(); // Recharge la page en cas de succès
                },
                (errorMessage) => {
                    showErrorAlert(errorMessage); // Affiche l'erreur dans une alerte
                }
            );
        });
    }

// Gestion de la soumission des formulaires pour modifier un logement
const editLogementForm = document.querySelector('#edit-logement-form');
if (editLogementForm) {
    editLogementForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Empêche le comportement par défaut du formulaire

        const formData = new FormData(editLogementForm);

        // Facultatif : vérifier si les champs sont bien remplis
        if (!formData.get('id') || !formData.get('adresse') || !formData.get('num_tel') || !formData.get('ip')) {
            alert("Tous les champs sont obligatoires !");
            return;
        }

        try {
            const response = await fetch('/modifier_logement', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                console.log("Modification réussie :", result.message);
                alert(result.message); // Affiche un message de succès
                window.location.reload(); // Recharge la page
            } else {
                const error = await response.json();
                console.error("Erreur lors de la modification :", error.error);
                alert(error.error || "Une erreur s'est produite.");
            }
        } catch (err) {
            console.error("Erreur réseau :", err);
            alert("Erreur réseau. Veuillez réessayer.");
        }
    });
}




    // Gestion des suppressions avec confirmation
    const deleteForms = document.querySelectorAll('form[action*="supprimer_"]');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const confirmation = confirm("Êtes-vous sûr de vouloir supprimer cet élément ?");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });

    // Mise à jour en temps réel des capteurs
    setInterval(() => {
        const pieceId = window.location.href.split('/').pop();
        fetch(`/update_valeurs/${pieceId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data) {
                    data.forEach(capteur => {
                        const row = document.querySelector(`tr[data-id="${capteur.id}"]`);
                        if (row) {
                            row.querySelector('.derniere-valeur').textContent = capteur.valeur || "N/A";
                            const now = new Date();
                            row.querySelector('.heure-mesure').textContent = now.toLocaleString();
                        }
                    });
                }
            })
            .catch(err => console.error("Erreur lors de la mise à jour des capteurs :", err));
    }, 5000);
});



document.addEventListener('DOMContentLoaded', function () {
    const logementId = window.location.href.split('/').pop();

    fetch(`/factures_data/${logementId}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('consommationChart').getContext('2d');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.types,
                    datasets: [
                        {
                            label: 'Montant Total (€)',
                            data: data.montants,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        },
                        {
                            label: 'Consommation Totale',
                            data: data.consommations,
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        })
        .catch(err => console.error('Erreur lors du chargement des données du graphique :', err));
});

// Gestion de la modale d'édition des logements
const editLogementModal = document.getElementById('editLogementModal');
if (editLogementModal) {
    editLogementModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        // Récupérer les données depuis les attributs data-*
        const id = button.getAttribute('data-id');
        const adresse = button.getAttribute('data-adresse');
        const numTel = button.getAttribute('data-numtel');
        const ip = button.getAttribute('data-ip');

        // Remplir les champs du formulaire
        editLogementModal.querySelector('#logement-id').value = id;
        editLogementModal.querySelector('#edit-adresse').value = adresse;
        editLogementModal.querySelector('#edit-num-tel').value = numTel;
        editLogementModal.querySelector('#edit-ip').value = ip;
    });
}
