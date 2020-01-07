(function() {
    var CONST = {
        VALID_VISUAL_DISTANCE: 40
    };
    var templateNative = (function() {
        var tn = {
            adElementLoad: function(event, traceid, params, success) {
                if (success) {
                    var frameWrapEl = window.parent.document.getElementById(window.name);
                    if (frameWrapEl) {
                        if (exposureOperation.checkAdPositionisHidden(frameWrapEl)) {
                            exposureOperation.checkHiddenHandler[traceid] = (function(frameWrapEl, traceid, params) {
                                return setInterval(function() {
                                    if (!exposureOperation.checkAdPositionisHidden(frameWrapEl)) {
                                        clearInterval(exposureOperation.checkHiddenHandler[traceid]);
                                        exposureOperation.checkHiddenHandler[traceid] = null;
                                        exposureOperation.initExpose(frameWrapEl, traceid, params);
                                        util.addEvent(window.parent.document, 'scroll', exposureOperation.scrollFunc);
                                        exposureOperation.bindScrollFunc[traceid] = true;
                                        exposureOperation.doExpose(frameWrapEl, traceid, params);
                                    }
                                },
                                100);
                            })(frameWrapEl, traceid, params);
                        } else {
                            exposureOperation.initExpose(frameWrapEl, traceid, params);
                            util.addEvent(window.parent.document, 'scroll', exposureOperation.scrollFunc);
                            exposureOperation.bindScrollFunc[traceid] = true;
                            exposureOperation.doExpose(frameWrapEl, traceid, params);
                        }
                    }
                }
            },
            adClick: function(event, traceid, params) {

                window.parent.TencentGDT.TN.doClick(event, traceid, params);
            },
            adClose: function(event, traceid, params) {
                var frameWrapEl = window.parent.document.getElementById(window.name);
                window.parent.TencentGDT.TN.adClose({
                    event: event,
                    traceid: traceid,
                    params: params
                });
                if (frameWrapEl) {
                    frameWrapEl.parentNode.removeChild(frameWrapEl);
                }
            },
            openOfficialWebSite: function(event, traceid, params) {
                window.open("http://e.qq.com");
            }
        };
        return tn;
    } ());
    var exposureOperation = (function() {
        var operation = {
            checkHiddenHandler: {},
            scrollFuncHandler: {},
            bindScrollFunc: {},
            frameWrapEl: {},
            traceid: null,
            params: {},
            checkAdPositionisHidden: function(elm) {
                return util.checkIsHidden(elm, window.parent.document);
            },
            initExpose: function(frameWrapEl, traceid, params) {
                operation.frameWrapEl = frameWrapEl;
                operation.traceid = traceid;
                operation.params = params;
            },
            exposeCheck: function(elm) {
                var posTop = elm.offsetTop;
                var parentDocument = window.parent.document;
                var parentWindowClientHeight = parentDocument.documentElement.clientHeight;
                var visualDistance = parseInt(window.parent.pageYOffset) + parseInt(parentWindowClientHeight) - parseInt(posTop);
                if (visualDistance > CONST.VALID_VISUAL_DISTANCE) {
                    return true;
                } else {
                    return false;
                }
            },
            scrollFunc: function() {
                if (!operation.traceid) {
                    return;
                }
                if (operation.scrollFuncHandler[operation.traceid]) {
                    operation.scrollFuncHandler[operation.traceid] = null;
                }
                operation.scrollFuncHandler[operation.traceid] = window.setTimeout(function() {
                    operation.doExpose(operation.frameWrapEl, operation.traceid, operation.params);
                },
                50);
            },
            doExpose: function(elm, traceid, params) {
                if (operation.exposeCheck(elm)) {
                    if (operation.bindScrollFunc[traceid]) {
                        operation.bindScrollFunc[traceid] = false;
                        window.parent.document.removeEventListener('scroll', operation.scrollFunc, false);
                    }
                    window.parent.TencentGDT.TN.doExpose(traceid, params);
                }
            }
        };
        return operation;
    })();
    var util = (function() {
        var inner = {};
        inner.checkIsHidden = function(elm, father) {
            var isHidden = false;
            while (elm != father) {
                if (elm != father && elm.style.display != "none" && elm.style.visibility != "hidden" && elm.style.visibility != "collapse") {
                    elm = elm.parentNode;
                } else if (elm.style.display == "none" || elm.style.visibility == "hidden" || elm.style.visibility == "collapse") {
                    isHidden = true;
                    break;
                }
            }
            return isHidden;
        };
        inner.addEvent = function(elm, type, cb) {
            if (window.parent.attachEvent) {
                elm.attachEvent('on' + type, cb);
            } else {
                elm.addEventListener(type, cb, false);
            }
        }
        return inner;
    })();
    window.mtaid = templateNative;
})()