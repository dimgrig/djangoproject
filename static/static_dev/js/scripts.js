$(document).ready(function(){
    var form_buying_product = $('#form_buying_product');
    var form_for_token = $('#form_for_token');
    //console.log(form);


    function basketUpdating(product_id, nmb, name, price, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        data.name = name;
        data.price = price;
        //var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();

        var csrf_token = $('#form_for_token [name="csrfmiddlewaretoken"]').val();

        data["csrfmiddlewaretoken"] = csrf_token;

        var url = form_for_token.attr("action");

        if (is_delete){
            data["is_delete"] = true;
        }
        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK");
                //console.log(data.products_total_nmb);
                if (data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#basket_total_nmb').text(" (" + data.products_total_nmb + ")");
                    //console.log(data.products_total_nmb);
                    console.log(data.products);
                    $('.basket-items').html("");
                }
                 if (data.products_total_nmb) {
                    $.each(data.products, function (k, v) {
                        $('.basket-items').append(
                            '<span><li>' +
                            v.name +
                            ' - ' +
                            v.nmb +
                            ' шт. ' +
                            ' - ' +
                            parseInt(v.price_per_item) * v.nmb +
                            ' руб. ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>' +
                            '</li></span>');
                    });
                }

            },
            error: function () {
                console.log("error")
            }
        });
    }

    form_buying_product.on('submit', function (e) {
        e.preventDefault();

        var nmb = $('#number').val();

        var submit_btn = $('#submit_btn');
        var product_id = submit_btn.data("product_id");
        var name = submit_btn.data("name");
        var price = submit_btn.data("price");

        //console.log(nmb);
        //console.log(product_id);
        //console.log(name);
        //console.log(price);

        basketUpdating(product_id, nmb, name, price, is_delete=false)

    })

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();

        product_id = $(this).data("product_id");
        console.log("ID");
        console.log(product_id);
        nmb = 0;
        name='';
        price='';
        basketUpdating(product_id, nmb, name, price, is_delete=true);

        //$(this).closest('li').remove();

    });

    function calculatingBasketAmount(){
        var total_order_amount = 0;

        $('.product_in_basket_amount').each(function () {
            total_order_amount += parseFloat($(this).text());
        });

        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    calculatingBasketAmount();



    $(document).on('change', '.product_in_basket_nmb', function(e){

        var product_in_basket_nmb = parseFloat($(this).val());
        //console.log(product_in_basket_nmb);
        var current_tr = $(this).closest('tr');
        var product_in_basket_price_per_item = current_tr.find($('.product_in_basket_price_per_item'));
        var product_in_basket_amount = current_tr.find($('.product_in_basket_amount'));
        var price = parseFloat(product_in_basket_price_per_item.text());

        product_in_basket_amount.text(parseFloat(price*product_in_basket_nmb).toFixed(2));

        calculatingBasketAmount();
    });
});

