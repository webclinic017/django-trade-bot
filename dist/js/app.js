// Code goes here
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems);
  });
  
  // Initialize collapsible (uncomment the lines below if you use the dropdown variation)
  // var collapsibleElem = document.querySelector('.collapsible');
  // var collapsibleInstance = M.Collapsible.init(collapsibleElem, options);
  
  // Or with jQuery
  
  $(document).ready(function(){
      // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered

      //init materialize components old fashioned way 
      M.AutoInit();
        
      data_global = {
        Markets: { 
          "url": '/markets'
        },
        Profile: { 
          "url": '/accounts/profile'
        },
        FAQ: { 
          "url": '/faq'
        },
        Questions: { 
          "url": '/faq'
        },
      };
  
      data = { 
        "Markets": null,
        "Profile": null,
        "FAQ": null,
        "Questions": null,
      };
  
      //sidenav
      var isOpen = false;
      var sideNav = $('.sidenav-triggerr');

      sideNav.on('click', function(){
        $('.sidenav').sidenav('open')
        return;
      });

      //autocompletion for search nav
      $('input.autocomplete').autocomplete({
        data: data,
        onAutocomplete: cb,
      });
      
      function cb(val){
        console.log(val);
  
        if(val in  data){
          if(val in data_global){
            var url = data_global[val].url;
  
            console.log(val, url );
            window.location.replace(url);
          }
        }
      }
    });
