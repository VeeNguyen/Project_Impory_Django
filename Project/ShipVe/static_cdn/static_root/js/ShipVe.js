// Always have a selector first

$(document).ready(function(){

    //-----Contact Form handler---------------------------------------------------------------------
    var contactForm = $(".contact-form")

    var contactFormMethod = contactForm.attr("method")  //POST
    var contactFormEndPoint = contactForm.attr("action")  // /abc/

    // The submit loading icon. Reuse available.
    function displaySubmitting(submitBtn, defaultText, doSubmit){
        if (doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending..")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function(event){
        event.preventDefault()

        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

        var contactFormData = contactForm.serialize()
        var thisForm = $(this)

        displaySubmitting(contactFormSubmitBtn, "", true)

        $.ajax({
            url: contactFormEndPoint,
            method: contactFormMethod,
            data: contactFormData,

            success: function(data){
                contactForm[0].reset()
                $.alert({
                    title: "Success!",
                    content: data.message,  // ShipVe/views.py/contact_page has the message
                    theme: "modern",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },
            error: function(error){
                contactForm[0].reset()
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""

                $.each(jsonData, function(key, value){  // jsonData is a dictionary so we use key-value instead of array -> index-object
                    msg += key + ": " + value[0].message
                })

                $.alert({
                    title: "Opps!",
                    content: msg,
                    theme: "modern",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            }
        })
    }) //contactForm


    //-----Auto Search feature---------------------------------------------------------------------
    var searchForm = $(".search-form")

    var searchInput = searchForm.find("[name='q']")  // Input name='q'
    var searchBtn = searchForm.find("[type='submit']")

    var typingTimer;
    var typingInterval = 500;  // .5s

    // Key release
    searchInput.keyup(function(event){
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    // Key pressed
    searchInput.keydown(function(event){
        clearTimeout(typingTimer)
    })

    // The search loading icon
    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching")
    }

    // Performing the Search
    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href = '/search/?q=' + query
        }, 1000)
    }


    //-----Cart and Add/Remove Products feature---------------------------------------------------------------------
    var productForm = $(".form-product-ajax") //got a form selector here

    productForm.submit(function(event){
        event.preventDefault();
        //console.log("Form is not sending as in Ajax works")

        var thisForm = $(this) //to be specific on this form only
        //var actionEndPoint = thisForm.attr("action"); //API EndPoint

        var actionEndPoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method"); //POST
        var formData = thisForm.serialize();


        // Add to cart and Remove
        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,

            success: function(data){
                // 'added' 'removed' from carts/views.py/cart_update portion
                // The button Added or Removed
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("<button type='submit' class='btn btn-success'>Remove</button>")
                } else {
                    submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
                }

                // Updating the number of cart icon
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)
                var currentPath = window.location.href

                // Updating the cart for real
                // If 'cart' is in current path -> refreshCart()
                if (currentPath.indexOf("cart") != -1){
                    refreshCart()
                }
            },
            error: function(error){
                $.alert({
                    title: "Opps!",
                    content: "An error occurred.",
                    theme: "modern",
                })
            }
        })


        //Called when location is cart
        function refreshCart(){
            console.log("in current cart")

            var cartTable = $(".cart-table")
            var cartBody = cartTable.find(".cart-body") //Because cartBody is related to cartTable (parent)
            //cartBody.html("<h1>Changed</h1>")

            var productRows = cartBody.find(".cart-product")
            var currentUrl = window.location.href

            var refreshCartUrl = '/api/cart/'
            var refreshCartMethod = "GET";
            var data = {};

            // Remove feature
            $.ajax({
                url: refreshCartUrl,
                method: refreshCartMethod,
                data: data,

                success: function(data){
                    var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

                    // Updating Subtotal and Total
                    if (data.products.length > 0){
                        productRows.html("")
                        i = data.products.length;  //Counter the number of products

                        $.each(data.products, function(index, value){   //value is product Object
                            console.log("value", value)

                            // Cloning Remove feature for each product
                            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                            newCartItemRemove.css("display", "block")
                            newCartItemRemove.find(".cart-item-product-id").val(value.id)

                            // Prepend brings it to the top of body
                            cartBody.prepend("<tr><th scope=\'row\'>" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                            i--
                        })
                        cartBody.find(".cart-subtotal").text(data.subtotal)
                        cartBody.find(".cart-total").text(data.total)
                    } else {
                        window.location.href = currentUrl  //Refresh the page
                    }
                },
                error: function(error){
                    $.alert({
                        title: "Opps!",
                        content: "An error occurred.",
                        theme: "modern",
                    })
                }
            })
        } //refreshCart
    }) //productForm
//--------------------------------------------------------------------------
}) //documentReady