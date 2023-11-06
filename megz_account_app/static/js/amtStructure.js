var amt = document.getElementsByClassName("amt");

for(var i=0;i<amt.length;i++){
    let x = parseInt(amt[i].innerText);
    let s = x.toLocaleString('hi-IN', {style:"currency", currency:"INR", maximumFractionDigits:0});
    amt[i].innerText=s;
}