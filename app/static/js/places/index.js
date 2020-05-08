/* FILTRY */

    /* povoluje otevírací dobu 'no data', pokud je checknuté 'opened places only' */
        $(document).ready( function(){
            if(document.getElementById('filters-OpenedState').checked)
            {
                document.getElementById('filters-OpenedStateNone').disabled = false;
            }
        });

    /* zakazuje otevírací dobu 'no data', pokud je unchecknuté 'opened places only' */
        function Disable(hiddenElId){
            if(document.getElementById(hiddenElId).disabled)
            {
                document.getElementById(hiddenElId).disabled = false;
            }
            else
            {
                document.getElementById(hiddenElId).disabled = true;
                document.getElementById(hiddenElId).checked = false;
            }
        }

/* COLLAPSING METODY */
    $("#filters-placeTypes").on('shown.bs.collapse', function(){
        document.getElementById('filters-placeTypesArrow').classList.remove('fa-caret-right');
        document.getElementById('filters-placeTypesArrow').classList.add('fa-caret-up');
      });
    $("#filters-placeTypes").on('hidden.bs.collapse', function(){
        document.getElementById('filters-placeTypesArrow').classList.remove('fa-caret-up');
        document.getElementById('filters-placeTypesArrow').classList.add('fa-caret-right');
    });
    $("#filters-Section").on('shown.bs.collapse', function(){
        document.getElementById('filters-ShowHideButton').innerText = "Hide filters";
        document.getElementById('filters-ButtonSeparator').hidden = false;
      });
    $("#filters-Section").on('hidden.bs.collapse', function(){
        document.getElementById('filters-ShowHideButton').innerText = "Show filters";
        document.getElementById('filters-ButtonSeparator').hidden = true;
      });