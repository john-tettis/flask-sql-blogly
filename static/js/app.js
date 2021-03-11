$first_name = $('#first_name')
$last_name = $('#last_name')
$warning = $('#warning')
console.log('beans')
$('form').on('submit', function(e){
    console.log('SUbmit')
    if(!$last_name.val() || !$first_name.val()){
        e.preventDefault();
        $warning.text('First and Last name are Required fields!')
    }
    else{
        $warning.text('')
    }
})