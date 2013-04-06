// util

var throttle = function(fn, delay) {
    var timer = null;
    return function () {
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            fn.apply(context, args);
        }, delay);
    };
};


// search

var Search = {
    init: function($input, $results) {
        var that = this;
        this.xhr = null;
        this.$input = $input;
        this.$results = $results;

        $input.keyup(function() { 
            var search = $input.val().toUpperCase();
            console.log(search);
            throttle(that._remoteSearch(search), 250);
        });
    },

    _remoteSearch: function(search) {
        var that = this;

        if(search.length < 2) {
            this._clearResults();
            return;
        }

        if(this.xhr != null) {
            this.xhr.abort();
        }

        this.xhr = $.getJSON('/lookup/', {search:search}, function(data) {
            that._renderResults(data);
        });
    },

    _clearResults: function() {
        this.$results.html("").css("padding-bottom", "0px");
        this.$results.removeClass('hh');
    },

    _noResults: function() {
        var result = '<li><i class="icon-flag"></i> Nothing found</li>';
        this.$results.removeClass('hh');
        this.$results.html(result);
    },

    _renderResults: function(data) {
        var result = "";

        // any results?
        if(!data) {
            this._noResults();
            return;
        }

        result += '<li><i class="icon-flag"></i> MPs:</li>';
        
        _.each(data, function(item, i) {
            // console.log(item);
            result += '<li><a href="/mp/' + item.person_id + '">' + item.name + '</a></li>';
    // "name": "Bridget Phillipson",
    // "member_id": "40323"
        });


        console.log(result);
        console.log(this.$results);
        this.$results.addClass('hh');

        this.$results.html(result);
    }
};


$(function(){

    window.search = Object.create(Search);
    window.search.init($('input[name=search]'), $('#search-results'));

    // Make links work in iOS fullscreen web app
    // $("a").click(function (event) {
    //     event.preventDefault();
    //     window.location = $(this).attr("href");
    // });

});  


// if mobile, hide address bar when window has loaded
$(window).load(function(){
    /mobi/i.test(navigator.userAgent) && !location.hash && setTimeout(function () {
        if (!pageYOffset) window.scrollTo(0, 1);
    }, 1200);
});

