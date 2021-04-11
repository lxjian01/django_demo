/*-------------------altDialog弹出提示框----------------------------*/
/**
 * 弹出提示框
 * @param 提示内容
 */

window.onload = function () {
    /****************************
    * 作者：q821424508@sina.com   *
    * 时间：2012-08-20            *
    * version：2.0              *
    * 禁用回退键[backspace键]浏览历史跳转                     *
    ****************************/
    document.getElementsByTagName("body")[0].onkeydown = function () {

        //获取事件对象
        var event = window.event || arguments[0];

        if (event.keyCode == 8) {//判断按键为backSpace键

            //获取按键按下时光标做指向的element
            var elem = event.srcElement || event.currentTarget;

            //判断是否需要阻止按下键盘的事件默认传递
            var name = elem.nodeName;

            if (name != 'INPUT' && name != 'TEXTAREA') {
                return _stopIt(event);
            }
            var type_e = elem.type.toUpperCase();
            if (name == 'INPUT' && (type_e != 'TEXT' && type_e != 'TEXTAREA' && type_e != 'PASSWORD' && type_e != 'FILE')) {
                return _stopIt(event);
            }
            if (name == 'INPUT' && (elem.readOnly == true || elem.disabled == true)) {
                return _stopIt(event);
            }
        }
    }
}
function _stopIt(e) {
    if (e.returnValue) {
        e.returnValue = false;
    }
    if (e.preventDefault) {
        e.preventDefault();
    }

    return false;
}