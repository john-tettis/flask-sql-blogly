
$warning = $('#warning');
$waring.text('');
$('#user-form').on('submit', function(e){
    $first_name = $('#first_name')
    $last_name = $('#last_name')
    if(!$last_name.val() || !$first_name.val()){
        e.preventDefault();
        $warning.text('First and Last name are Required fields!')
    }
    else{
        $warning.text('')
    }
})
$('#post-form').on('submit', function(e){
    $title = $('#title')
    $content = $('#content')
    if(!$title.val() || !$content.val()){
        e.preventDefault();
        $warning.text('Please fill out all fields')
    }
    else{
        $warning.text('')
    }
})