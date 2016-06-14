function main(){
document.body.innerHTML='<div id="userbackgound"><div id="downloadurl"><p><strong>Downloadurl ---><strong><span><input type="text" id="downloadurlinput"></span></p></div><div id="offlineurl"><p><strong>Offlineurl ---><strong><span><input type="text" id="offlineurlinput"></span></p></div><div id="submitbtn" onclick="submitinfo()"></div></div><div id="verifycode"><div id="verify"><img src="" id="verifyimg"></div><span><input type="text" id="verifyinput"></span></div>';
getverify()
}
document.addEventListener('DOMContentLoaded',main);

function submitinfo(){
  var durl=document.getElementById("downloadurlinput").value;
  var vcode=document.getElementById('verifyinput').value;
  if(durl.length==0){return;}
  else{
    //初始化ajax
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.open("POST","api/taskcommit",true);
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xmlhttp.send("downloadurl="+durl+"&verifycode="+vcode);
    xmlhttp.onreadystatechange=function(){
      if(xmlhttp.readyState==4&&xmlhttp.status==200){
        document.getElementById("offlineurlinput").value=xmlhttp.responseText;
        getverify()
      }
    }
  }
}
function getverify(){
  var verifycode=new XMLHttpRequest();
  verifycode.open('GET','api/verifycode',true);
  verifycode.send()
  verifycode.onreadystatechange=function(){
    if(verifycode.readyState==4&&verifycode.status==200){
      var verifydiv=document.getElementById('verify');
      while(verifydiv.hasChildNodes()){
        verifydiv.removeChild(verifydiv.firstChild);
      }
      var verifyimg=document.createElement('img');
      verifyimg.id='verifyimg';
      verifyimg.src='/js/'+verifycode.responseText;
      verifydiv.appendChild(verifyimg)
    }
  }
}
