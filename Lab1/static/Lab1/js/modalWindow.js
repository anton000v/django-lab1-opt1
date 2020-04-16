function modalDisplay() {
  $('#modal_window').show();
  $('#modal_window').css('display', 'block');
  $('#modal_window').css('display', 'block');
  setTimeout(modalClose, 4000);
}

// When the user clicks on <span> (x), close the modal
function modalClose() {
  $('#modal_window').hide();
}

// When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }
