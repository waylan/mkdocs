require([
    base_url + '/mkdocs/js/mustache.min.js',
    base_url + '/mkdocs/js/lunr.min.js',
    'text!search-results-template.mustache',
    'text!../search_data.json',
    'text!../search_index.json',
], function (Mustache, lunr, results_template, data, indexDump) {
   "use strict";

    function getSearchTerm()
    {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++)
        {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == 'q')
            {
                return decodeURIComponent(sParameterName[1].replace(/\+/g, '%20'));
            }
        }
    }

    var index = lunr.Index.load(JSON.parse(indexDump));

    data = JSON.parse(data);
    var documents = {};

    for (var i=0; i < data.docs.length; i++){
        var doc = data.docs[i];
        var id = doc.location;
        doc.location = base_url + doc.location;
        documents[id] = doc;
    }

    var search = function(){

        var query = document.getElementById('mkdocs-search-query').value;
        var search_results = document.getElementById("mkdocs-search-results");
        while (search_results.firstChild) {
            search_results.removeChild(search_results.firstChild);
        }

        if(query === ''){
            return;
        }

        var results = index.search(query);

        if (results.length > 0){
            for (var i=0; i < results.length; i++){
                var result = results[i];
                doc = documents[result.ref];
                doc.base_url = base_url;
                doc.summary = doc.text.substring(0, 200);
                var html = Mustache.to_html(results_template, doc);
                search_results.insertAdjacentHTML('beforeend', html);
            }
        } else {
            search_results.insertAdjacentHTML('beforeend', "<p>No results found</p>");
        }

        if(jQuery){
            /*
             * We currently only automatically hide bootstrap models. This
             * requires jQuery to work.
             */
            jQuery('#mkdocs_search_modal a').click(function(){
                jQuery('#mkdocs_search_modal').modal('hide');
            })
        }

    };

    var search_input = document.getElementById('mkdocs-search-query');

    var term = getSearchTerm();
    if (term){
        search_input.value = term;
        search();
    }

    search_input.addEventListener("keyup", search);

});
