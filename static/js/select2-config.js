// Configuration globale pour les champs Select2
document.addEventListener('DOMContentLoaded', function() {
    // Fonction pour initialiser Select2 sur un élément
    function initSelect2(element) {
        $(element).select2({
            language: 'fr',
            placeholder: 'Rechercher...',
            allowClear: true,
            width: '100%'
        });
    }
    
    // Initialise Select2 sur tous les champs select existants avec la classe .select2-field
    if (typeof $.fn.select2 !== 'undefined') {
        $('.select2-field').each(function() {
            initSelect2(this);
        });
        
        // Gestion spéciale pour les formsets
        // Quand on ajoute un nouveau formulaire dans un formset
        $(document).on('click', '.add-form-button', function() {
            // Temporisation pour laisser le DOM se mettre à jour
            setTimeout(function() {
                // Initialise Select2 sur les nouveaux champs ajoutés
                $('.select2-field:not(.select2-hidden-accessible)').each(function() {
                    initSelect2(this);
                });
            }, 100);
        });
        
        // Réinitialisation des Select2 après la mise à jour des indices de formset
        $(document).on('formset:added', function(event, $row, formsetName) {
            // Initialiser Select2 sur les nouveaux champs
            $row.find('.select2-field').each(function() {
                initSelect2(this);
            });
        });
        
        // Gérer les Select2 dans les onglets Bootstrap (s'ils sont utilisés)
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $('.select2-field').each(function() {
                $(this).select2('destroy');
                initSelect2(this);
            });
        });
    }
}); 