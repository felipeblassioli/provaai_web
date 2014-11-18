function onLoginButtonClick(){
    if($("#formularioLogin").css("display")=="none") {
        $("#formularioLogin").slideDown();
    }
    else {
        $("#formularioLogin").slideUp();
    }
}

/* Inits UI stuff */
function init(){
    $('.tituloPeca').blurjs({
        source: 'img',
        radius: 5,
        overlay: 'rgba(255,255,255,0.9)',
        optClass: 'blurred',
        cache: false
    });


    $( ".peca" ).mouseenter(function() {
        $(this).find(".tituloPeca").slideDown();
        $(this).find(".descricaoPeca").slideDown();
    });
    $( ".peca" ).mouseleave(function() {
        $(this).find(".tituloPeca").slideUp();
        $(this).find(".descricaoPeca").slideUp();
    });
    $( ".prevDadosPeca" ).mouseenter(function() {
        $(".dadosPeca").slideDown();
    });
    $(".dadosPeca").mouseleave(function() {
        $(".dadosPeca").slideUp();
    });


    $('ul.listaPecas li.peca:nth-child(4n+1)').addClass("first");
    $('ul.listaPecas li.peca:nth-child(4n+4)').addClass("last");
}

$(document).ready(function() {
    console.log("bla2");
    $( "#botaoLogin" ).click(onLoginButtonClick);
    init();
});
