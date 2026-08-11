let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        //console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
   // console.log(place);
   var geocoder=new google.maps.Geocoder()
   var address=document.getElementById('id_address').value

   geocoder.geocode({'address':address},function(results,status){
    // console.log('results=>',results)
    // console.log('status=>',status)
    if(status==google.maps.GeocoderStatus.OK){
        var latitude = results[0].geometry.location.lat();
        var longitude = results[0].geometry.location.lng();


        // console.log('lat=>',latitude);
        // console.log('lng=>',longitude);

        $('#id_latitude').val(latitude);
        $('#id_longitude').val(longitude);


        $('#id_address').val(address);
    }
   });

   // loop through the address components and assign other address data
   console.log(place.address_components)
   for(var i=0; i<place.address_components.length;i++){
      for(var j=0; j<place.address_components[i].types.length;j++){
           // get country
           if(place.address_components[i].types[j]=='country'){
            $('#id_country').val(place.address_components[i].long_name);
           }
           // get state
           if(place.address_components[i].types[j]=='administrative_area_level_1'){
            $('#id_state').val(place.address_components[i].long_name);
           }

           // get city
           if(place.address_components[i].types[j]=='locality'){
            $('#id_city').val(place.address_components[i].long_name);
           }

            // get pincode
           if(place.address_components[i].types[j]=='postal_code'){
            $('#id_pin_code').val(place.address_components[i].long_name);
           }else{
               $('#id_pin_code').val("");
           }

      }
   }
}




// DON'T EDIT ABOVE THIS LINE




$(document).ready(function(){
    console.log('custom.js loaded');

    $.ajaxSetup({
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });

    // safe swal wrapper: if SweetAlert isn't loaded, don't throw
    function safeSwal(title, text, icon, thenCallback){
        try{
            if (typeof swal === 'function'){
                var result = swal(title, text, icon);
                if (thenCallback && result && typeof result.then === 'function'){
                    result.then(thenCallback);
                }
            } else {
                if (thenCallback) thenCallback();
                else console && console.warn && console.warn('swal not available');
            }
        } catch(err){
            console && console.error && console.error('safeSwal error', err);
            if (thenCallback) thenCallback();
        }
    }

    $(document).on('click', '.add_to_cart', function(e){
        e.preventDefault();
        const product_id = $(this).attr('data-id');
        const url = $(this).attr('data-url');
        console.log('add_to_cart clicked', product_id, url);

        if (!url) {
            console.error('Add to cart missing data-url');
            return;
        }

        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            cache: false,
            success: function(response){
                console.log('add_to_cart response', response);
                if (response.status === 'Success') {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    $('#qty-'+product_id).html(response.qty);
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );

                } else if (response.status === 'login_required') {
                    safeSwal(response.message, '', 'info', function(){
                        window.location = '/login';
                    });
                } else {
                    safeSwal(response.message, '', 'error');
                }
            },
            error: function(xhr, status, error){
                console.error('Add to cart AJAX error:', status, error, xhr.responseText);
            }
        });
    });

    $(document).on('click', '.decrease_cart', function(e){
        e.preventDefault();
        const product_id = $(this).attr('data-id');
        const url = $(this).attr('data-url');
        const cart_id = $(this).attr('id');
        console.log('decrease_cart clicked', product_id, url);

        if (!url) {
            console.error('Decrease cart missing data-url');
            return;
        }

        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            cache: false,
            success: function(response){
                console.log('decrease_cart response', response);
                if (response.status === 'Success') {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    $('#qty-'+product_id).html(response.qty);
                      if(window.location.pathname =='/cart/'){
                    removeCartItem(response.qty, response.cart_id);
                    checkEmptyCart();
                           applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );
                }
                } else if (response.status === 'login_required') {
                    safeSwal(response.message, '', 'info', function(){
                        window.location = '/login';
                    });
                } else {
                    safeSwal(response.message, '', 'error');
                }
            },
            error: function(xhr, status, error){
                console.error('Decrease cart AJAX error:', status, error, xhr.responseText);
            }
        });
    });

    $('.item_qty').each(function(){
        const product_id = $(this).data('id');
        const qty = $(this).data('qty');
        if (product_id !== undefined) {
            $('#qty-'+product_id).html(qty);
        }
    })

    // DELETE CART ITEM
    // robust DELETE CART ITEM handler — listens on the anchor or any child element click
    $(document).on('click', '.delete_cart, .delete_cart *', function(e){
        // find the closest anchor with the delete_cart class
        var anchor = $(e.target).closest('.delete_cart');
        if (!anchor || !anchor.length) return;
        e.preventDefault();

        const cart_id = anchor.attr('data-id');
        const url = anchor.attr('data-url');
        console.log('delete_cart clicked (resolved)', cart_id, url, 'eventTarget=', e.target);

        if (!url) {
            console.error('Delete cart missing data-url');
            return;
        }

        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            cache: false,
            success: function(response){
                console.log('delete_cart response', response);
                if (response.status === 'Failed') {
                    safeSwal(response.message, '', 'error');
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    // remove immediately so UI is responsive, then show message
                    removeCartItem(0, cart_id);
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );
                    checkEmptyCart();
                    safeSwal(response.status, response.message, 'success');
                }
            },
            error: function(xhr, status, error){
                console.error('Delete cart AJAX error:', status, error, xhr.responseText);
                // fallback: if AJAX fails (JSON parse error, network), navigate to the delete URL
                if (url) {
                    console.warn('Falling back to full-page delete at', url);
                    window.location = url;
                }
            }
        });
    });

    // remove the deleted cart item from the DOM
    function removeCartItem(cartItemQty, cart_id){
      
          
         if(cartItemQty <= 0){
            // remove the cart item element
            $('#cart-item-'+cart_id).remove();
        
        }

  
    }

    // check if the cart is empty and display a message
    function checkEmptyCart(){
        var cart_counter=document.getElementById('cart_counter').innerHTML;
        if(cart_counter==0){
            document.getElementById("empty-cart").style.display='block';
        }
    }

    // apply cart amounts
    function applyCartAmounts(subtotal, tax_dict, grand_total){
        if(window.location.pathname == '/cart/'){
            var s = Number(subtotal) || 0;
            var g = Number(grand_total) || 0;
            $('#subtotal').text(s.toFixed(2));
            // template uses id="total" for grand total
            $('#total').text(g.toFixed(2));

            if (tax_dict && typeof tax_dict === 'object') {
                for (var key1 in tax_dict) {
                    if (!tax_dict.hasOwnProperty(key1)) continue;
                    var taxItem = tax_dict[key1];
                    for (var key2 in taxItem) {
                        if (!taxItem.hasOwnProperty(key2)) continue;
                        $('#tax-' + key1).text(Number(taxItem[key2] || 0).toFixed(2));
                    }
                }
            }
        }
    }

    // Native capture-phase fallback: intercept clicks on the delete icon early
    // This ensures deletion works even if other listeners stop propagation
    document.addEventListener('click', function(e){
        var target = e.target;
        var anchor = target.closest ? target.closest('.delete_cart') : null;
        if (!anchor) return;
        // Prevent duplicate handling by stopping further propagation
        e.preventDefault();
        e.stopPropagation();

        var cart_id = anchor.getAttribute('data-id');
        var url = anchor.getAttribute('data-url');
        console.log('native capture delete clicked', cart_id, url, 'eventTarget=', target);

        if (!url) {
            console.error('Delete cart missing data-url (native)');
            return;
        }

        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            cache: false,
            success: function(response){
                console.log('delete_cart response (native)', response);
                if (response.status === 'Failed') {
                    safeSwal(response.message, '', 'error');
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    removeCartItem(0, cart_id);
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );
                    checkEmptyCart();
                    safeSwal(response.status, response.message, 'success');
                }
            },
            error: function(xhr, status, error){
                console.error('Delete cart AJAX error (native):', status, error, xhr.responseText);
                if (url) {
                    console.warn('Falling back to full-page delete at', url);
                    window.location = url;
                }
            }
        });
    }, true);

        // ADD OPENING HOUR
    function toggleOpeningHourFields() {
        var isClosed = document.getElementById('id_is_closed').checked;
        document.getElementById('id_from_hour').disabled = isClosed;
        document.getElementById('id_to_hour').disabled = isClosed;
        if (isClosed) {
            document.getElementById('id_from_hour').value = '';
            document.getElementById('id_to_hour').value = '';
        }
    }

    $('#id_is_closed').on('change', function() {
        toggleOpeningHourFields();
    });

    toggleOpeningHourFields();

    $('#opening_hours').on('submit', function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value

        if (is_closed) {
            from_hour = '';
            to_hour = '';
        }

        console.log(day, from_hour, to_hour, is_closed, csrf_token)

        var validDays = ['1','2','3','4','5','6','7'];
        var condition;
        if(is_closed){
            is_closed = 'True'
            condition = validDays.includes(day);
        }else{
            is_closed = 'False'
            condition = validDays.includes(day) && from_hour != '' && to_hour != '';
        }

        if(condition){
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: function(response){
                    if(response.status == 'success'){
                        var currentPath = window.location.pathname.replace(/\/$/, '')
                        var removeUrl = currentPath + '/remove/' + response.id + '/'
                        if(response.is_closed == 'Closed'){
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="'+removeUrl+'">Remove</a></td></tr>';
                        }else{
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="'+removeUrl+'">Remove</a></td></tr>';
                        }
                        
                        $(".opening_hours").append(html)
                        document.getElementById("opening_hours").reset();
                    }else{
                        swal(response.message, '', "error")
                    }
                }
            })
        }else{
            swal('Please fill all fields', '', 'info')
        }
    });

    // REMOVE OPENING HOUR
    $(document).on('click', '.remove_hour', function(e){
        var url = $(this).attr('href') || $(this).data('url');
        if (!url) return;
        e.preventDefault();
        console.log('remove_hour click', url);

        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            cache: false,
            success: function(response){
                console.log('remove_hour response', response);
                if(response && response.status === 'success'){
                    var row = document.getElementById('hour-'+response.id);
                    if(row) row.remove();
                }
            },
            error: function(xhr, status, error){
                console.error('remove_hour AJAX error', status, error, xhr.responseText);
                if (url) {
                    window.location = url;
                }
            }
        });
    });
     // document ready close 
});
