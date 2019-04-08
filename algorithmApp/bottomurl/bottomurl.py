import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from utils import file_path, Crawltitle_date


#去除噪声,(li,script,等标签)
def remove_noise(html,noise_file_path):
    doc = pq(html)
    file=open(noise_file_path,encoding='utf-8')
    tag_list=file.readlines()
    file.close()
    for tag in tag_list:
        doc.find(tag).remove()
    htmls = str(doc)
    return htmls

def readtxt(file):
    with open(file,encoding="utf-8") as f:
        Line = []
        line = f.readline()
        while line:
            Line.append(line.strip())
            line = f.readline()
    return Line


def bottomUrl(html,keyWord_list,url):
    if len(keyWord_list) < 1:
        return
    htmls = remove_noise(html, file_path.noise_ad_file)
    soup = BeautifulSoup(htmls, "html.parser")
    a_tags = soup.select("a")
    if "" in keyWord_list:
        keyWord_list.remove("")
    a_href_list = []
    site_name = urlparse(url)
    site_host = site_name.hostname
    # 域名
    site_url = site_name.scheme + "://" + site_host
    not_user_file = file_path.not_user_file
    not_user_url_list = Crawltitle_date.readtxt(not_user_file)
    pattern = re.compile("index.*html$")
    for a_tag in a_tags:
        a_url = a_tag.get("href")
        # 判断是否规范的URL,不规范不需要,不需要一些搜索网站
        if not a_url or len(a_url) < 4:
            continue
        # 如果url 中包含一些特殊词汇或者用不了的无效网站跳过
        flag = False
        for item in not_user_url_list:
            if item in a_url:
                flag = True
                break
        if flag:
            continue
        if not ("http" in a_url):
            # 如果只有没有斜杆表示主页
            if a_url.count("/") < 1:
                continue
            if a_url.startswith('/'):
                a_url = site_url + a_url
            else:
                a_url = site_url + "/" + a_url
        else:
            if a_url.count("/") < 3:
                continue
        # 如果找到的index结尾的url没有斜杆不需要这个url
        result = pattern.findall(a_url)
        if len(result) > 0:
            if result[0].count("/") < 1:
                continue
        a_text = a_tag.get_text()
        if not a_text or len(a_text) < 10:
            continue
        for keyWord in keyWord_list:
            if keyWord in a_text:
                a_href_list.append(a_url)
                break
    if len(a_href_list) < 1:
        return a_href_list
    a_href_list = list(set(a_href_list))
    return a_href_list

if __name__ == '__main__':
    html = """
<script type="text/javascript" src="http://www.qianlima.com/css/newweb/jquery-1.8.3.min.js"></script>
<style type="text/css">
body{position: relative;}
.black_overlay{display: none;position: absolute;top: 0%;left: 0%;width: 100%;height: 100%;background: #bab6b6;_background:none;z-index: 1001;_z-index:-1;-moz-opacity: 0.5;opacity: .50;filter: alpha(opacity = 55);}
.white_content{display: none;position: fixed;_position: absolute;_top: expression(eval(document.documentElement.scrollTop +200));top: 25%;left: 38%;width: 384px;background-color: white;_background-color:none;_z-index:-1;z-index: 1002;font-size: 14px;border-radius: 2px;border: 1px solid #ccc;font-family: "Microsoft YaHei", "SimSun", "sans-serif";}
.white_content p{line-height: 25px;}
#close_zhu{position: absolute;display: block;/*background: url(http://img_al.qianlima.com/newDefault/images/sprite.gif)0 0;*/background:#ccc;color:#fff;font-size:14px;text-align:center;width: 24px;height: 24px;top: 0;right: 0;}
*{padding: 0;list-style: none;border: 0;}
a{cursor: pointer;outline: none;text-decoration: none;}
a:hover{color: #e93100;quotes: none;text-decoration: underline;}
.info-tabs .tabMenu ul li.current, .WanShanMian, .register, .register ul li .text-tel,.WanShanMian ul li .text-tel, .yzmBtn, .WanShanMian ul li .text,.register ul li .text, .finBtn, .finBtn2, .wanshanh2, .finBtn3,.text-code{background-image:url(http://img_al.qianlima.com/newDefault/images/sprite.png);background-repeat: no-repeat;}
.register{background: #fff;width: 384px;height: 341px;padding-top: 25px;margin-left: auto;margin-right: auto;}
.register h2{width: 390px;height: 30px;overflow: hidden;padding-bottom: 25px;color: #333;text-align: center;font-size: 18px;}
.register ul{padding-left: 33px;}
.register ul li{width: 350px;float: left;padding-bottom: 20px;font-family: "Microsoft YaHei", "SimSun", "sans-serif";}
.register ul li .text{padding: 0 9px;background-position: -150px -178px;width: 152px;height: 50px;font-size: 18px;line-height: 50px;border: 0;}
.register ul li .text-tel{background-position: left -118px;border: 0;padding-left: 57px;width: 263px;height: 50px;font-size: 18px;line-height: 50px;}
.register ul li .text-code{background-position: left -414px;border: 0;padding-left: 57px;width: 263px;height: 50px;font-size: 18px;line-height: 50px;}
.register ul li .ac{color: #666;font-size: 12px;}
.register ul li .ac a{color: #666;padding: 0;}
.WanShanMian{background: #fff;width: 384px;padding-top: 45px;margin-left: auto;margin-right: auto;font-family: "SimSun", "sans-serif";}
.WanShanMian h2{width: 390px;height: 30px;overflow: hidden;margin-bottom: 25px;color: #333;text-align: center;font-size: 12px;}
.WanShanMian ul{padding-left: 33px;}
.WanShanMian ul li{width: 330px;float: left;padding-bottom: 20px;}
.WanShanMian ul li .text{padding: 0 9px;background-position: -150px -178px;width: 152px;height: 50px;font-size: 18px;line-height: 50px;border: 0;}
.WanShanMian ul li .text-tel{background-position: left -118px;border: 0;padding-left: 57px;width: 263px;height: 50px;font-size: 18px;line-height: 50px;}
.WanShanMian ul li .ac{color: #666;font-size: 12px;}
.WanShanMian ul li .ac a{color: #666;padding: 0;}
.ac input{vertical-align: middle;margin-right: 5px;}
.yzmBtn{height: 50px;width: 140px;background-position: left -178px;display: inline-block;vertical-align: top;margin-right: 5px;line-height: 50px;text-align: center;color: #D40000;font-size: 18px;font-weight: bold;}
.finBtn{width: 320px;height: 60px;display: block;vertical-align: middle;background-position: left -238px;}
.finBtn2{width: 320px;height: 60px;display: block;vertical-align: middle;background-position: left -41px;}
.tips{color: red;font-size: 12px;padding-top: 5px;}
.tips a{color: #333;}
.institution{padding-top: 30px;width: 1000px;overflow: hidden;margin-right: auto;margin-left: auto;}
.institution h2{font-weight: normal;padding-bottom: 15px;display: block;font-size: 24px;}
.institution ul{width: 1100px;height: 176px;overflow: hidden;}
.institution ul li{width: 190px;height: 78px;border: 1px solid #ccc;background-color: #fff;text-align: center;float: left;margin-right: 10px;margin-bottom: 10px;}
.institution ul li img{display: block;margin: 0 auto;overflow: hidden;}
.register ul li .ac .yideng{padding-left: 20px;*padding-left: 15px;_padding-left: 10px;}
.register ul li .ac .yideng a{color: #900;}
.WanShanMian ul li .ac .yideng{padding-left: 20px;*padding-left: 15px;_padding-left: 10px;}
.WanShanMian ul li .ac .yideng a{color: #900;}
.finBtn3{width: 233px;height: 47px;display: block;vertical-align: middle;background-position: left -306px;margin-left: 93px;}
.tips1{color: red;font-size: 12px;padding-top: 5px;margin-left: 93px;}
.WanShanMian h2.wanshanh2{width: 327px;height: 47px;background-position: left -359px;margin-left: 26px;}
.wanshanname{display: block;width: 88px;height: 30px;line-height: 30px;text-align: right;font-size: 12px;padding-right: 5px;float: left;color: #900;}
#WS_email, #WS_company{width: 228px;height: 30px;line-height: 30px;padding-left: 5px;border: 1px solid #ccc;float: left;color: #666;}
.WanShanMian ul.wanshan{padding-left: 3px;}
#WS_keyword1, #WS_keyword2, #WS_keyword3{dispaly: block;width: 68px;height: 25px;line-height: 25px;border: 1px solid #ccc;color: #666;padding-left: 3px;}
#WS_keyword1, #WS_keyword2{margin-right: 2px;}
#key_tishi{color: #9c9797;}
.zhiwei{padding-left: 5px;color: #900;}
.zhiwei, .wanshanname{padding-right: 3px;font-size: 12px;display: block;height: 30px;line-height: 30px;float: left;}
#WS_zhiwei, #WS_username{width: 88px;height: 30px;line-height: 30px;padding-left: 5px;border: 1px solid #ccc;float: left;color: #666;float: left;}
#submitBlock{cursor: pointer;}
.content11{_display:none;}
</style>
<script type="text/javascript" src="http://www.qianlima.com/seo/js/jquery.min.js"></script>


<script type="text/javascript">
	var xmlhttp = new XMLHttpRequest();
	var mobileFlag = "";
	var codeFlag = "";

	var emailFlag = "";
	var companyFlag = "";
	var usernameFlag = "";
	var zhiweiFlag = "";
	var kwFlag = "";
	var ks_closezhuFlag = false;
	//get validateCode
	
  
function changeStatus() {
  
  var   temp454   =   document.form1.email.value.indexOf('@'); 
  var   temp4543   =   document.form1.email.value.indexOf('.'); 
	if(document.form1.mail.value=="")
  {
    alert('请输入电子邮箱');
	document.form1.email.focus();
	
  }
  if(temp454==-1||temp4543==-1){
  	
  	alert('电子邮箱的格式不正确');
		document.form1.email.focus();
		return false;
  			
  	}
}
function changeStatus() {
		document.getElementById('code-info').innerHTML = " ";
		//获取页面的出处
		var registtype = document.getElementById('registtype').value;
		//alert("获取验证码") ;
		var tu = document.getElementById("getcode");
		var Num = "";
		for (var i = 0; i < 6; i++) {
			Num += Math.floor(Math.random() * 10);
		}
		//	alert(tu.value) ;
		var mobile = document.getElementById("T-mobile").value;
var re = /(^1[3|4|5|7|8|9][0-9]{9}$)/;

		if (!re.test(mobile)) {
			document.getElementById("T-error-info").innerHTML = "请填写正确的手机号码";
			//alert("请填写正确的手机号码");
			return;
		}

		if (!(/^1[3|4|5|7|8|9][0-9]\d{4,8}$/.test(mobile))) {
			//alert("不是完整的11位手机号或者正确的手机号前七位");   
			document.getElementById("T-error-info").innerHTML = "请填写正确的手机号码";
			//alert("请填写正确的手机号码");
			return;
		}
		mobileFlag = "true";
		//点击获取验证码时，验证手机是否注册过。\
		xmlhttp.open("post", "http://www.qianlima.com:80/common/mobileValidate.jsp?type=1&mobile=" + mobile,
				false);
		xmlhttp.setRequestHeader("Content-Type", "text/html;charset=GBK");
		xmlhttp.send();
		if (xmlhttp.readyState == 4) {
			 var rtn =JSON.parse(xmlhttp.responseText)
			
			//alert(rtn.isHas);
			if (rtn.isHas == 1) {//注册过
				//document.getElementById("T-error-info").innerHTML="该用户名已经注册，请直接<a href='login.jsp?regStatus=phone' >登录</a>" ;
				document.getElementById("T-error-info").innerHTML = "该用户名已经注册，请直接登录";
				document.getElementById("codeBlock").style.display = "none";
				document.getElementById("submitBlock").className = "finBtn2";//登录图片
				document.getElementById("pwdBlock").style.display = "";//登录图片
				document.getElementById("status").value = 2;
				document.getElementById("yiyouyonghu").style.display = 'none';
				document.getElementById("xinzhuce").style.display = 'inline';
				return;
				//alert("##444") ;
			}
		}
		if (tu.value == "获取验证码" || tu.value == "立即重发") {
			document.getElementById("T-error-info").innerHTML = "验证码已发送，如未正常收到，请点击重新发送";
			var codeTip;
			if (tu.value == "获取验证码") {
				codeTip = 1;
			} else if (tu.value == "立即重发") {
				codeTip = 2;
			}

			xmlhttp.open("get", "http://www.qianlima.com:80/common/saveCodeNew.jsp?num=" + Num + "&type=1&tips="
					+ codeTip + "&mobile=" + mobile + "&registtype="
					+ registtype, false);
			xmlhttp.send();
			if (xmlhttp.readyState == 4) {
				var rtn = xmlhttp.responseText;
				//alert(rtn) ;
				if (rtn == 1) {//短信发送过多
					alert("您在10分内注册太频繁了，请10分钟后重试。");
					return;
				}
				if (rtn == 2) {
					alert("ip访问受到限制，请明天再来.");
					return;
				}
			}
			//tu.innerHTML="<span>48</span>秒后重新发送" ;//倒计时
			document.getElementById("getcode").disabled = true;
			document.getElementById("getcode").style.color = "silver";
			tu.value = "60秒后重新发送"

			var i = 60;
			timeInterval = setInterval(function() {
				i--;
				document.getElementById("getcode").value = i + "秒后重新发送";
				if (i == 0) {
					clearTime();
					document.getElementById("getcode").disabled = false;
					document.getElementById("getcode").value = "立即重发";
					document.getElementById("getcode").style.color = "crimson";
				}
			}, 1000);
		} else {
			//tu.innerHTML="获取验证码" ;
			tu.value = "获取验证码";
		}
	}

	function clearTime() {
		clearInterval(timeInterval);
	}



	function onLoadPopStyle() {

		var cookieUserid = document.getElementById("cookieUserid").value;
		var ziliaoFlag = document.getElementById("ziliaoFlag").value;

		if (cookieUserid > 0) {//登录
			//alert("已登录") ;
			if (ziliaoFlag == "false") {
				//alert("未完善资料....") ;
				document.getElementById('light').style.display = 'block';
				document.getElementById('fade').style.display = 'block';
				document.getElementById('regStatus').style.display = 'none';
				document.getElementById('wanshanStatus').style.display = '';//完善资料
				var kwf = document.getElementById('keywordFlag').value;
				//alert(kwf);
				if (kwf > 0) {
					document.getElementById('keywords').style.display = 'none';
				}
			}

		}
	}

	//弹出层
	function popStyle(registtype) {
		//alert("弹出层~！！！ 哈哈")
		if(ks_closezhuFlag){
			return;
		}
		if(typeof(registtype)!="undefined" && registtype!=""){
			document.getElementById('registtype').value = registtype;
		}
		var cookieUserid = document.getElementById("cookieUserid").value;
		var ziliaoFlag = document.getElementById("ziliaoFlag").value;

		//alert(cookieUserid) ;
		//alert(ziliaoFlag) ;
		if (cookieUserid > 0) {//登录
			
			//alert("已登录") ;
			if (ziliaoFlag == "false") {
			//alert("未完善资料....") ;
				document.getElementById('light').style.display = 'block';
				document.getElementById('fade').style.display = 'block'
				document.getElementById('regStatus').style.display = 'none'
				document.getElementById('wanshanStatus').style.display = '';//完善资料
				var kwf = document.getElementById('keywordFlag').value;
				//alert(kwf);
				if (kwf > 0) {
					document.getElementById('keywords').style.display = 'none';
				}
			}
		} else {//未登录
			//alert("未登录") ;
			document.getElementById('light').style.display = 'block';
			document.getElementById('fade').style.display = 'block';
			document.getElementById('xinzhuce').style.display = 'none';
			xmlhttp.open("get", "http://www.qianlima.com:80/common/saveCodeNew.jsp?type=5&registtype="+registtype ,true);
			xmlhttp.setRequestHeader("Content-Type", "text/html;charset=GBK");
			xmlhttp.send();
		}
	}
	
	//点击地下免费注册
	function popStyle2(registtype) {
		ks_closezhuFlag = false;
		popStyle(registtype);
	}
	

	//validate Code
	function checkCode(code) {
		var mobile = document.getElementById("T-mobile").value;
		if (code == '') {
			document.getElementById("code-info").value = '请填写手机收到的验证码';
		} else if (code.indexOf("验证码")==-1) {
			xmlhttp.open("post", "http://www.qianlima.com:80/common/mobileValidate.jsp?type=2&mobile=" + mobile
					+ "&inputcode=" + code, false);
			xmlhttp.setRequestHeader("Content-Type", "text/html;charset=GBK");
			xmlhttp.send();
			if (xmlhttp.readyState == 4) {

				var rtn = xmlhttp.responseText;
				if (rtn == 1) {//验证码错误
					document.getElementById("code-info").innerHTML = "验证码错误，请输入正确的验证码";
					codeFlag = "false";
					return;
				} else if (rtn == 2) {//验证码超时
					document.getElementById("code-info").innerHTML = "验证码超时,请重新获取";
					codeFlag = "false";
					return;
				} else {
					codeFlag = "true";
				}
			}
		}else{
			document.getElementById("code-info").value = '请填写手机收到的验证码！';
		}
	}
	
	function ks_checkSubmit() {
		//通过手机号开始注册
		//alert("开始。。。手机号走起。。。")
		var p = document.getElementById("status").value; //1注册	 2登录
		var mobile = document.getElementById("T-mobile").value;
		var redirectPath =  document.getElementById("urlPath").value;
		var pattern = /\s/;
		/*新添的*/
		var re_ = /(^1[3|4|5|6|7|8|9][0-9]{9}$)/;

		if (!re_.test(mobile)) {
			document.getElementById("T-error-info").innerHTML = "请填写正确的手机号码";
			//alert("请填写正确的手机号码");
			return false;
		}

		if (!(/^1[3|4|5|6|7|8|9][0-9]\d{4,8}$/.test(mobile))) {
			//alert("不是完整的11位手机号或者正确的手机号前七位");   
			document.getElementById("T-error-info").innerHTML = "请填写正确的手机号码";
			//alert("请填写正确的手机号码");
			return false;
		}
		mobileFlag = "true";
		
		
	//	alert("判断是否注册过");
		if (p == 1) {
			
		//点击获取验证码时，验证手机是否注册过。\
		
		$.ajax({
			url:"http://www.qianlima.com/seo/mobileValidate.jsp?type=1&mobile="+mobile,
			type:'post',
			success:function(msg){
				
				if (msg == 1) {//注册过
					//document.getElementById("T-error-info").innerHTML="该用户名已经注册，请直接<a href='login.jsp?regStatus=phone' >登录</a>" ;
					document.getElementById("T-error-info").innerHTML = "该用户名已经注册，请直接登录";
					document.getElementById("codeBlock").style.display = "none";
					document.getElementById("submitBlock").className = "finBtn2";//登录图片
					document.getElementById("pwdBlock").style.display = "";//登录图片
					document.getElementById("status").value = 2;
					document.getElementById("yiyouyonghu").style.display = 'none';
					document.getElementById("xinzhuce").style.display = 'inline';
					return false;
					//alert("##444") ;
				}
			}
		});
		
		/**/
			//alert("check  : "+ "验证码进行校验。。。。");
			var code = document.getElementById("validateCode").value;
			checkCode(code);
			//alert("code  : "+ code);
			if(codeFlag == "false"){
				return false;
			}
			if (codeFlag == "true" && mobileFlag == "true") {
				xmlhttp.open("post", "http://www.qianlima.com:80/common/saveCodeNew.jsp?type=2&mobile=" + mobile+"&code="+code,false);
				xmlhttp.setRequestHeader("Content-Type","text/html;charset=GBK");
				xmlhttp.send();
				if (xmlhttp.readyState == 4) {
					//alert("2222");
					var rtn = xmlhttp.responseText;
				//	var pattern = /^[0-9]+/;
					rtn=rtn.trim();
					//var flag = pattern.test(rtn); //全数字表明是userid
				//	alert(rtn);
					if (rtn == "ok") {
						wanshanSubmit();
						//document.getElementById('light').style.display = 'block';
						//document.getElementById('fade').style.display = 'block';
						//document.getElementById('regStatus').style.display = 'none';
						//document.getElementById('wanshanStatus').style.display = '';//完善资料
						//baidutj();
						
					} else {
						document.getElementById("T-error-info").innerHTML = "注册失败，请检查填写内容，重新注册，谢谢！";
					}
				} else {
					document.getElementById("T-error-info").innerHTML = "内部错误，请重新提交， 谢谢！";
				}
				return false;
			} else {
				if (mobileFlag != "true") {
					document.getElementById('T-error-info').innerHTML = "请输入正确的手机号，并获取验证码";
				}else{
					document.getElementById('T-error-info').innerHTML ="";
				}
				return false;
			}
		
		} else {//注册过，直接登录
			alert("注册过，直接登录");
			if (mobileFlag == "true" && codeFlag == "") {
				var pwd = document.getElementById("T-code").value;
				xmlhttp.open("post", "http://www.qianlima.com:80/common/saveCodeNew.jsp?type=4&mobile=" + mobile
						+ "&pwd=" + pwd + "&redirectPath=" + redirectPath,
						false);
				xmlhttp.setRequestHeader("Content-Type",
						"text/html;charset=GBK");
				xmlhttp.send();
				if (xmlhttp.readyState == 4) {
					var rtn = xmlhttp.responseText;
					if (rtn == 1) {
						location.reload();
					} else {
						document.getElementById("pwd-error-info").innerHTML = "密码输入错误，请重新输入";
						document.getElementById("T-code").value = "";
						document.getElementById("T-error-info").value = "";
					}
				} else {
					document.getElementById("pwd-error-info").innerHTML = "内部错误，请重新提交， 谢谢！";
				}
			}
		}
		
		return false;
	}

	function wanshanSubmit() {
		//alert("开始走注册手机号代码。。。");
		
		//alert("注册手机号代码结束。。。准备走完善资料程序。。。");
		var cookieUserName = document.getElementById("T-mobile").value;
		//alert("cookieUserName : "+cookieUserName);
		var urlPath = document.getElementById("urlPath").value;
		//alert("urlPath : "+urlPath);
		var WS_email = document.getElementById("WS_email").value;
		//alert("WS_email : "+WS_email);
		var WS_company = document.getElementById("WS_company").value;
		//alert("WS_company : "+WS_company);
		var WS_username = document.getElementById("WS_username").value;
		//alert("WS_username : "+WS_username);
		var WS_zhiwei = document.getElementById("WS_zhiwei").value;
		//alert("cookieUserName : "+cookieUserName);
		var userid = document.getElementById("userid").value;
		//alert("userid   : "+userid);
		var validate = "请输入";
		
		var pattern = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
		var pattern2 = /\s/;
		flag = pattern.test(WS_email); //邮箱
		if (flag) {
			emailFlag = "true";
			document.getElementById("wanshanEmail").innerHTML = "";
		} else {
			document.getElementById("WS_email").value = "";
			document.getElementById("wanshanEmail").innerHTML = "请输入正确的邮箱";
			emailFlag = "false";
		}

		if (WS_company == null || WS_company == "" || pattern2.test(WS_company)
				|| WS_company.indexOf(validate) != -1) {
			companyFlag = "false";
			document.getElementById("wanshanCompany").innerHTML = "请输入公司名称";
			document.getElementById("WS_company").value = "";
		} else {
			companyFlag = "true";
			document.getElementById("wanshanCompany").innerHTML = "";
		}

		if (WS_username == null || WS_username == "" || pattern2.test(WS_username)
				|| WS_username.indexOf(validate) != -1) {
			usernameFlag = "false";
			document.getElementById("wanshanLxr").innerHTML = "请输入联系人";
			document.getElementById("WS_username").value = "";
		} else {
			usernameFlag = "true";
		}
		if (WS_zhiwei == null || WS_zhiwei == "" || pattern2.test(WS_zhiwei)
				|| WS_zhiwei.indexOf(validate) != -1) {
			zhiweiFlag = "false";
			document.getElementById("wanshanLxr").innerHTML = "请输入职位";
			document.getElementById("WS_zhiwei").value = "";
		} else {
			zhiweiFlag = "true";
		}
		if (usernameFlag == "true" && zhiweiFlag == "true") {
			document.getElementById("wanshanLxr").innerHTML = "";
		}
		/* var kwf = document.getElementById('keywordFlag').value;
		//alert(kwf);
		if (kwf > 0) {
			kwFlag = "true";
			document.getElementById('keywords').style.display = 'none';
		} else {
			if((null == WS_kw1 || "" == WS_kw1)&&(null == WS_kw2 || "" == WS_kw2)&&(null == WS_kw3 || "" == WS_kw3)){
				document.getElementById("key_error").innerHTML = "请填写您想关注的产品关键词！";
				document.getElementById("WS_keyword1").value="关键词一";
				kwFlag = "false";
			}else{
				if(WS_kw1=="关键词一" && WS_kw2=="关键词二" && WS_kw3=="关键词三"){
					document.getElementById("key_error").innerHTML = "请填写您想关注的产品关键词！";
					document.getElementById("WS_keyword1").value="关键词一";
					kwFlag = "false";
				}else{
					if(WS_kw1=="关键词一" ){
						WS_kw1="";
					}
					if(WS_kw2=="关键词二"){
						WS_kw2="";
					}
					if(WS_kw3=="关键词三"){
						WS_kw3="";
					}
					kwFlag = "true";
				}
			}
		} */
		//alert("判断结束、、、");
		//alert(emailFlag);alert(companyFlag);alert(zhiweiFlag);alert(usernameFlag);
		if (emailFlag == "true" && companyFlag == "true"
			&& usernameFlag == "true" && zhiweiFlag == "true"
			) {
			//String email = request.getParameter("email");
			//String company = request.getParameter("company");
			//String lxr = request.getParameter("username");
			//String zw = request.getParameter("zhiwei");
			//String redirectPath = request.getParameter("urlPath");
			//String keywordFlag = request.getParameter("keyword");
			//String userid = request.getParameter("userid");
			//window.location.href ="saveCode.jsp?type=3&mobile="+cookieUserName+"&WS_email="+WS_email+"&WS_company="+WS_company+"&WS_username="+WS_username+"&urlPath="+urlPath+"&WS_zhiwei="+WS_zhiwei ;
			document.getElementById("registLogin2").action = "http://www.qianlima.com/seo/saveCodeNew.jsp?type=3&mobile="+cookieUserName+"&email="+WS_email+"&company="+WS_company+"&username="+WS_username+"&urlPath="+urlPath+"&zhiwei="+WS_zhiwei+"&userid="+userid ;
			document.getElementById("registLogin2").submit();
		}
	}

	//当点击新注册后显示注册框
	function xinzhuce() {
		document.getElementById("T-error-info").innerHTML = "";
		document.getElementById("codeBlock").style.display = "block";
		document.getElementById("kw_tijiao").className = "finBtn";//登录图片
		document.getElementById("pwdBlock").style.display = "none";//登录图片
		document.getElementById("status").value = 1;
		document.getElementById("yiyouyonghu").style.display = 'inline';
		document.getElementById("xinzhuce").style.display = 'none';
		document.getElementById("getcode").disabled = false;
	}
	
	//点击叉后的事件
	function ks_closepopup(){
		document.getElementById('light').style.display='none';
		document.getElementById('fade').style.display='none';
		//ks_closezhuFlag = true;
	}
	//百度统计
	function baidutj(){
		var xmlhttp1 = new XMLHttpRequest();
		xmlhttp1.open("get", "http://www.qianlima.com/new/baidu_tongji.jsp",true);
		xmlhttp1.setRequestHeader("Content-Type","text/html;charset=GBK");
		xmlhttp1.send();
	}
</script>
 

<style>
	.info-tabs .tabMenu ul li.current, .WanShanMian, .register, .register ul li .text-tel, .WanShanMian ul li .text-tel, .yzmBtn, .WanShanMian ul li .text, .register ul li .text, .finBtn, .finBtn2, .wanshanh2, .finBtn3, .text-code{
		background-image:none;
	}
	.register ul li .text-tel{
		/* background-position: left -118px; */
		border: 0;
		/* padding-left: 57px; */
		width: 150px;
		height: 30px;
		font-size: 18px;
		line-height: 18px;
		border: 1px solid #ccc;
		font-size: 15px;
		padding: 6px;
		color: gray;
	}
	.yzmBtn{
		height: 30px;
		width: 92px;
		/* background-position: left -178px; */
		display: inline-block;
		vertical-align: top;
		margin-right: 5px;
		line-height: 30px;
		text-align: center;
		background: #ef1901;
		font-size: 15px;
		color: #fff;
		font-weight: 400;
	}
	.register ul li .text{
		padding-left: 8px;
		/* background-position: -150px -178px; */
		width: 152px;
		height: 30px;
		font-size: 14px;
		line-height: 30px;
		border: 0;
		color: gray;
		border: 1px solid #ccc;
	}
	.finBtn3{
	
		width: 251px;
		height: 37px;
		display: block;
		vertical-align: middle;
		/* background-position: left -306px; */
		margin-left:40px;
		background-color: #ef1901;
		color:#fff;
		font-size:18px;
	}
	.white_content{
		width:500px;
	}
	.tips{
		margin-left:86px;
	}
</style>
<div class="content11">
  <div id="light" class="white_content" style="_display:none;"><!-- 白色弹出层 -->
  <form method="post" id="registLogin2"  action="">
         <div class="register" id="regStatus">
      <h2>免费注册，即可查看全国免费招标项目</h2>
       <ul>
		 <li class="wanshanli">
	         	<span class="wanshanname">公司名称：</span>
	         	<input id="WS_company" title="公司名称" type="text" name="company" class="wanshanC" value="" onfocus="if (value ==&#39;请输入公司名称&#39;){value =&#39;&#39;}" onblur="if (value ==&#39;&#39;){value=&#39;请输入公司名称&#39;}">
	         	<div class="tips1" id="wanshanCompany"></div> 
	     </li>
		 <li class="wanshanli">
	         	<span class="wanshanname">电子邮箱：</span>
	         	<input id="WS_email" title="邮箱" type="text" name="email" class="wanshanE" value="" onfocus="if (value ==&#39;请输入邮箱&#39;){value =&#39;&#39;}" onblur="if (value ==&#39;&#39;){value=&#39;请输入邮箱&#39;}">
	         		<div class="tips1" id="wanshanEmail"></div>
	     </li>
		 <li class="wanshanli">
	          <span class="wanshanname">联&nbsp;系&nbsp;人：</span>
	          <input id="WS_username" title="联系人" type="text" name="username" class="wanshanU" value="" onfocus="if (value ==&#39;请输入联系人&#39;){value =&#39;&#39;}" onblur="if (value ==&#39;&#39;){value=&#39;请输入联系人&#39;}">
	          <span class="zhiwei">职位：</span>
	          <input id="WS_zhiwei" title="职位" type="text" name="zhiwei" class="wanshanU" value="" onfocus="if (value ==&#39;请输入职位&#39;){value =&#39;&#39;}" onblur="if (value ==&#39;&#39;){value=&#39;请输入职位&#39;}">
	          <div style="clear:both;"></div>
	        	 <div class="tips1" id="wanshanLxr"></div> 
	     </li>
         <li>
         <!-- 
         	<input id="T-mobile" title="手机号码" type="text" name="mobile" class="text-tel"  value="请输入您的手机号" onfocus="if (value =='请输入您的手机号'){value =''}" onblur="checkMobile()"/>
         	 -->
			 <span class="wanshanname">手机号码：</span>
         	<input id="T-mobile" title="手机号码" type="text" name="mobile" class="text-tel" value="" onfocus="if (value ==&#39;请输入您的手机号&#39;){value =&#39;&#39;}" onblur="if (value ==&#39;&#39;){value =&#39;请输入您的手机号&#39;}">
	         <input type="button" id="getcode" class="yzmBtn" onclick="changeStatus()" value="获取验证码">
			 <div class="tips" id="T-error-info">
	         <!-- 该用户名已经注册，请<a href="#" target="_blank">登录</a>-->
	         </div>
         </li>
         
        <li id="pwdBlock" style="display:none">
	       	<input id="T-code" title="密码" type="text" name="code" class="text-code" value="请输入您的登陆密码" onblur="if(!value) {value=defaultValue; this.type=&#39;text&#39;;}" onfocus="if(this.value==defaultValue) {this.value=&#39;&#39;;this.type=&#39;password&#39;}">
	       	<div class="tips" id="pwd-error-info"></div>
	       	<!-- <div class="tips" id="T-error-info">密码错误，请重新输入</div> -->
       	</li>
         
         <li id="codeBlock">
         	
	         <!--  <a href="javascript:void(0);" id="getcode" class="yzmBtn" onclick="changeStatus()">获取验证码</a> 
	          -->
	          <!--<a id="getcode" class="yzmBtn"><span>48</span>秒后重新发送</a>
	          -->  
			  <span class="wanshanname">验&nbsp;证&nbsp;码：</span>
	           <input id="validateCode" name="mobilecode" title="验证码" type="text" tip="输入验证码" class="text" value="" onfocus="if (value ==&#39;输入验证码&#39;){value =&#39;&#39;}" onblur="if (value ==&#39;&#39;){value =&#39;输入验证码&#39;}">
	           
	    
	           <div class="tips" id="code-info"></div> 
         </li>
         
	         
	        
	         	
	          
	          	
	      <!--   <li class="wanshanli" id="keywords">
	          <span class="wanshanname">关&nbsp;键&nbsp;词：</span>
	          <input id="WS_keyword1" title="关键词一" type="text" name="kw1" class="wanshanU"  value="关键词一" onfocus="if (value =='关键词一'){value =''}" onblur="if (value ==''){value='关键词一'}" >
	          <input id="WS_keyword2" title="关键词二" type="text" name="kw2" class="wanshanU"  value="关键词二" onfocus="if (value =='关键词二'){value =''}" onblur="if (value ==''){value='关键词二'}" >
	          <input id="WS_keyword3" title="关键词三" type="text" name="kw3" class="wanshanU"  value="关键词三" onfocus="if (value =='关键词三'){value =''}" onblur="if (value ==''){value='关键词三'}" >
	          <div class="tips1" id="key_error"></div> 
	          <div class="tips1" id="key_tishi">填写您所关注的产品关键词，以便我们将优质招标、项目及时发送至您的邮箱。</div> 
	          </li> -->
	         <li>
	         <!--  <a href="#" class="finBtn3" value="--=-="></a> -->
	         <input id="wsSubmitBlock" type="button" class="finBtn3" value="提交注册>>" onclick="ks_checkSubmit()">
	         </li>
      
         <input type="hidden" value="1" id="status"><!-- 1:注册  2:登录-->
         <input type="hidden" value="0" id="cookieUserid">
         <input type="hidden" value="" id="cookieUserName">
         <input type="hidden" value="false" id="ziliaoFlag">
         <input type="hidden" value="http://www.qianlima.com/caizhao_24523/" id="urlPath">
         <input id="registtype" type="hidden" value="10">    <!-- 注册来源，来自哪个注册页 -->
         <li><p class="ac">
         	<input name="agree" title="用户服务条款" type="checkbox" id="agree" checked="checked">我同意接受网站<a href="http://my.qianlima.com/register_xz.jsp" id="serveTerms_dialog">《用户服务条款》</a>
         	<input type="checkbox" name="hasmail" value="1" id="protocol1" tabindex="10" checked="checked"/><label for="protocol" style=" line-height:14px;">同意接收项目信息邮件</label>
         	<span style="margin-right: -39px;float: right;">已有账号，<a style="line-height:14px;" href="http://center.qianlima.com/login.jsp" target="_blank"><font color="red">登录>></font></a></span>
         	&nbsp;&nbsp;&nbsp;
         	 <span id="xinzhuce" style="display: none;"><a href="Javascript:xinzhuce()" style="display: none;color:#8E3331;">没有账号？立即注册</a></span> 
         </p></li></ul>
       <a href = "javascript:void(0)" onclick = "document.getElementById('light').style.display='none';document.getElementById('fade').style.display='none'" id="close_zhu">X</a>
   </div>
  </form>
  
 
 
            </div> 
                <div id="fade" class="black_overlay" style="_display:none;"></div><!-- 黑色背景 --> 
         </div>
         
		 <script type="text/javascript">
	         var click = 0;
	         document.onclick = function () {
	           click = 1;
	         }
	         document.onmousemove = function () {
	           click = 2;
	         }
	         document.onkeydown = function () {
	           click = 3;
	         }
	         document.onscroll = function () {
	           click = 4;
	         }
	         var timer =  setTimeout(function () {
	           if (click!==1 && click!==2 && click!==3 && click!==4) {
	        	   document.getElementById('light').style.display='none';
	        	   document.getElementById('fade').style.display='none';
	           }
	         },10000)
         </script>



<input type="hidden" id="isFlag" value="1" />
<script type='text/javascript'>
 var c = document.getElementById("isFlag").value;
    if(c == 2){
     setTimeout("popStyle(10)",5000);
    }
</script>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>热烈庆祝北京科技大学、千里马产学研合作基地正式授牌成立！ - 千里马招标网 - zb.qianlima.com</title>
<link href="/css/qlm_zb.css" rel="stylesheet" type="text/css">
<link href="/css/base.css" rel="stylesheet" type="text/css">

<style>
.black_overlay {
   background: #000;
    opacity: 0.5;
}
</style>
</head>

<body class="qwe">






<script type="text/javascript" src="http://cbjs.baidu.com/js/m.js"></script><script language=javascript src="http://www.qianlima.com/images/gg.js"></script><table width="960" border="0" align="center" cellpadding="0" cellspacing="0">  <tr>    <td align="center" bgcolor="#f4f4f4"><table width="99%"  border="0" cellspacing="0" cellpadding="0">      <tr>        <td width="33%" align="left"><table width="100%"  border="0" cellspacing="0" cellpadding="0">          <tr align="left">            <td width="100%"><iframe src=http://www.qianlima.com/common/top_login.jsp name=top_login width=100% smarginwidth=0 height=20 marginheight=0 scrolling=no frameborder=0 id=cart></iframe></td>          </tr>        </table></td>        <td width="67%" align="right"><span style="color: #FF0000"><b>分站：</b></span><a target=_blank href=http://www.qianlima.com/zb/area_2/>北京</a> <a target=_blank href=http://www.qianlima.com/zb/area_5/>广东</a> <a target=_blank href=http://www.qianlima.com/zb/area_6/>广西</a> <a target=_blank href=http://www.qianlima.com/zb/area_9/>河北</a> <a target=_blank href=http://www.qianlima.com/zb/area_10/>河南</a> <a target=_blank href=http://www.qianlima.com/zb/area_12/>湖北</a> <script language="javascript">var pagewidth=-400;</script> <script language="JavaScript" src="http://img.qianlima.com/index.js"></script> <script language="JavaScript" src="http://img.qianlima.com/index1.js"></script> <script language="javascript" src="http://img.qianlima.com/a_20051231.js" type="text/javascript"></script> <script language="javascript" src="http://img.qianlima.com/b_20051231.js" type="text/javascript"></script> <script language="javascript" src="http://img.qianlima.com/c_20051231.js" type="text/javascript"></script> <STYLE>.n2Pop{border: 0px outset #EEEDDD;background:#fff;position:absolute;margin-left:-435px;margin-top:-18px;}.allexam{width:400px;border:1px solid #af7205;padding:4px;background:#fff;}.animatedBox{position:absolute;visibility:hidden;border:1px solid gray;background:white;}.animatedBoxHollow{position:absolute;visibility:hidden;border:1px solid gray;}</STYLE><STYLE>.allss{position:absolute;margin-left:-450px;width:320px;border:1px solid #af7205;padding:4px;background:#fff;}</STYLE>          [<a href=http://www.qianlima.com/common/zb_all_area.qlm name=two-tabs|he|allss><font color=#FF0000><b>更多</b></font></a>] </td>      </tr>    </table></td>  </tr></table><div class=allss id=allss style="DISPLAY: none"><div class=allss><table width="325"  border="0" cellspacing="0" cellpadding="0">              <tr>                <td width="21%" height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华北</td>                <td width="79%" align="left">[<a href="http://www.qianlima.com/zb/area_2/" class="blue121">北京</a>] [<a href="http://www.qianlima.com/zb/area_26/" class="blue121">天津</a>] [<a href="http://www.qianlima.com/zb/area_9/" class="blue121">河北</a>] [<a href="http://www.qianlima.com/zb/area_22/" class="blue121">山西</a>] [<a href="http://www.qianlima.com/zb/area_18/" class="blue121">内蒙古</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;东北</td>                <td align="left">[<a href="http://www.qianlima.com/zb/area_14/" class="blue121">吉林</a>] [<a href="http://www.qianlima.com/zb/area_17/" class="blue121">辽宁</a>] [<a href="http://www.qianlima.com/zb/area_11/" class="blue121">黑龙江</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;西北</td>                <td align="left">[<a href="http://www.qianlima.com/zb/area_23/" class="blue121">陕西</a>] [<a href="http://www.qianlima.com/zb/area_4/" class="blue121">甘肃</a>] [<a href="http://www.qianlima.com/zb/area_19/" class="blue121">宁夏</a>] [<a href="http://www.qianlima.com/zb/area_20/" class="blue121">青海</a>] [<a href="http://www.qianlima.com/zb/area_28/" class="blue121">新疆</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华东</td>                <td align="left">[<a href="http://www.qianlima.com/zb/area_21/" class="blue121">山东</a>] [<a href="http://www.qianlima.com/zb/area_1/" class="blue121">安徽</a>] [<a href="http://www.qianlima.com/zb/area_24/" class="blue121">上海</a>] [<a href="http://www.qianlima.com/zb/area_15/" class="blue121">江苏</a>] [<a href="http://www.qianlima.com/zb/area_30/" class="blue121">浙江</a>] [<a href="http://www.qianlima.com/zb/area_3/" class="blue121">福建</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华中</td>                <td align="left">[<a href="http://www.qianlima.com/zb/area_10/" class="blue121">河南</a>] [<a href="http://www.qianlima.com/zb/area_12/" class="blue121">湖北</a>] [<a href="http://www.qianlima.com/zb/area_13/" class="blue121">湖南</a>] [<a href="http://www.qianlima.com/zb/area_16/" class="blue121">江西</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华南</td>                <td align="left">[<a href="http://www.qianlima.com/zb/area_5/" class="blue121">广东</a>] [<a href="http://www.qianlima.com/zb/area_6/" class="blue121">广西</a>] [<a href="http://www.qianlima.com/zb/area_8/" class="blue121">海南</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;西南</td>                <td align="left">[<a href="http://www.qianlima.com/zb/area_29/" class="blue121">云南</a>] [<a href="http://www.qianlima.com/zb/area_7/" class="blue121">贵州</a>] [<a href="http://www.qianlima.com/zb/area_25/" class="blue121">四川</a>] [<a href="http://www.qianlima.com/zb/area_31/" class="blue121">重庆</a>] [<a href="http://www.qianlima.com/zb/area_27/" class="blue121">西藏</a>]</td>              </tr>          </table></div></div>



<table width="960" border="0" align="center" cellpadding="0" cellspacing="0">  <tr>    <td height="1" bgcolor="#cccccc"></td>  </tr></table><table width="960" height="90" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">  <tr>    <td width="209" align="center"><a href="http://www.qianlima.com/"><img src="http://img.qianlima.com/qlm_sj.gif" border="0"></a></td>    <td width="575" align="left"><table width="570" border="0" cellspacing="0" cellpadding="0">      <tr>        <td width="10"><img src="http://img.qianlima.com/20100709/bg.gif" width="10" height="28"></td>        <td width="653" align="center" valign="bottom"><table width="100%"  border="0" cellpadding="0" cellspacing="0" background="http://img.qianlima.com/20100709/bg_1.gif">          <tr>            <td width="7%" height="28">&nbsp;</td>            <td width="17%" align="center" background="http://img.qianlima.com/20100709/bg_2.gif" class="tu"><span style="font-size:14px"><strong>全文检索</strong></span></td>            <td width="74%" align="left" background="http://img.qianlima.com/20100709/bg_7.gif" class="tu"><table width="95%" border="0" cellpadding="0" cellspacing="0">              <tr>                <td width="8%" align="center"><img src="http://img.qianlima.com/20100709/d5.jpg" width="19" height="16"></td>                <td align="left"><span style="font-size:12px; color:#FF0000 ">热门搜索：</span> <a href="http://search.qianlima.com/search.jsp?q=%B5%F1%CB%DC" class="blue121" rel="nofollow">雕塑</a>&nbsp;                  <a href="http://search.qianlima.com/search.jsp?q=%B1%C3" class="blue121" rel="nofollow">泵</a>&nbsp; <a href="http://search.qianlima.com/search.jsp?q=CT" class="blue121" rel="nofollow">CT</a> &nbsp;<a href="http://search.qianlima.com/search.jsp?q=%BE%B0%B9%DB" class="blue121" rel="nofollow">景观</a> &nbsp;<a href="http://search.qianlima.com/search.jsp?q=DR" class="blue121" rel="nofollow">DR</a> &nbsp;<a href="http://search.qianlima.com/search.jsp?q=%B7%A7%C3%C5" class="blue121" rel="nofollow">阀门</a> &nbsp;<a href="http://search.qianlima.com/search.jsp?q=%CE%DB%CB%AE" class="blue121" rel="nofollow">污水</a>&nbsp; <a href="http://search.qianlima.com/search.jsp?q=%C5%E7%C8%AA" class="blue121" rel="nofollow">喷泉</a> &nbsp;<a href="http://search.qianlima.com/search.jsp?q=%BB%FA%B3%A1" class="blue121" rel="nofollow">机场</a> </td>                </tr>            </table></td>            <td width="2%">&nbsp;</td>          </tr>        </table></td>        <td width="7"><img src="http://img.qianlima.com/20100709/bg_5.gif" width="7" height="28"></td>      </tr>      <tr>        <td width="10"><img src="http://img.qianlima.com/20100709/bg_3.gif" width="10" height="41"></td>        <td width="653" align="center" background="http://img.qianlima.com/20100709/bg_4.gif"><table width="99%" height="25" border="0" cellpadding="0" cellspacing="0">          <tr>            <form name="form1" method="get" action="http://search.qianlima.com/" target=_blank>              <td width="75%" align="left" class="red13b"><input name="q" type="text" style=width:400px class="input4"></td>              <td width="25%" align=left><input name="image" type=image src="http://img.qianlima.com/20100709/ss.jpg" width="73" height="23"  style=vertical-align:middle;> <a href=http://search.qianlima.com/qlm_adv_se.jsp target=_blank rel="nofollow">高级检索</a></td>            </form>          </tr>        </table></td>        <td width="7"><img src="http://img.qianlima.com/20100709/bg_6.gif" width="7" height="41"></td>      </tr>    </table></td>    <td width="176" align="center"><table width="160" height="65"  border="0" cellpadding="0" cellspacing="4" bgcolor="#f2f5fa" class="boder1">      <tr align="center">        <td height="25" background="http://img.qianlima.com/20100709/bg1_1.gif" class="tu"><a href="http://www.qianlima.com/about/about.shtml" rel="nofollow">关于我们</a></td>        <td height="25" background="http://img.qianlima.com/20100709/bg1_1.gif" class="tu"><a href="http://www.qianlima.com/about/contact.shtml" rel="nofollow">联系我们</a></td>      </tr>      <tr align="center">        <td height="25" background="http://img.qianlima.com/20100709/bg1_1.gif" class="tu"><a href="http://www.qianlima.com/about/huiyuan.shtml" rel="nofollow">会员服务</a></td>        <td height="25" background="http://img.qianlima.com/20100709/bg1_1.gif" class="tu"><a href="javascript:window.external.AddFavorite('http://www.qianlima.com/','千里马商机网')" rel="nofollow">收藏本站</a></td>      </tr>    </table></td>  </tr></table><table width="960" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">  <tbody><tr>    <td width="10"><img src="http://www.qianlima.com/images/20100709/bg2.jpg" width="10" height="30"></td>    <td width="940" align="center" background="http://www.qianlima.com/images/20100709/bg2_1.jpg"><table width="930" border="0" cellspacing="0" cellpadding="0">      <tbody><tr>        <td width="930" align="left"><table width="930" border="0" cellspacing="0" cellpadding="0">          <tbody><tr align="center">            <td width="110" background="http://www.qianlima.com/images/bg2695.gif" class="tu" style="padding-top:5px ">　 <a href="http://www.qianlima.com" class="white13b"><strong><font color="black">千里马首页</font></strong></a></td>            <td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/cat.jsp?catid=-9999&amp;progid=0" class="white13b">招标公告</a></td>            <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>            <td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/cat.jsp?catid=-9999&amp;progid=1" class="white13b">招标预告</a></td>            <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>            <td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/cat.jsp?catid=-9999&amp;progid=2" class="white13b">招标变更</a></td>            <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>            <td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/cat.jsp?catid=-9999&amp;progid=3" class="white13b">中标结果</a></td>            <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>						<td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/zb_file_list.jsp" class="white13b">招标文件</a></td>						<td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>						<td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/xm_list.jsp" class="white13b">拟在建项目</a></td>            <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>			<td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/yezhu_vip_list.jsp" class="white13b">VIP项目</a></td>            <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>			<td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/common/agents.jsp" class="white13b">招标机构库</a></td>           <td width="3"><img src="http://www.qianlima.com/images/20100709/bg2_3.jpg" width="3" height="30"></td>			<td width="75" background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px "><a href="http://www.qianlima.com/huizhan/exhibition_main.jsp" class="white13b">展会频道</a></td>            <td background="http://www.qianlima.com/images/20100709/1_bg5_1.jpg" class="tu" style="padding-top:5px " align="right"><table width="100%" border="0" cellspacing="0" cellpadding="0">          <tbody><tr>            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">                <tbody><tr>                  <td width="15" align="center">&nbsp;</td>                  <td align="left">&nbsp;</td>                </tr>            </tbody></table></td>            <td align="right" valign="bottom"><img src="http://www.qianlima.com/images/tel34.gif"></td>                       </tr>        </tbody></table></td>          </tr>        </tbody></table></td>           </tr>    </tbody></table></td>    <td width="10"><img src="http://img.qianlima.com/20100709/bg2_2.jpg" width="10" height="30"></td>  </tr></tbody></table><table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">  <tr>    <td height="3"></td>  </tr></table><table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">  <tr>    <td><!-- 广告位：C1 --><script type="text/javascript">BAIDU_CLB_fillSlot("156429");</script></td>  </tr></table><table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">  <tr>    <td height="3"></td>  </tr></table>

<table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">

  <tr valign="top">
    <td width="630" align="center"> 
<table width="100%"  border="0" cellpadding="0" cellspacing="0" class="boder2">
      <tr>
        <td valign="top"><table width="100%"  border="0" align="center" cellpadding="0" cellspacing="0">
          <tr>
            <td height="30" align="left">&nbsp;&nbsp;&nbsp;&nbsp;<span class="red121">您现在的位置：</span><a href=/>千里马招标网</a> &gt;&gt; <a href=http://www.qianlima.com/common/zb.jsp>招标中心</a> &gt;&gt; 站内公告</td>
          </tr>
        </table>
          <table width="95%"  border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td height="40" align="center"><table width="80%"><tr><td class="red16b" align=center>热烈庆祝北京科技大学、千里马产学研合作基地正式授牌成立！</td></tr></table></td>
            </tr>
            <tr>
              <td width=100% bgcolor=CCCCCC align="center" height=1>
              </td>
            </tr>
            <tr>
              <td align="center" valign="top" style="padding:10px "><table width="100%"  border="0" cellspacing="0" cellpadding="0">
                  <tr>
<td align="left" style=font-size:14px>

<table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                    <td align="left" style="font-size:14px; line-height: 25px;">                   
                    <p style="text-indent: 2em;">2018年8月24日北京科技大学和北京千里马网信科技有限公司大数据技术应用联合研发基地正式授牌成立，北京科技大学人工智能研究院陈红松教授、千里马CEO王剑波等主要领导均出席了该仪式。</p>
                    <center><img src="http://upload.qianlima.com/upload/20180828/20180828110645_792.png" width="500" height="340"></center>
                    <p style="text-indent: 2em;">千里马公司自2001年成立以来一直秉承“让工程变简单”的理念，持续深化产学研合作，依托高端创新平台，加强产品的设计研发，凭借每天为全国企业用户提供招标、中标、采购、海量工程信息，满足了用户随时随地、及时查看信息的需求，从而得到了众多企业管理者和市场人员的认可。</p>
                    <p style="text-indent: 2em;">北京科技大学是教育部直属全国重点大学，国家“双一流”世界一流学科建设高校，国家“211工程”、“985工程优势学科创新平台”重点建设院校，研究院主要围绕智能计算与大数据、智能通信与宽带物联网、智能控制与无人系统、智能感知与知识自动化、智能制造与脑科学、智能冶金六大研究方向，推进大跨度的学科交叉融合，推进大范围的技术与产业融合。并为多家企业提供技术支持和人才储备，为我国企业的技术发展做出诸多贡献。</p>
                    <center><img src="http://upload.qianlima.com/upload/20180828/20180828110722_572.jpg" width="500" height="340"></center>
                    <p style="text-indent: 2em;">今天双方的合作即是对企业多年来坚持技术创新的充分肯定，也为企业持续发展创造了新的机遇。借此契机，千里马公司一定会适应新的发展机遇，深化和学校的合作，进一步提高科研创新能力，研发出更多的新产品、好产品，赢得更大的市场，实现做大做强，实现共赢。</p>
                    </td>
                    </tr>
                    </tbody>
                  </table> 

</td>
                  </tr>
                </table>                </td>
            </tr>
    
          </table></td>
      </tr>
    </table>
</td>
    <td align="right">
	

<style>  .HY_classify p{    padding-left:0;  }  .HY_classify span{      background:none;    height: 100%;    display: inline-block;    padding-left: 15px;    padding-right: 15px;  cursor: pointer;  }  .HY_classify span.active{    background-color: rgb(252,150,14);    color:#fff;  }</style><style>  .HY_classify p{    padding-left:0;  }  .HY_classify span{      background:none;    height: 100%;    display: inline-block;    padding-left: 15px;    padding-right: 15px;  cursor: pointer;  }  .HY_classify span.active{    background-color: rgb(252,150,14);    color:#fff;  }</style><table width="325" border="0" cellspacing="0" cellpadding="0">				      <tr>        <td width="19"><img src="http://img.qianlima.com/1_bg1.jpg" width="19" height="29"></td>        <td  style="position:  relative; position:  relative;"  width="300" align="left" background="http://img.qianlima.com/1_bg1_1.jpg" class="black14b HY_classify"> &nbsp;        	<span class="red13b tabone active" id="rr">招标热词</span>			<span class="red13b tabtwo">采购热词</span>			<a href="http://www.qianlima.com/gjxx/sitemap.html"   target="_blank" style="font-weight:  normal;  position:  absolute; right: 0;">更多>></a>		</td>        <td width="6"><img src="http://img.qianlima.com/1_bg1_2.jpg" width="10" height="29"></td>      </tr>     <tr valign="top" id="listtab1">        <td colspan="3" class="boder2" style="padding:5px "><table width="100%" border="0" cellspacing="0" cellpadding="0">            <tbody><tr>              <td align="left"><div id="dv">									<a href="http://www.qianlima.com/gjxx/tag3/"  target="_blank">建筑工程</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag8/"  target="_blank">市政工程</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag5/"  target="_blank">给排水</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag6/"  target="_blank">钢结构</a>&nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag96/"  target="_blank">园林</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag14/"  target="_blank">中央空调</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag69/"  target="_blank">路灯护栏</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag4/"  target="_blank">防水工程</a>&nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag106/"  target="_blank">广告牌</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag191/"  target="_blank">配电</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag98/"  target="_blank">绿化</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag94/"  target="_blank">交通运输</a> &nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag150/"  target="_blank">色谱仪</a> &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag180/"  target="_blank">水利工程</a> &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag283/"  target="_blank">办公家具</a> &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag68/"  target="_blank">道路标志</a>  &nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag117/"  target="_blank">医疗设备</a> &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag247/"  target="_blank">系统集成</a>  &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag245/"  target="_blank">弱电工程</a> &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag101/"  target="_blank">垃圾处理</a>&nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag187/"  target="_blank">电力设备</a> &nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag105/"  target="_blank">喷泉</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag2/"  target="_blank">房屋建筑</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag248/"  target="_blank">安防监控</a>	&nbsp;&nbsp;        							</div></td>            </tr>        </tbody></table></td>      </tr>	  	  	  	  	        <tr valign="top" id="listtab2" style="display:none;">        <td colspan="3" class="boder2" style="padding:5px "><table width="100%" border="0" cellspacing="0" cellpadding="0">            <tbody><tr>              <td align="left"><div id="dv">    								<a href="http://www.qianlima.com/gjxx/tag18/"  target="_blank">建材</a>&nbsp;&nbsp;										<a href="http://www.qianlima.com/gjxx/tag19/"  target="_blank">建设</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag13/"  target="_blank">电梯</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag91/"  target="_blank">管道管材</a>	&nbsp;&nbsp;									</div>    								<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag112/"  target="_blank">净化</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag141/"  target="_blank">试剂</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag143/"  target="_blank">超声波B超</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag172/"  target="_blank">仪器仪表</a>	&nbsp;&nbsp;									</div>    								<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag196/"  target="_blank">水泵</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag213/"  target="_blank">化工设备</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag219/"  target="_blank">能源化工</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag298/"  target="_blank">广告</a>	&nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag291/"  target="_blank">办公设备</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag317/"  target="_blank">软件</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag321/"  target="_blank">数字数显</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag324/"  target="_blank">止回阀调节阀</a>	&nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag351/"  target="_blank">台式机</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag358/"  target="_blank">铝材药材</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag419/"  target="_blank">肉类</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag440/"  target="_blank">纱窗窗帘</a>	&nbsp;&nbsp;									</div>									<div id="dv">									<a href="http://www.qianlima.com/gjxx/tag516/"  target="_blank">坐垫坐便</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag227/"  target="_blank">橡胶</a>	&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag21/"  target="_blank">泥处理</a>&nbsp;&nbsp;									<a href="http://www.qianlima.com/gjxx/tag132/"  target="_blank">医保药品</a>	&nbsp;&nbsp;   									</div></td>            </tr>        </table></td>      </tr>				    </table>      <table width="325" border="0" cellspacing="0" cellpadding="0">        <tr>          <td height="5"></td>        </tr>      </table>      <table width="325" border="0" cellspacing="0" cellpadding="0">        <tr>          <td height="5"><a target=_blank href="http://www.qianlima.com/about/zp.htm"><img src="http://img.qianlima.com/zp_tu.gif" width="326" height="80" border="0"></a></td>        </tr>      </table>      <table width="325" border="0" cellspacing="0" cellpadding="0">        <tr>          <td height="5"></td>        </tr>      </table>      <table width="325" border="0" cellpadding="0" cellspacing="0" class="boder2">        <tr>          <td width="31"><img src="http://img.qianlima.com/1_bg.gif" width="31" height="29"></td>          <td width="80" align="center" valign="bottom" background="http://img.qianlima.com/1_bg_1.jpg" class="black14b"><span class="red13b">行业招标</span></td>          <td width="10"><img src="http://img.qianlima.com/1_bg_2.jpg" width="10" height="29"></td>          <td width="204" background="http://img.qianlima.com/1_bg_3.gif">&nbsp;</td>        </tr>        <tr>          <td colspan="5" align=center>		  <table border="0" cellspacing="2" cellpadding="2">            <tr>              <td align="center"><a href="/zb/hy_45/">交通运输</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_46/">机械设备加工</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_64/">安全防护 </a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_57/">出版印刷包装</a></td>            </tr>            <tr>              <td align="center"><a href="/zb/hy_47/">电子电器</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_52/">建筑水利桥梁</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_51/">通讯通信</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_50/">计算机网络</a></td>            </tr>            <tr>              <td align="center"><a href="/zb/hy_48/">化工能源</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_53/">环护绿化园林</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_54/">医疗卫生</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_61/">商业服务</a></td>            </tr>            <tr>              <td align="center"><a href="/zb/hy_49/">冶金矿产</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_56/">旅游运动娱乐</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_55/">科教办公</a> </td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_68/">艺术相关</a></td>            </tr>            <tr>              <td align="center"><a href="/zb/hy_67/">仪器仪表</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_58/">轻工业纺织食品</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_60/">农林渔牧</a></td>              <td align="center">|</td>              <td align="center"><a href="/zb/hy_63/">其他行业</a></td>            </tr>          </table></td>        </tr>      </table>      <table width="325" border="0" cellspacing="0" cellpadding="0">        <tr>          <td height="5"></td>        </tr>      </table>      <table width="325" border="0" cellspacing="0" cellpadding="0">        <tr>          <td width="31"><img src="http://img.qianlima.com/1_bg.gif" width="31" height="29"></td>          <td width="80" align="center" valign="bottom" background="http://img.qianlima.com/1_bg_1.jpg" class="black14b"><span class="red13b">地区招标</span>          </td>          <td width="10"><img src="http://img.qianlima.com/1_bg_2.jpg" width="10" height="29"></td>          <td width="204" background="http://img.qianlima.com/1_bg_3.gif">&nbsp;</td>        </tr>        <tr align="left" bgcolor="#fff9f6">          <td colspan="4" class="boder3" style="padding:5px "><table width="100%"  border="0" cellspacing="0" cellpadding="0">              <tr>                <td width="21%" height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华北</td>                <td width="79%" align="left">[<a href="/zb/area_2/" class="blue121">北京</a>] [<a href="/zb/area_26/" class="blue121">天津</a>] [<a href="/zb/area_9/" class="blue121">河北</a>] [<a href="/zb/area_22/" class="blue121">山西</a>] [<a href="/zb/area_18/" class="blue121">内蒙古</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;东北</td>                <td align="left">[<a href="/zb/area_14/" class="blue121">吉林</a>] [<a href="/zb/area_17/" class="blue121">辽宁</a>] [<a href="/zb/area_11/" class="blue121">黑龙江</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;西北</td>                <td align="left">[<a href="/zb/area_23/" class="blue121">陕西</a>] [<a href="/zb/area_4/" class="blue121">甘肃</a>] [<a href="/zb/area_19/" class="blue121">宁夏</a>] [<a href="/zb/area_20/" class="blue121">青海</a>] [<a href="/zb/area_28/" class="blue121">新疆</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华东</td>                <td align="left">[<a href="/zb/area_21/" class="blue121">山东</a>] [<a href="/zb/area_1/" class="blue121">安徽</a>] [<a href="/zb/area_24/" class="blue121">上海</a>] [<a href="/zb/area_15/" class="blue121">江苏</a>] [<a href="/zb/area_30/" class="blue121">浙江</a>] [<a href="/zb/area_3/" class="blue121">福建</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华中</td>                <td align="left">[<a href="/zb/area_10/" class="blue121">河南</a>] [<a href="/zb/area_12/" class="blue121">湖北</a>] [<a href="/zb/area_13/" class="blue121">湖南</a>] [<a href="/zb/area_16/" class="blue121">江西</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;华南</td>                <td align="left">[<a href="/zb/area_5/" class="blue121">广东</a>] [<a href="/zb/area_6/" class="blue121">广西</a>] [<a href="/zb/area_8/" class="blue121">海南</a>]</td>              </tr>              <tr>                <td height="25" align="center" background="http://img.qianlima.com/1_bg3.jpg" class="tu">&nbsp;西南</td>                <td align="left">[<a href="/zb/area_29/" class="blue121">云南</a>] [<a href="/zb/area_7/" class="blue121">贵州</a>] [<a href="/zb/area_25/" class="blue121">四川</a>] [<a href="/zb/area_31/" class="blue121">重庆</a>] [<a href="/zb/area_27/" class="blue121">西藏</a>]</td>              </tr>          </table></td>        </tr>      </table>            <table width="325" border="0" cellspacing="0" cellpadding="0">        <tr>          <td height="5"></td>        </tr>      </table>	  	  <script>            $(".tabone").bind("mouseover",function(){            $("#listtab1").show();            $("#listtab2").hide();            $(".tabone").addClass("active");            $(".tabtwo").removeClass("active");            });            $(".tabtwo").bind("mouseover",function(){            $("#listtab2").show();            $("#listtab1").hide();            $(".tabtwo").addClass("active");            $(".tabone").removeClass("active");            });      </script>

	</td>
  </tr>
</table>
<table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <tr>
    <td height="5"></td>
  </tr>
</table>
<table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
  <tr>
    <td height="5"></td>
  </tr>


    
	<input id="refererUrl" type="hidden" value="http://www.qianlima.com/common/wrap_newpage.jsp">
	<input id="contentId2" type="hidden" value="997">
	<input id="subscribe" type="hidden" value="1">
	<script type="text/javascript" src="http://www.qianlima.com/css/newweb/add_Behavior_record.js"></script>

<table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">  <tr>    <td align="center"><table width="100%"  border="0" cellspacing="0" cellpadding="0">      <tr>        <td height="1" bgcolor="#cccccc"></td>      </tr>      <tr>        <td height="10"></td>      </tr>      <tr>        <td align="center"><a href="http://www.qianlima.com/" rel="nofollow">千里马首页</a> ┊ <a href="http://www.qianlima.com/about/about.shtml" rel="nofollow">关于我们</a> ┊ <a href="http://www.qianlima.com/about/contact.shtml" rel="nofollow">联系我们</a> ┊ <a href="http://www.qianlima.com/about/zp.htm" rel="nofollow">招聘信息</a> ┊ <a href="http://www.qianlima.com/about/huiyuan.shtml" rel="nofollow"><font color=red>会员服务</font></a> ┊ <a href="http://www.qianlima.com/about/fkfs.shtml" rel="nofollow">付款方式</a> ┊ <a href="http://www.qianlima.com/about/ggbj.shtml" rel="nofollow">广告服务</a> ┊ <a href="http://www.qianlima.com/common/law_list.jsp" rel="nofollow">招标法规</a> ┊ <a href="http://www.qianlima.com/about/copyright.shtml" rel="nofollow">网站声明</a> ┊ <a href="http://www.qianlima.com/about/yqlj.shtml" rel="nofollow">友情链接</a> ┊ <a href="http://www.qianlima.com/sitemap/1.shtml" rel="nofollow">网站地图</a> ┊ <a href="javascript:window.external.AddFavorite('http://www.qianlima.com/','千里马招标网')" rel="nofollow">收藏本站</a><br>版权所有 2008-2018 <a href=http://www.qianlima.com>千里马招标网</a> www.qianlima.com 京ICP备16007318号 <div style="width:300px;margin:0 auto; padding:20px 0;">		 		<a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802022728" style="display:inline-block;text-decoration:none;height:20px;line-height:20px;"><img src="" style="float:left;"/><p style="float:left;height:20px;line-height:20px;margin: 0px 0px 0px 5px; color:#939393;"><img src="http://img_al.qianlima.com/newDefault/images/beian.png" />京公网安备 11010802022728号</p></a>		 	</div></td>      </tr>    </table></td>  </tr>  <tr><td align=center><script language="javascript" src="http://www.qianlima.com/css/bottom.js"></script>				<!--可信网站图片LOGO安装开始--><script src="http://kxlogo.knet.cn/seallogo.dll?sn=e14010311010044934m03o000000&size=0"></script><!--可信网站图片LOGO安装结束--></td></tr></table><table width="960"  border="0" align="center" cellpadding="0" cellspacing="0" bgcolor=#FFFFFF>  <tr valign="top">    <td align="left" height=5px></td>  </tr>  <tr>    <td align="center"><script type="text/javascript">var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3F0a38bdb0467f2ce847386f381ff6c0e8' type='text/javascript'%3E%3C/script%3E"));</script><script type="text/javascript"> var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://"); document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3F5dc1b78c0ab996bd6536c3a37f9ceda7' type='text/javascript'%3E%3C/script%3E")) </script><script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1848524'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s96.cnzz.com/stat.php%3Fid%3D1848524%26show%3Dpic1' type='text/javascript'%3E%3C/script%3E"));</script> <script type='text/javascript'>      var _vds = _vds || [];      window._vds = _vds;      (function(){        _vds.push(['setAccountId', '83e3b26ab9124002bae03256fc549065']);        (function() {          var vds = document.createElement('script');          vds.type='text/javascript';          vds.async = true;          vds.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'dn-growing.qbox.me/vds.js';          var s = document.getElementsByTagName('script')[0];          s.parentNode.insertBefore(vds, s);        })();      })();  </script> </td>  </tr>  <tr valign="top">    <td align="left" height=5px></td>  </tr></table></body></html>



"""
    keyWord_list = ["晋江","项目","施工","预算","招标","千里"]
    url = "http://www.qzzb.gov.cn/project/projectInfo.do?projId=25270&tdsourcetag=s_pctim_aiomsg#"

    url_list = bottomUrl(html,keyWord_list,url)
    print(url_list)