// // $(document).ready(function(){
// //   $(".team-heading").click(function(){
// //     $(".menu").toggleClass("showMenu");
// //       $(".menu > option").click(function(){
// //         $(".team-heading > p").text($(this).text());
// //         $(".menu").removeClass("showMenu");
// //       });
// //   });


// let selectElement = $('#select');
// let numberOfOptions = selectElement.children('option').length;

// /* Add class hidden to default select element to hide it */
// selectElement.addClass('hidden');

// selectElement.after('<div class="select"></div>');

// let selectStyled = selectElement.next('.select');
// selectStyled.text(selectElement.children('option').eq(0).text());

// let list = $('<ul />', {
//     'class': 'select-options'
// }).insertAfter(selectStyled);

// for (let i = 0; i < numberOfOptions; i++) {
//     $('<li />', {
//         text: selectElement.children('option').eq(i).text(),
//         rel: selectElement.children('option').eq(i).val()
//     }).appendTo(list);
// }

// let listItems = list.children('li');

// selectStyled.click(function(e) {
//     e.stopPropagation();
//     $('.select.active').each(function(){
//         $(this).removeClass('active').next('ul.select-options').hide();
//     });
//     $(this).toggleClass('active').next('ul.select-options').toggle();
// });

// listItems.click(function(e) {
//     e.stopPropagation();
//     selectStyled.text($(this).text()).removeClass('active');
//     selectElement.val($(this).attr('rel'));
//     list.hide();
// });

// $(document).click(function() {
//     selectStyled.removeClass('active');
//     list.hide();
// });
