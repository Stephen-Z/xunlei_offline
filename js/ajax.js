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
      document.getElementById('verifyimg').src=verifycode.responseText;
    }
  }
}
