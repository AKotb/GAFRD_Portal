
var collaps = false;
var boltyCollaps = false;
var bayadCollaps = false;
var waqqarCollaps = false;
var lottCollaps = false;
var tho3banCollaps = false;
var redboltyCollaps = false;
var HybridsPennyfishCollaps = false;
var ThechocolateHybridsCollaps = false;
var qaroosCollaps = false;
var gambrysuezCollaps = false;
var gambryqazazCollaps = false;
var gambryyabanyCollaps = false;
var gambryhindiCollaps = false;
var gambryfanmyCollaps = false;
var gambrymiah3azbaCollaps = false;

var fishTypesCollaps = document.getElementById("fishTypesCollaps");
fishTypesCollaps.onclick = function(){
    if (!collaps) {
        document.getElementById("fishTypesCollaps").classList.toggle("active");
        document.getElementById("img-div").style.display = "none";
        document.getElementById("fish-types").style.display = "block";
        document.getElementById("fishTyps").style.height = "100%";
        document.getElementById("fishTypesUl").style.display = "block";
        collaps = true;
    }
    else {
        document.getElementById("fishTypesCollaps").classList.toggle("active");
        document.getElementById("fish-types").style.display = "none";
        document.getElementById("img-div").style.display = "block";
        document.getElementById("fishTyps").style.height = "20%";
        document.getElementById("fishTypesUl").style.display = "none";
        collaps = false;
    }
};

var fishBolty = document.getElementById("fish-bolty");
fishBolty.onclick = function(){
    if (!boltyCollaps) {
        document.getElementById("fish-bolty").classList.toggle("active");
        document.getElementById("fish-types").style.display = "none";
        document.getElementById("fish-types-Bolty").style.display = "block";
        boltyCollaps = true;
    }
    else {
        document.getElementById("fish-bolty").classList.toggle("active");
        document.getElementById("fish-types").style.display = "block";
        document.getElementById("fish-types-Bolty").style.display = "none";
        boltyCollaps = false;
    }
};

var fishBayad = document.getElementById("fish-bayad");
fishBayad.onclick = function(){
    if (!bayadCollaps) {
        document.getElementById("fish-bolty").classList.toggle("active");
        document.getElementById("fish-bayad").classList.toggle("active");
        document.getElementById("fish-types-Bolty").style.display = "none";
        document.getElementById("fish-types").style.display = "none";
        document.getElementById("fish-types-Bayad").style.display = "block";
        bayadCollaps = true;
    }
    else {
        document.getElementById("fish-bolty").classList.toggle("active");
        document.getElementById("fish-bayad").classList.toggle("active");
        document.getElementById("fish-types-Bolty").style.display = "block";
        document.getElementById("fish-types-Bayad").style.display = "none";
        bayadCollaps = false;
    }
};

var fishwaqqar = document.getElementById("fish-waqqar");
fishwaqqar.onclick = function(){
    if (!waqqarCollaps) {
        document.getElementById("fish-waqqar").classList.toggle("active");
        document.getElementById("fish-bolty").classList.toggle("active");
        document.getElementById("fish-bayad").classList.toggle("active");
        document.getElementById("fish-types").classList.toggle("active");
        document.getElementById("fish-types-Bolty").style.display = "none";
        document.getElementById("fish-types-Bayad").style.display = "none";
        document.getElementById("fish-types").style.display = "none";
        document.getElementById("fish-types-waqqar").style.display = "block";
        waqqarCollaps = true;
    }
    else {
        document.getElementById("fish-types").classList.toggle("active");
        document.getElementById("fish-bolty").classList.toggle("active");
        document.getElementById("fish-bayad").classList.toggle("active");
        document.getElementById("fish-waqqar").classList.toggle("active");
        document.getElementById("fish-types").style.display = "block";
        document.getElementById("fish-types-Bolty").style.display = "none";
        document.getElementById("fish-types-Bayad").style.display = "none";
        document.getElementById("fish-types-waqqar").style.display = "none";
        waqqarCollaps = false;
    }
};