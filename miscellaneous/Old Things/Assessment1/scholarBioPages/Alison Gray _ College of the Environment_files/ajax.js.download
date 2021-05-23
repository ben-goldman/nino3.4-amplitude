
//Universal Ajax Filtering
jQuery(function($)
{
    if ( $('body').hasClass('page-template-careers') ) { //only run on careers template page
        //Load posts on document ready
        var ignore_scroll = false;
        var count = 2;
        var firstScroll = true;
        
        ajax_get_posts();
        
        $('#results').on('click', '.load-more', function(){
            $(this).remove();
            ajax_get_posts(count)
        });
     
        //If list item is clicked, trigger input change and add css class
        $('.ajax-filters .button').on('click', function(){
            var input = $(this).find('input'); //Check if clear all was clicked
            if ( $(this).attr('class') == 'clear-all' )
            {
                $('.ajax-filters .button').removeClass('selected').find('input').prop('checked',false); //Clear settings
                ajax_get_posts(); //Load Posts
            }
            else if ($(this).hasClass('selected') )
            {
                $(this).removeClass('selected').attr('aria-pressed', false).find('i').remove();
                count = 2;
                
            } else {
                $(this).addClass('selected').attr('aria-pressed', true).delay(400).queue(function (next) {
                    $(this).prepend('<i class="icon-cross"></i> ');
                    next();
                });
            }
            
            $(this).change();
        });
        
        // sort your posts and if clicked, make selection selected
        $('.sorter ul li').on('click', function(){
            if (!$(this).hasClass('selected') ) {
                $('.sorter ul li').not(this).removeClass('selected').attr('aria-pressed', false);
                $(this).attr('aria-pressed', true).addClass('selected');
                ajax_get_posts();
            }
            
            $(this).change();
        });
        
        //Get Search Form Values
        function getSortValue()
        {
            var sortValue = $('.sorter .selected').data('value'); //Get sorter button value
            return sortValue;
        }
        
        // show breadcrumbs for filtered terms and allow them to be removed by clicking to unselect
        $('#results').on('click', '.filter-crumbs .term-filter', function(){
            var crumbVal = $(this).val();
            var preClass = '.term_id_';
            crumbVal = preClass+crumbVal;
            $(crumbVal).removeClass('selected').find('i').remove();
            count = 2;
            ajax_get_posts();
        });
     
        //If input is changed, load posts
        $('.ajax-filters, .filter-crumbs .term-filter').change( function(){
            count = 2;
            ajax_get_posts(); //Load Posts
        });
     
        //Find Selected terms
        function getSelectedterms()
        {
            var terms = []; //Setup empty array with excluded categories
     
            $(".ajax-filters li .selected").each(function() {
                var val = $(this).val();
                terms.push(val); //Push value onto array
            });
            return terms; //Return all of the selected terms in an array
        }
        
        var delay = (function(){
        var timer = 0;
          return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
          };
        })();
        
        //Fire ajax request when typing in search
        $('#post-search input.text-search').on('keyup', function(e){
            if( e.keyCode == 27 ) {
                $(this).val(''); //If 'escape' was pressed, clear value
            }
            if( e.keyCode == 13 ) {
                return;
            }
            delay(function(){
                var newSearchVal = $('#post-search input.text-search').val();
                var oldSearchVal = $('#post-search input.text-search').attr('data-old-search');
                if (newSearchVal === oldSearchVal) {
                    return;
                } else {
                    count = 2;
                    ajax_get_posts(); //Load Posts
                }
            }, 200 );
        });
        
        $('#submit-search').on('click', function(e){
            e.preventDefault();
            count = 2;
            var newSearchVal = $('#post-search input.text-search').val();
            var oldSearchVal = $('#post-search input.text-search').attr('data-old-search');
            if (newSearchVal === oldSearchVal) {
                return;
            } else {
                ajax_get_posts(); //Load Posts
            }
        });
        
        // when search filter breadcrumb is clicked on, clear the searchbox
        $('#results').on('click', '.filter-crumbs .search-crumb', function(){ 
            $('.search-crumb').remove();
            $('#post-search input.text-search').val('');
            var searchValue = null;
            count = 2;
            ajax_get_posts();
        });
     
        //Get Search Form Values
        function getSearchValue()
        {
            var searchValue = $('#post-search input.text-search').val(); //Get search form text input value
            return searchValue;
        }
     
        //If pagination is clicked, load correct posts
        //$('.pagination a').on('click', function(e){
          //  e.preventDefault();
     
            //var url = $(this).attr('href'); //Grab the URL destination as a string
            //var paged = url.split('&paged='); //Split the string at the occurance of &paged=
     
            //ajax_get_posts(paged[1]); //Load Posts (feed in paged value)
        //});
     
        //Main ajax function
        function ajax_get_posts(paged, infinite)
        {
            var paged_value = paged; //Store the paged value if it's being sent through when the function is called
            var ajax_url = ajax_params.ajax_url; //Get ajax url (added through wp_localize_script)
            var action = $('#results').data('action'); //get wordpress php function for posts - e.g. career-action
            
            if(infinite) {
                $.ajax({
                      url: ajax_params.ajax_url,
                      type:'GET',
                      data: {
                        action: action,
                        terms: getSelectedterms, //Get array of values from previous function
                        search: getSearchValue, //Retrieve search value using function
                        paged: paged_value, //If paged value is being sent through with function call, store here
                        sorter: getSortValue
                      },
                    beforeSend: function ()
                    {
                        //You could show a loader here
                        $("#results").append('<p class="status">Loading additional results...</p>');
                    },
                      success: function(data){
                          $('.status').remove();
                          $("#results").append(data);    // This will be the div where our content will be loaded
                          if (data) ignore_scroll = false;
                      }
                  });
                } else {
     
                $.ajax({

                    type: 'GET',
                    url: ajax_params.ajax_url,
                    data: {
                        action: action,
                        terms: getSelectedterms, //Get array of values from previous function
                        search: getSearchValue, //Retrieve search value using function
                        paged: paged_value, //If paged value is being sent through with function call, store here
                        sorter: getSortValue
                    },
                    beforeSend: function ()
                    {
                        if (paged_value) {
                            //You could show a loader here
                            $("#results").append('<p class="status">Loading more results...</p>');
                        } else {
                          if ($(window).scrollTop() > 355) {
                            $('html, body').animate({
                                scrollTop: $("#post-search").offset().top
                            }, 500);
                          }
                            //You could show a loader here
                            $("#results").html('<p class="status">Loading results...</p>');
                        }
                    },
                    success: function(data)
                    {
                        $('#post-search input.text-search').attr( 'data-old-search', getSearchValue);
                        if (paged_value) {
                            //On load more, remove the loading status, add the data, find the new page count, and put the button at the end
                            $('.status').remove();
                            $('#results').append(data);
                            total = $('#counter').data('page-count');
                            count++;
                            
                            if (count <= total) {
                                $('#results').append('<a class="button load-more"><span class="plus">+</span> Load more</a>');
                            }
                            
                            
                        } else {
                            
                            //On first load, dump the data, get a page count, and add the more button if there's more
                            $('#results').html(data);
                            var total = $('#counter').data('page-count');
                            if(data == '') {
                                $("#results").html('<p class="status">No results found.</p>');
                            }
                            if (count <= total) {
                                $('#results').append('<a class="button load-more"><span class="plus">+</span> Load more</a>');
                            }
                        }
                        if (firstScroll == true) {
                            var newPosts = $('.career').filter(function() {
                                return $(this).attr('id') > localStorage.lastShown;
                            }).map(function() { return '#'+this.id+' .article__meta'; })      .get(); //ToArray;
                            if (window.sessionStorage) {
                                sessionStorage.newPosts = newPosts;
                                console.log(newPosts);
                            }
                            var lastShownID = $('.career').eq(0).attr('id');
                            localStorage.lastShown = lastShownID
                            firstScroll = false;
                        }
                        var newPostsSS = String(sessionStorage.newPosts);
                        if (!$(".new")[0]){
                            $(newPostsSS).prepend('<p class="new"><span class="dashicons dashicons-star-filled"></span> New</p>');
                        }
                    },
                    error: function()
                    {
                        //If an ajax error has occured, do something here...
                        $("#results").html('<p>There has been an error</p>');
                    }
                });
            };
        }
    }
});
 
