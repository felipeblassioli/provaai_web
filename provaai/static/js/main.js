$( "#botaoLogin" ).click(function() {
    if($("#formularioLogin").css("display")=="none") {
        $("#formularioLogin").slideDown();
    }
    else {
        $("#formularioLogin").slideUp();
    }
});


$('.tituloPeca').blurjs({
	source: 'img',
    radius: 5,
    overlay: 'rgba(255,255,255,0.9)',
    optClass: 'blurred',
    cache: false
});


$( ".peca" ).mouseenter(function() {
    $(this).find("img").css("opacity", "0.8");
    $(this).find(".descricaoPeca h3").css("opacity", "0.3");
    $(this).find(".descricaoPeca h4").css("opacity", "0.3");
    $(this).find(".descricaoPeca p").css("opacity", "0.3");
    $(this).find(".descricaoPeca .dadosPeca").show();
});
$( ".peca" ).mouseleave(function() {
    $(this).find("img").css("opacity", "1");
    $(this).find(".descricaoPeca h3").css("opacity", "1");
    $(this).find(".descricaoPeca h4").css("opacity", "1");
    $(this).find(".descricaoPeca p").css("opacity", "1");
    $(this).find(".dadosPeca").hide();
});


$('#submit').click(function(){
    alert('Cadastro realizado com sucesso!');
    $('#formfield').submit();
});


$( ".meuPerfil a.linkAcessarMenuUsuario" ).click(function() {
    if($("#menuUsuario").css("display")=="none") {
        $("#menuUsuario").slideDown();
    }
    else {
        $("#menuUsuario").slideUp();
    }
});

$( ".meuPerfil a.linkAcessarMenuUsuario" ).click(function() {
    if($("#menuUsuarioComLoja").css("display")=="none") {
        $("#menuUsuarioComLoja").slideDown();
    }
    else {
        $("#menuUsuarioComLoja").slideUp();
    }
});


$( "#buscaAvancada" ).click(function() {
    $("#categoriesBox").show();
});
$(document).ready(function()
{
    $("body").mouseup(function(e)
    {
        var subject = $("#categoriesBox"); 

        if(e.target.id != subject.attr('id') && !subject.has(e.target).length)
        {
            subject.hide();
        }
    });
});



/* Video Home Primeiro Acesso 
$(document).ready(function(){
    if (!getCookie('primeiroAcesso')) {
        $('#slide').show();
    }

    $('#escuro').click(function() {
        $('#principal').show();
        $(this).hide();
        setCookie('primeiroAcesso', true, 1);
    });
    
    $('.sa_lampada').click(function() { 
        $('#principal').hide();
        $('#escuro').show();
    });         
    
});
*/



/*$("form").submit(function(){ DO THE MAGIC HERE });*/

/*$('ul.listaPecas li.peca:nth-child(4n+1)').addClass("first");
$('ul.listaPecas li.peca:nth-child(4n+4)').addClass("last");*/