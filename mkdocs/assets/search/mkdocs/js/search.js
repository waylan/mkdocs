require([
    base_url + '/mkdocs/js/operative.min.js',
    base_url + '/mkdocs/js/mustache.min.js',
    'text!search-results-template.mustache',
    'text!../search_data.json',
    'text!../search_index.json',
], function (operative, Mustache, results_template, data, indexDump) {
    "use strict";

    var searchWorker = operative({
        documents: {},

        init: function(data, indexDump, callback) {
            // setup search
            indexDump = JSON.parse(indexDump);
            data = JSON.parse(data);
            self = this;

            function isEmptyObject(obj) {
                // See http://stackoverflow.com/a/34491287/866026
                for (var x in obj) { return false; }
                return true;
            }

            if (! isEmptyObject(indexDump)) {
                // Load prebuilt index
                console.debug('Loading pre-built index...');
                self.index = lunr.Index.load(indexDump);

                for (var i=0; i < data.docs.length; i++) {
                    var doc = data.docs[i];
                    self.documents[doc.location] = doc;
                }
            } else {
                // No prebuilt index. create it
                console.debug('Building index...');
                self.index = lunr(function () {
                    this.field('title', {boost: 10});
                    this.field('text');
                    this.ref('location');
                });

                for (var i=0; i < data.docs.length; i++) {
                    var doc = data.docs[i];
                    doc.location = base_url + doc.location;
                    self.index.add(doc);
                    self.documents[doc.location] = doc;
                }
            }
            // Success! return true
            callback(true);
        },

        search: function(query, callback) {
            // run search query
            var results = this.index.search(query);
            var documents = [];
            for (var i=0; i < results.length; i++) {
                    var result = results[i];
                    doc = this.documents[result.ref];
                    doc.summary = doc.text.substring(0, 200);
                    documents.push(doc);
            }
            callback({documents: documents});
        }
    }, [
        // webworker dependencies
        base_url + '/mkdocs/js/lunr.min.js'
    ]);

    function getSearchTerm() {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == 'q') {
                return decodeURIComponent(sParameterName[1].replace(/\+/g, '%20'));
            }
        }
    }

    var search = function() {
        var query = document.getElementById('mkdocs-search-query').value;
        var search_results = document.getElementById("mkdocs-search-results");
        while (search_results.firstChild) {
            search_results.removeChild(search_results.firstChild);
        }

        if(query === '') {
            return;
        }

        searchWorker.search(query, function(result){
            if (result.documents.length > 0) {
                for (var i=0; i < result.documents.length; i++) {
                    var doc = result.documents[i];
                    doc.base_url = base_url;
                    var html = Mustache.to_html(results_template, doc);
                    search_results.insertAdjacentHTML('beforeend', html);
                }
            } else {
                search_results.insertAdjacentHTML('beforeend', "<p>No results found</p>");
            }

            if(jQuery) {
                /*
                 * We currently only automatically hide bootstrap models. This
                 * requires jQuery to work.
                 */
                jQuery('#mkdocs_search_modal a').click(function() {
                    jQuery('#mkdocs_search_modal').modal('hide');
                })
            }
        });
    };

    // Run search init
    searchWorker.init(data, indexDump, function(result) {
        if (result) {
            console.debug('search init complete');
            var search_input = document.getElementById('mkdocs-search-query');

            var term = getSearchTerm();
            if (term) {
                search_input.value = term;
                search();
            }

            search_input.addEventListener("keyup", search);
        }
    });
});
