/**
 * Created by 1 on 2016/6/26.
 */

var regMobilePhone=/^(?:13\d|15\d)\d{5}(\d{3}|\*{3})$/;
var regTelPhone=/^((0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/;
var regCard = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
function isMobilePhone(str){
    if(regMobilePhone.test(str)){
        return true;
    }
    return false;
}

function isPhone(str){
    if(regMobilePhone.test(str) || regTelPhone.test(str)){
        return true;
    }
    return false;
}

function isCard(str){
    if(regCard.test(str)){
        return true;
    }
    return false;
}
