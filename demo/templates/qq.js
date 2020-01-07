!
function(e) {
    var t = {};
    function n(o) {
        if (t[o]) return t[o].exports;
        var i = t[o] = {
            i: o,
            l: !1,
            exports: {}
        };
        return e[o].call(i.exports, i, i.exports, n),
        i.l = !0,
        i.exports
    }
    n.m = e,
    n.c = t,
    n.d = function(e, t, o) {
        n.o(e, t) || Object.defineProperty(e, t, {
            configurable: !1,
            enumerable: !0,
            get: o
        })
    },
    n.n = function(e) {
        var t = e && e.__esModule ?
        function() {
            return e.
        default
        }:
        function() {
            return e
        };
        return n.d(t, "a", t),
        t
    },
    n.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    },
    n.p = "/",
    n(n.s = 3)
} ([, , ,
function(e, t, n) {
    e.exports = n(4)
},
function(e, t, n) {
    "use strict";
    var o = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ?
    function(e) {
        return typeof e
    }: function(e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol": typeof e
    }; !
    function() {
        var e = {
            conflist: [],
            originConflist: [],
            exposureOids: [],
            rlMap: [],
            apUrlMap: [],
            isAndroidApp: [],
            isIOSApp: [],
            loadedAd: [],
            site: {},
            adConf: {},
            display_type: "inner",
            CONST: {
                MIN_LOADCOUNT: 1,
                MAX_LOADCOUNT: 10,
                ACTTYPE_DOWNLOAD: 35,
                AD_ACTITON_TYPE: {
                    URL: 0,
                    APP: 1,
                    PHONE: 18
                },
                PRODUCT_TYPE: {
                    OPEN_APP: 12,
                    MYAPP: 5,
                    IOSAPP: 19
                },
                SITESET_MOBILE_INNER: 25,
                DISPLAY_TYPE_INNER: "inner",
                DISPLAY_TYPE_BANNER: "banner",
                DISPLAY_TYPE_INTERSTITIAL: "interstitial",
                WRAP_TYPE_INTERSTITIAL: "gdt_template_interstitial_wrap"
            },
            tbsDomain: "recmd.html5.qq.com",
            tbsFlag: "tbs",
            init: function(t) {
                var n = e.getReqCond(t),
                o = t.posid || t.placement_id,
                i = t.count || e.CONST.MIN_LOADCOUNT,
                a = t.appid || t.app_id,
                r = t.from,
                d = t.tbs_config,
                p = t.onComplete;
                e.bindSite(o, t.site_set),
                e.bindAdConf(o, t),
                e.display_type = t.display_type ? t.display_type: e.display_type,
                e.checkLoadCondition(o, i, p) && (d ? f.isTBSPageView() && c.loadJS("//res.imtt.qq.com/tbs/tbs.js",
                function() {
                    if (s.tbsLoaded = !0, window.tbs && window.tbs.ad && window.tbs.ad.setAdInfo) try {
                        tbs.ad.setAdInfo({
                            ifShowAd: !!d.ifShowAd && d.ifShowAd,
                            adType: d.adType ? d.adType: "splice",
                            adShape: d.adShape ? d.adShape: "",
                            adPos: d.adPos ? d.adPos: "bottom",
                            appId: a,
                            adId: o
                        })
                    } catch(e) {} else console.log("tbsjs not ready")
                }) : (e.conflist.push({
                    posId: o,
                    count: i,
                    platform: "mobile",
                    from: r || "",
                    tbsAdConfig: d || null,
                    onComplete: function(n) {
                        e.callback(o, n, t)
                    },
                    context: {
                        appid: a,
                        req: {
                            support_https: c.isHttpsProtocol() ? 1 : 0
                        },
                        common: n
                    },
                    tempContext: {
                        appid: a,
                        req: {
                            support_https: c.isHttpsProtocol() ? 1 : 0
                        },
                        common: JSON.parse(JSON.stringify(n))
                    }
                }), e.originConflist.push({
                    posId: o,
                    count: i,
                    platform: "mobile",
                    from: r || "",
                    tbsAdConfig: d || null,
                    onComplete: function(n) {
                        e.callback(o, n, t)
                    },
                    context: {
                        appid: a,
                        req: {
                            support_https: c.isHttpsProtocol() ? 1 : 0
                        },
                        common: n
                    },
                    tempContext: {
                        appid: a,
                        req: {
                            support_https: c.isHttpsProtocol() ? 1 : 0
                        },
                        common: JSON.parse(JSON.stringify(n))
                    }
                })))
            },
            bindSite: function(t, n) {
                if (e.site[t]) return ! 0;
                e.site[t] = n
            },
            getSite: function(t) {
                return e.site[t] || !1
            },
            bindAdConf: function(t, n) {
                if (e.adConf[t]) return ! 0;
                e.adConf[t] = n
            },
            getAdConf: function(t) {
                return e.adConf[t] || !1
            },
            checkLoadCondition: function(t, n, o) {
                return ! (!t || !t.match(/^\d+$/)) && (!(!n || !c.isInteger(n) || n < e.CONST.MIN_LOADCOUNT || n > e.CONST.MAX_LOADCOUNT) && !(!o || "function" != typeof o))
            },
            getUserConnStatus: function(e) {
                return "wifi" == e ? 1 : "2g" == e ? 2 : "3g" == e ? 3 : "4g" == e ? 4 : 0
            },
            getReqCond: function(t) {
                var n = navigator.userAgent.toLowerCase() || "",
                o = t.muidtype || t.muid_type,
                i = t.muid,
                a = t.site_set,
                r = t.information_info || t.informationInfo,
                d = {
                    c_os: "",
                    c_hl: navigator.language || navigator.browserLanguage,
                    url: document.location.href,
                    sdk_src: "mobile_union_js",
                    tmpallpt: !0
                };
                if (t && t.display_type && t.display_type === e.CONST.DISPLAY_TYPE_INTERSTITIAL && (d.inline_full_screen = 1), window.location != window.parent.location) {
                    var s = document.referrer,
                    p = c.getByteLen(s);
                    p > 0 && p < 512 && (d.referrerurl = s)
                }
                if (n = n.toLowerCase(), f.isTBSPageView() && (d.flow_source = 2, window.browser && window.browser.connection && window.browser.connection.getType(function(e) {
                    e && (d.conn = this.getUserConnStatus(e))
                }), window.tbs && window.tbs.network)) {
                    var l = window.tbs.network.type();
                    l && (d.conn = this.getUserConnStatus(l))
                }
                return r && "undefined" != r && "" != r && (d.information_info = r),
                /android|adr/.test(n) ? d.c_os = "android": /ios|iphone|ipad|itouch/.test(n) && (d.c_os = "ios"),
                o && c.isValidMuidtype(o) && i && c.isValidMuid(i) && (d.muidtype = parseInt(o), d.muid = i),
                c.webpEnabled && (d.webp = "1"),
                a && (d.site_set = a),
                d
            },
            loadAd: function(t, n) {
                for (var o = e,
                i = [], a = 0; a < o.originConflist.length; a++) if (o.originConflist[a].context = JSON.parse(JSON.stringify(o.originConflist[a].tempContext)), t == o.originConflist[a].posId) {
                    o.originConflist[a].from && o.originConflist[a].from == o.tbsFlag && o.tbsDomain == document.domain && o.originConflist[a].context && o.originConflist[a].context.common && n && (o.originConflist[a].context.common.url = n),
                    i.push(o.refreshConnParam(o.originConflist[a]));
                    break
                }
                GDT.load(i)
            },
            checkAndLoadNativeAd: function() {
                var t = e;
                t.conflist && t.conflist.length > 0 && !t.qbsLoaded && c.loadJS("//qzonestyle.gtimg.cn/qzone/biz/comm/js/qbs.js",
                function() {
                    t.qbsLoaded = !0;
                    for (var e = [], n = 0; n < t.conflist.length; n++) t.conflist[n].from && t.conflist[n].from == t.tbsFlag && t.tbsDomain == document.domain || e.push(t.refreshConnParam(t.conflist[n]));
                    GDT.load(e)
                })
            },
            refreshConnParam: function(e) {
                if (f.isTBSPageView() && e && e.tempContext && e.tempContext.common) {
                    if (!e.tempContext.common.conn) {
                        var t = navigator.userAgent || "";
                        if ( - 1 == t.indexOf("TBS/") && -1 !== t.indexOf("MQQBrowser/") && (window.browser ? window.browser.connection ? window.browser.connection.getType(function(t) {
                            var n = t;
                            n ? e.tempContext.common.conn = "wifi" == n ? 1 : "2g" == n ? 2 : "3g" == n ? 3 : "4g" == n ? 4 : 0 : c.pingHot("nobrowserconnectionstate")
                        }) : c.pingHot("nobrowserconnection") : c.pingHot("nobrowser")), -1 !== t.indexOf("TBS/") && -1 !== t.indexOf("MQQBrowser/")) if (window.tbs) if (window.tbs.network) {
                            var n = window.tbs.network.type();
                            n ? e.tempContext.common.conn = "wifi" == n ? 1 : "2g" == n ? 2 : "3g" == n ? 3 : "4g" == n ? 4 : 0 : c.pingHot("notbsnetworktype")
                        } else c.pingHot("notbsnetwork");
                        else c.pingHot("notbs");
                        e.tempContext.common.conn || ( - 1 !== (t = t.toLowerCase()).indexOf("nettype/wifi") ? (e.tempContext.common.conn = 1, c.pingHot("netfromua")) : -1 !== t.indexOf("nettype/2g") ? (e.tempContext.common.conn = 2, c.pingHot("netfromua")) : -1 !== t.indexOf("nettype/3g") ? (e.tempContext.common.conn = 3, c.pingHot("netfromua")) : -1 === t.indexOf("nettype/4g") && -1 === t.indexOf("nettype/ctlte") || (e.tempContext.common.conn = 4, c.pingHot("netfromua")))
                    }
                    e.context = JSON.parse(JSON.stringify(e.tempContext))
                }
                return e
            },
            isAppAd: function(t) {
                return ! (!t || t.acttype != e.CONST.AD_ACTITON_TYPE.APP && t.producttype != e.CONST.PRODUCT_TYPE.IOSAPP && t.producttype != e.CONST.PRODUCT_TYPE.OPEN_APP && t.producttype != e.CONST.PRODUCT_TYPE.MYAPP)
            },
            exposeTemplateNativeAd: function(t, n) {
                var o = e,
                i = o.loadedAd[t];
                if (i) {
                    var a = {
                        placement_id: i.posid,
                        advertisement_id: i.adData.cl
                    };
                    o.doExpose(a)
                }
            },
            clickTemplateNativeAd: function(t, n, o) {
                var i = e,
                a = i.loadedAd[n];
                if (a) {
                    var r = {
                        down_x: t.pageX,
                        down_y: t.pageY,
                        up_x: t.pageX,
                        up_y: t.pageY
                    },
                    d = {
                        placement_id: a.posid,
                        advertisement_id: a.adData.cl,
                        s: encodeURIComponent(JSON.stringify(r))
                    };
                    i.doExpose(d),
                    i.doClick(d)
                }
            },
            loadIframeUrlJS: function(e, t, n) {
                var o = e.createElement("script");
                o.onload = o.onreadystatechange = o.onerror = function() {
                    o && o.readyState && /^(?!(?:loaded|complete)$)/.test(o.readyState) || (o.onload = o.onreadystatechange = o.onerror = null, o.src = "", o.parentNode.removeChild(o), o = null, n && n())
                },
                o.charset = "utf-8",
                o.src = t;
                try {
                    e.head.appendChild(o)
                } catch(e) {
                    console.log(e)
                }
            },
            creatInterstitialNativeContainer: function() {
                var t = e.CONST.WRAP_TYPE_INTERSTITIAL,
                n = document.getElementById(t);
                return n ? [t, n] : ((n = document.createElement("div")).id = t, document.body.appendChild(n), [t, n])
            },
            renderTemplateNativeAd: function(t, n) {
                var o = c.$("#" + n),
                i = e.loadedAd[t && t.tid],
                a = i && i.template,
                r = i && i.adData && i.adData.reltarget,
                d = i && i.adData && i.adData.producttype,
                s = i && i.adData && i.adData.ext && i.adData.ext.pkg_name,
                p = (i && i.adData && i.adData.ext && i.adData.ext.appid, i.posid),
                l = {
                    packagename: s
                };
                if (e.getAdConf(p).display_type === e.CONST.DISPLAY_TYPE_INTERSTITIAL && (o = e.creatInterstitialNativeContainer()[1], n = e.creatInterstitialNativeContainer()[0]), n && o && t && t.tid && t.advertisement_id && t.placement_id && i && a && t && t.tid && t.advertisement_id && t.placement_id && i && a) try {
                    if (e.checkEnvironment("inQB") && window.browser && window.browser.app && d == e.CONST.PRODUCT_TYPE.OPEN_APP && 1 == r) window.browser.app.isInstallApk(function(i) {
                        1 != i && e.creatAdframe(t, n, o, a, p)
                    },
                    l);
                    else if (e.checkEnvironment("inQW") && window.tbs && window.tbs.package && d == e.CONST.PRODUCT_TYPE.OPEN_APP && 1 == r) {
                        1 != window.tbs.package.isApkInstalled(l,
                        function(e) {}) && e.creatAdframe(t, n, o, a, p)
                    } else e.creatAdframe(t, n, o, a, p)
                } catch(i) {
                    e.creatAdframe(t, n, o, a, p),
                    console.log(i)
                }
            },
            setStyle: function(e, t) {
                if ("object" === (void 0 === t ? "undefined": o(t))) for (var n in t) e.style[n] = t[n]
            },
            setBannerContainerHeight: function(e) {
                var t = e.offsetWidth,
                n = parseInt(t / 6.4) + 1;
                if ("0px" === e.style.height) return ! 1;
                e.style.height = n + "px"
            },
            creatAdframe: function(t, n, o, i, a) {
                var r = "gdt_template_native_wrap_" + t.tid + "_" + t.advertisement_id,
                d = document.createElement("div"),
                s = e.getAdConf(a);
                d.id = r,
                s.display_type === e.CONST.DISPLAY_TYPE_INTERSTITIAL && e.setStyle(d, {
                    position: "fixed",
                    zIndex: 999,
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    background: "rgba(0, 0, 0, 0.4)"
                }),
                s.display_type === e.CONST.DISPLAY_TYPE_BANNER ? (o.innerHTML = "", o.appendChild(d)) : (s.display_type, e.CONST.DISPLAY_TYPE_INTERSTITIAL, o.innerHTML = "", o.appendChild(d));
                var p = document.createElement("iframe");
                p.id = r + "_iframe",
                p.name = r + "_iframe",
                p.height = 0,
                p.style.border = 0,
                d.appendChild(p);
                try {
                    e.setIframeElSize(p, o, t),
                    e.renderTemplateAd(p, i, null),
                    e.getOnorientationChange(p, i, p.id, o, t)
                } catch(e) {}
            },
            getTargetIframe: function(e, t) {
                var n = document.getElementsByTagName("iframe"),
                o = e.contentDocument || e.contentWindow && e.contentWindow.document,
                i = null;
                if (o) return o;
                if (null !== t) {
                    for (var a in n) Object.prototype.hasOwnProperty.call(n, a) && n[a].id === t && (o = (i = n[a]).contentDocument || i.contentWindow && i.contentWindow.document);
                    return o
                }
                return ! 1
            },
            renderTemplateAd: function(t, n, o) {
                var i = e.getTargetIframe(t, o),
                a = 0;
                if (!1 !== i) {
                    var r = setInterval(function() {
                        if (++a > 20) return clearInterval(r),
                        !1;
                        if (!m.checkIsHidden(t) && (i && "complete" == i.readyState || i && "interactive" == i.readyState)) if (i.body.scrollHeight > 150) t.style.height = i.body.scrollHeight + "px";
                        else {
                            if (! (i.body.getElementsByTagName("div").length >= 1)) return ! 1;
                            t.style.height = i.body.getElementsByTagName("div")[0].scrollHeight + "px"
                        }
                    },
                    500),
                    d = i.createElement("meta");
                    d.setAttribute("content", "edge"),
                    d.setAttribute("http-equiv", "X-UA-Compatible"),
                    d.setAttribute("charset", "utf-8"),
                    i.head.appendChild(d),
                    e.loadIframeUrlJS(i, "//test.hdongtui.com/js/mtaid.js",
                    function() {
                        i.body.innerHTML = n
                    })
                }
            },
            setIframeElSize: function(t, n, o) {
                var i = document.documentElement.clientWidth,
                a = document.documentElement.clientHeight,
                r = e.getAdConf(o.placement_id),
                d = e.loadedAd[o && o.tid],
                s = 0,
                p = 0;
                if (r.display_type === e.CONST.DISPLAY_TYPE_INTERSTITIAL) {
                    if (d && d.adData) {
                        var c = d.adData.template_width,
                        l = d.adData.template_height;
                        s = i < a ? .7 * i + "px": c * a / l * .7 + "px"
                    } else p = Math.min(i, a),
                    s = Math.min(.7 * p, .56 * a) + "px";
                    e.setStyle(t, {
                        position: "absolute",
                        margin: "auto",
                        top: 0,
                        left: 0,
                        bottom: 0,
                        right: 0,
                        width: s,
                        height: 0,
                        scrolling: "no",
                        transition: "all 0.05s ease-in-out 0s"
                    })
                } else r.display_type === e.CONST.DISPLAY_TYPE_BANNER ? (e.setStyle(t, {
                    width: "100%",
                    height: 0,
                    scrolling: "no",
                    transition: "all 0.05s ease-in-out 0s"
                }), e.setBannerContainerHeight(n)) : e.setStyle(t, {
                    width: "100%",
                    scrolling: "no"
                })
            },
            getOnorientationChange: function(t, n, o, i, a) {
                window.addEventListener("onorientationchange" in window ? "orientationchange": "resize",
                function(r) {
                    setTimeout(function() {
                        try {
                            e.setIframeElSize(t, i, a),
                            e.renderTemplateAd(t, n, o)
                        } catch(e) {}
                    },
                    300)
                },
                !1)
            },
            processTemplateNativeAd: function(t, n, o, i) {
                for (var a = [], r = n.data, d = e.getAdConf(t), s = "", p = 0; p < r.length; p++) {
                    var c = {
                        tid: r[p].traceid,
                        advertisement_id: r[p].cl,
                        placement_id: t,
                        item: p
                    };
                    a.push(c)
                }
                d.display_type === e.CONST.DISPLAY_TYPE_BANNER ? ((s = e.checkAdConf(d)).data = a, 0 === s.ret && a.length > 0 ? (o.onComplete && o.onComplete(s), e.renderTemplateNativeAd(a[0], d.containerid), e.carouselBanner(t)) : o.onComplete && o.onComplete(i)) : d.display_type === e.CONST.DISPLAY_TYPE_INTERSTITIAL ? ((s = e.checkAdConf(d)).data = a, 0 === s.ret && a.length > 0 ? o.onComplete && o.onComplete(s) : o.onComplete && o.onComplete(i)) : o.onComplete && o.onComplete(a)
            },
            closeTemplateNativeAd: function(t) {
                if ("object" === (void 0 === t ? "undefined": o(t)) && t.hasOwnProperty("traceid")) {
                    var n = e.loadedAd[t.traceid].posid,
                    i = e.getAdConf(n);
                    if (i.display_type === e.CONST.DISPLAY_TYPE_INTERSTITIAL) {
                        var a = e.CONST.WRAP_TYPE_INTERSTITIAL,
                        r = document.getElementById(a);
                        r.parentNode.removeChild(r)
                    }
                    if (i.display_type === e.CONST.DISPLAY_TYPE_BANNER) {
                        var d = i.containerid;
                        clearTimeout(i.timeout),
                        document.getElementById(d).style.height = "0px",
                        i.carousel = 0
                    }
                }
            },
            carouselBanner: function(t) {
                var n = e.getAdConf(t),
                o = 0; (o = n.carousel >= 6e3 && n.carousel <= 6e4 ? n.carousel: n.carousel > 6e4 ? 6e4: 0) >= 6e3 && o <= 6e4 && (n.timeout = setTimeout(function() {
                    e.loadAd(t)
                },
                o))
            },
            checkAdConf: function(n) {
                var o = {
                    ret: t.SUCCESS[0],
                    message: t.SUCCESS[1]
                };
                return n.display_type !== e.CONST.DISPLAY_TYPE_BANNER || n.containerid || (o.ret = t.CONTAINERID_EMPTY[0], o.message = t.CONTAINERID_EMPTY[1]),
                o
            },
            processCustomNativeAd: function(n, o, i, a) {
                e.getAdConf(n).display_type === e.CONST.DISPLAY_TYPE_BANNER && a.data && 0 === a.data.length && (a.ret = t.TEMPLATE_EMPTY[0], a.message = t.TEMPLATE_EMPTY[1]),
                i.onComplete && i.onComplete(a)
            },
            processinQWCustomNativeAd: function(t, n, o, i) {
                for (var a = n.data,
                r = [], d = 0; d < a.length; d++) {
                    var s = a[d].producttype,
                    p = a[d].reltarget,
                    c = {
                        packagename: a[d].ext.pkg_name
                    };
                    if (s == e.CONST.PRODUCT_TYPE.OPEN_APP && 1 == p) 1 != window.tbs.package.isApkInstalled(c,
                    function(e) {}) && r.push(i.data[d]);
                    else r.push(i.data[d])
                }
                i.data = r,
                o.onComplete && o.onComplete(i)
            },
            processinQBCustomNativeAd: function(t, n, o, i) {
                var a = n.data,
                r = [],
                d = a.length;
                function s(e) {
                    0 == e && (i.data = r, o.onComplete && o.onComplete(i))
                }
                for (var p = 0; p < a.length; p++) {
                    var c = a[p].producttype,
                    l = a[p].reltarget,
                    u = {
                        packagename: a[p].ext.pkg_name
                    };
                    if (--d, c == e.CONST.PRODUCT_TYPE.OPEN_APP && 1 == l) try {
                        window.browser.app.isInstallApk(function(e) {
                            "true" != JSON.stringify(e) && r.push(i.data[p]),
                            s(d)
                        },
                        u)
                    } catch(e) {
                        console.error(e)
                    } else r.push(i.data[p]),
                    s(d)
                }
            },
            checkEnvironment: function(e) {
                var t = navigator.userAgent;
                switch (e) {
                case "inQW":
                    return - 1 !== t.indexOf("TBS/") && -1 !== t.indexOf("MQQBrowser/");
                case "inTBS":
                    return - 1 !== t.indexOf("TBS/") || -1 !== t.indexOf("MQQBrowser/");
                case "inQB":
                    return - 1 == t.indexOf("TBS/") && -1 !== t.indexOf("MQQBrowser/");
                default:
                    return ! 1
                }
            },
            callback: function(t, n, o) {
                var i = {};
                i = o.site_set && e.CONST.SITESET_MOBILE_INNER.toString() === o.site_set.toString() ? {
                    data: this.getInsideAdData(t, n),
                    ret: n.ret,
                    cfg: {
                        noping: n.cfg && n.cfg.noping
                    }
                }: {
                    data: this.getUnionAdData(t, n),
                    ret: n.ret
                },
                n.template && n.template.length > 0 ? e.processTemplateNativeAd(t, n, o, i) : e.checkEnvironment("inQB") ? e.processinQBCustomNativeAd(t, n, o, i) : e.checkEnvironment("inQW") && window.tbs && window.tbs.package && window.tbs.package.isApkInstalled ? e.processinQWCustomNativeAd(t, n, o, i) : e.processCustomNativeAd(t, n, o, i)
            },
            setNativeLoadAd: function(t, n, o, i) {
                if (void 0 === t) return ! 1;
                e.loadedAd[t] = {
                    posid: n,
                    adData: o,
                    template: i
                }
            },
            setNativeUriMap: function(t, n, i) {
                if ("object" !== (void 0 === t ? "undefined": o(t)) || void 0 === n) return ! 1;
                e.rlMap[t.cl + n] = t.rl,
                e.apUrlMap[t.cl + n] = t.apurl,
                e.rlMap[t.cl + n + i] = t.rl,
                e.apUrlMap[t.cl + n + i] = t.apurl
            },
            setNativeAppStatus: function(t) {
                "object" === (void 0 === t ? "undefined": o(t)) && (e.isAppAd(t) && t.producttype == e.CONST.PRODUCT_TYPE.OPEN_APP && (e.isAndroidApp[t.cl] = !0), e.isAppAd(t) && t.producttype == e.CONST.PRODUCT_TYPE.IOSAPP && (e.isIOSApp[t.cl] = !0))
            },
            getClickUrl: function(t, n) {
                for (var o = n && n.rl,
                i = 0; i < e.originConflist.length; i++) if (t == e.originConflist[i].posId) {
                    if (e.originConflist[i].from && e.originConflist[i].from == e.tbsFlag && e.tbsDomain == document.domain) return e.isAndroidApp[n.cl] ? o = ~~o.indexOf("&s_lp") > 0 ? o: o + "&acttype=" + e.CONST.ACTTYPE_DOWNLOAD: e.isIOSApp[n.cl] && navigator && navigator.userAgent && -1 !== navigator.userAgent.indexOf("MicroMessenger") && (o += "&platform=wx&target=appstore"),
                    o;
                    break
                }
            },
            getInsideAdData: function(t, n) {
                for (var o = n.data,
                i = [], a = "", r = {},
                d = "", s = "", p = 0; p < o.length; p++) a = o[p].traceid,
                d = n.template,
                s = o[p],
                this.setNativeLoadAd(a, t, o[p], e.getTemplateByTraceid(a, d)),
                this.setNativeUriMap(s, t, a),
                this.setNativeAppStatus(s),
                r = {
                    advertisement_id: s.cl,
                    description: s.desc || "",
                    title: s.txt || "",
                    is_app: e.isAppAd(s),
                    icon_url: s.img2 || "",
                    img_url: s.img || "",
                    traceid: a,
                    productid: s.productid,
                    corporation_name: s.corporation_name || "",
                    corporate_image_name: s.corporate_image_name || "",
                    corporate_logo: s.corporate_logo || ""
                },
                "" !== s.video ? (r.has_video = !0, r.video = s.video) : r.has_video = !1,
                r.is_app && (r.app_score = s && s.ext && s.ext.appscore, r.pkg_url = s && s.ext && s.ext.pkgurl, r.pkg_name = s && s.ext && s.ext.pkg_name, r.icon_url = s && s.ext && s.ext.applogo, r.app_price = s && s.price && "-" != s.price ? parseInt(s.price) : -1, r.desttype = s && s.ext && s.ext.desttype, r.download_count = s && s.ext && s.ext.alist && s.ext.alist[2025] && s.ext.alist[2025].aid && s.ext.alist[2025].aid.total || -1),
                i.push(r);
                return i
            },
            getUnionAdData: function(t, n) {
                var o = n.data,
                i = [],
                a = "",
                r = {},
                d = "",
                s = "";
                if (!o) return i;
                for (var p = 0; p < o.length; p++) a = o[p].traceid,
                d = n.template,
                s = o[p],
                this.setNativeLoadAd(a, t, o[p], e.getTemplateByTraceid(a, d)),
                this.setNativeUriMap(s, t, a),
                this.setNativeAppStatus(s),
                r = {
                    advertisement_id: s.cl,
                    is_app: e.isAppAd(s),
                    icon_url: s.img2 || "",
                    img_url: s.img || "",
                    description: s.desc || "",
                    title: s.txt || "",
                    traceid: a
                },
                void 0 !== this.getClickUrl(t, s) && (r.click_url = this.getClickUrl(t, s)),
                r.is_app && (r.app_score = s.ext && s.ext.appscore || -1, r.app_price = s.price && "-" != s.price ? parseInt(s.price) : -1, r.download_count = s.ext && s.ext.alist && s.ext.alist[2025] && s.ext.alist[2025].aid && s.ext.alist[2025].aid.total || -1),
                i.push(r);
                return i
            },
            getTemplateByTraceid: function(e, t) {
                if (!t || t.length <= 0) return null;
                for (var n = 0; n < t.length; n++) {
                    var o = t[n].view;
                    if (o.indexOf(e) >= 0) return o
                }
                return null
            },
            doExpose: function(t) {
                var n = "";
                if (t && t.placement_id && t.advertisement_id && t.traceid) n = e.apUrlMap[t.advertisement_id + t.placement_id + t.traceid];
                else {
                    if (! (t && t.placement_id && t.advertisement_id)) return;
                    n = e.apUrlMap[t.advertisement_id + t.placement_id]
                }
                if (!e.exposureOids[n]) {
                    if (t.redirect)(new Image).src = n;
                    else GDT.view(t.placement_id, t.advertisement_id);
                    e.exposureOids[n] = !0
                }
            },
            doClick: function(t) {
                for (var n = "",
                i = e,
                a = "",
                r = 0; r < i.originConflist.length; r++) if (t.placement_id == i.originConflist[r].posId) {
                    if (i.originConflist[r].from && i.originConflist[r].from == i.tbsFlag && i.tbsDomain == document.domain) return;
                    break
                }
                if (t && t.s && t.advertisement_id && t.placement_id) {
                    if (a = t.traceid ? e.apUrlMap[t.advertisement_id + t.placement_id + t.traceid] : e.apUrlMap[t.advertisement_id + t.placement_id], !e.exposureOids[a]) return {
                        ret: 1,
                        msg: "error锛屼笉鑳借繘琛岀偣鍑昏烦杞�"
                    };
                    try {
                        var d = c.getCookie("gdt_fp");
                        if (d) {
                            var s = "object" === o(t.s) ? decodeURIComponent(JSON.stringify(t.s)) : decodeURIComponent(t.s); (s = JSON.parse(s)).fpid = d,
                            t.s = encodeURIComponent(JSON.stringify(s))
                        }
                    } catch(e) {}
                    if (n = i.rlMap[t.advertisement_id + t.placement_id] + "&s=" + t.s, i.isAndroidApp[t.advertisement_id]) {
                        if (t.qqse_extStr) n = n + "&qqse_extStr=" + encodeURIComponent(JSON.stringify(t.qqse_extStr));
                        if (t._autodownload && (n = n + "&_autodownload=" + t._autodownload), e.getSite(t.placement_id) == e.CONST.SITESET_MOBILE_INNER) if (0 == t.redirect)(new Image).src = n;
                        else location.href = n;
                        else n = ~~n.indexOf("&s_lp") > 0 ? n: n + "&acttype=" + i.CONST.ACTTYPE_DOWNLOAD,
                        location.href = n
                    } else i.isIOSApp[t.advertisement_id] && navigator && navigator.userAgent && -1 !== navigator.userAgent.indexOf("MicroMessenger") && (n += "&platform=wx&target=appstore"),
                    location.href = n
                }
            },
            getTopUrl: function() {
                if (window.top === window) return window.location.href;
                if (window.top !== window) {
                    var e = window.document.referrer && window.document.referrer.match(/^.+:\/\/[^\/]+/)[0];
                    return new URL(e).hostname.match(/qq.com$/gi),
                    window.location.href
                }
                return null
            }
        },
        t = {
            SUCCESS: [0, "骞垮憡鍔犺浇鎴愬姛"],
            CONTAINERID_EMPTY: [100001, "containerid 涓嶈兘涓虹┖锛岃杈撳叆骞垮憡瀹瑰櫒"],
            TEMPLATE_EMPTY: [100002, "杩斿洖鐨勫箍鍛婃ā鏉夸负绌猴紝璇锋鏌ヨ姹傝繑鍥炴暟鎹帓鏌ラ棶棰�"]
        },
        n = {
            status: {
                code: 0,
                msg: ""
            },
            posid: "",
            appid: "",
            type: "",
            onComplete: "",
            ext: {
                url: e.getTopUrl()
            },
            initHybridAd: function(e) {
                var t = this;
                if (this.status = this.checkHybridAdParam(e), 0 !== this.status.code) return this.onCompleteCb(e, this.status),
                !1;
                this.posid = e.placement_id,
                this.appid = e.app_id,
                this.type = e.type,
                c.loadJS("//qzs.qq.com/union/res/union_sdk/page/unjs/un.js",
                function() {
                    window.unjs && window.unjs.isInUnSdk() ? t.status = t.getRespStatus("INIT_SUCC") : t.status = t.getRespStatus("ENV_FAIL"),
                    t.onCompleteCb(e, t.status)
                })
            },
            getRespStatus: function(e) {
                var t = {
                    code: 0
                };
                switch (e) {
                case "NO_POSID":
                    t = {
                        code: -1,
                        msg: "placement_id is empty."
                    };
                    break;
                case "NO_APPID":
                    t = {
                        code: -2,
                        msg: "app_id is empty."
                    };
                    break;
                case "NO_ONCOMPLETE":
                    t = {
                        code: -3,
                        msg: "onComplete callback is empty."
                    };
                    break;
                case "ENV_FAIL":
                    t = {
                        code: -4,
                        msg: "env fail"
                    };
                    break;
                case "CB_NOT_FUN":
                    t = {
                        code: -5,
                        msg: "callback is not a function"
                    };
                    break;
                case "ENV_NOT_SUPPORT":
                    t = {
                        code: -6,
                        msg: "env is not support"
                    };
                    break;
                case "INIT_SUCC":
                default:
                    t = {
                        code: 0,
                        msg: "reward ad init success"
                    }
                }
                return t
            },
            checkHybridAdParam: function(e) {
                var t = this.getRespStatus("INIT_SUCC");
                return e.placement_id || (t = this.getRespStatus("NO_POSID")),
                e.app_id || (t = this.getRespStatus("NO_APPID")),
                "function" != typeof e.onComplete && (t = this.getRespStatus("NO_ONCOMPLETE")),
                t
            },
            onCompleteCb: function(e, t) {
                "function" == typeof e.onComplete && e.onComplete(t)
            }
        };
        window.GDT_HYB = n;
        var i = function(e) {
            if (this.hybrid = window.GDT_HYB, this.app_id = this.hybrid.appid, this.placement_id = this.hybrid.posid, this.ext_url = this.hybrid.ext.url, this.instance_id = this.getInstanceId(), 0 == this.hybrid.status.code) {
                var t = {
                    ext_url: this.ext_url,
                    instance_id: this.instance_id,
                    placement_id: this.placement_id
                };
                window.unjs.project && window.unjs.project.rewardVideo && window.unjs.project.rewardVideo.registerRewardVideoAD ? window.unjs.project.rewardVideo.registerRewardVideoAD(t,
                function(t) {
                    "function" == typeof e && e(t)
                }) : "function" == typeof e && e(this.hybrid.getRespStatus("ENV_NOT_SUPPORT"))
            } else e("function" == typeof e ? this.hybrid.status: this.hybrid.getRespStatus("CB_NOT_FUN"))
        };
        i.prototype = {
            loadAd: function() {
                var e = {
                    instance_id: this.instance_id
                };
                0 == this.hybrid.status.code && window.unjs.project && window.unjs.project.rewardVideo.loadRewardVideoAD(e)
            },
            showAd: function() {
                var e = {
                    instance_id: this.instance_id
                };
                0 == this.hybrid.status.code && window.unjs.project && window.unjs.project.rewardVideo.showRewardVideoAD(e)
            },
            getInstanceId: function() {
                return "SPA_H5_HYBRID_" + (new Date).getTime()
            }
        };
        var a, r, d, s = {
            posid: "",
            apurl: "",
            tplType: "",
            posw: 300,
            posh: 250,
            needMask: !1,
            adType: "",
            bannerbox: {},
            tbsWebviewValidateValue: 0,
            webviewType: 0,
            missExpose: !1,
            tbsLoaded: !1,
            posborder: 4,
            adDomain: "qzonestyle.gtimg.cn",
            onClose: function() {},
            onFail: function() {},
            posDomain: "",
            postNum: "",
            init: function(t) {
                t.adType = t.type,
                s.cfgs = t,
                s.filltype = t.filltype || t.fill_type,
                s.adType = t.type,
                s.site_set = t.site_set,
                s.posDomain = encodeURIComponent(document.location.protocol + "//" + document.location.host),
                s.postNum = Math.random(),
                s.posid = t.posid || t.placement_id,
                s.initPlatform(),
                "banner" == t.adType ? s.initBanner(t) : "interstitial" == t.adType ? s.initInter(t) : "native" == t.adType ? e.init(t) : "rewardVideo" == t.adType && n.initHybridAd(t),
                c.debugTest()
            },
            initPlatform: function() {
                var e = document.createElement("script");
                s.platform = "web",
                -1 !== navigator.userAgent.search("QQ/") ? (s.platform = "mqq", e.src = "//pub.idqqimg.com/qqmobile/qqapi.js?_bid=152", document.body.appendChild(e)) : -1 !== navigator.userAgent.search("Qzone") ? (window.QZAppExternal && window.QZAppExternal.getPlatform || (e.src = "//qzonestyle.gtimg.cn/qzone/phone/m/v4/widget/mobile/jsbridge.js", document.body.appendChild(e)), s.platform = "mqzone", s.isHybrid = !0) : s.isHybrid = !1
            },
            BannerCb: {
                onBannerLoaded: function() {}
            },
            initBanner: function(e) {
                var t = s,
                n = [640, 480, 320, 240],
                o = [100, 75, 50, 38],
                i = 480,
                a = 75,
                r = s.getOs();
                if (window.screen) i = window.screen.width,
                a = window.screen.height,
                "ios" == r && (i *= window.devicePixelRatio, a *= window.devicePixelRatio);
                else if (document.body) {
                    var d = window.devicePixelRatio || 1;
                    i = document.body.clientWidth * d,
                    a = document.body.clientHeight * d
                }
                if (i < a) {
                    var p = a;
                    a = i,
                    i = p
                }
                i > n[0] ? (t.bannerbox.posw = n[0], t.bannerbox.posh = o[0]) : i > n[1] ? (t.bannerbox.posw = n[1], t.bannerbox.posh = o[1]) : i > n[2] ? (t.bannerbox.posw = n[2], t.bannerbox.posh = o[2]) : (t.bannerbox.posw = n[3], t.bannerbox.posh = o[3]),
                t.posw = t.bannerbox.posw,
                t.posh = t.bannerbox.posh,
                t.BannerCb.onBannerLoaded = e.onBannerLoaded,
                t.renderBannerWindow(e)
            },
            getOs: function() {
                var e = navigator.userAgent || "";
                return e = e.toLowerCase(),
                /android|adr/.test(e) ? "android": /ios|iphone|ipad|itouch/.test(e) ? "ios": "uncondi"
            },
            loadGDT: function() {
                s.renderWindow({},
                s.posw, s.posh, s.zIndex)
            },
            getWidthHeight: function() {
                var e = document.body.clientWidth || 640,
                t = document.body.clientHeight || 100;
                if (e > t) {
                    var n = e;
                    e = t,
                    t = n
                }
                var o = s;
                o.inter_posw = 300,
                o.inter_posh = 250,
                2 * o.inter_posw < e && (o.inter_posw *= 2, o.inter_posh *= 2)
            },
            renderBannerWindow: function(e) {
                s.posborder = 0,
                s.renderWindow(e, 0, 0, 1, "//qzonestyle.gtimg.cn/qzone/biz/res/tmpl/banner.html")
            },
            checkParam: function(e) {
                return ! new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~锛丂#锟モ€︹€�&*锛堬級&mdash;鈥攟{}銆愩€戔€橈紱锛氣€濃€�'銆傦紝銆侊紵]").test(e)
            },
            getUid: function() {
                var e = c.getParameter("sid"),
                t = c.getParameter("openid"),
                n = c.getParameter("openkey"),
                o = "";
                return e && c.checkParam(e) && (o += "&sid=" + encodeURIComponent(e)),
                t && c.checkParam(t) && (o += "&openid=" + encodeURIComponent(t)),
                n && c.checkParam(n) && (o += "&openkey=" + encodeURIComponent(n)),
                o
            },
            renderWindow: function(e, t, n, o, i) {
                var a = '<div class="gdth_popup_floater"></div><div class="gdth_popup_wrap" style="margin:0 auto;position:relative;{OTHER}">                            {CLOSEDIV}                                <iframe id="{IFRID}" style="position:static !important;display:block !important;margin:0 !important;padding:0 !important;visibility:visible !important;float:none !important;border-width:0 !important;width:{W};height:{H};"                                scrolling=no frameBorder=0 marginHeight=0 marginWidth=0 allowTransparency=true                                 src="{HTMLURL}#{PARAM}"></iframe>{LOGO}                        </div>',
                r = s;
                i || (i = "//qzonestyle.gtimg.cn/qzone/biz/res/tmpl/interstitial.html"),
                r.zIndex = o;
                var d = e.appid || e.app_id,
                l = e.muidtype || e.muid_type,
                u = e.muid,
                f = e.posid || e.placement_id,
                g = !!r.BannerCb.onBannerLoaded,
                h = e.information_info || e.informationInfo,
                w = e.taglist || e.tag_list,
                _ = e.posclass || e.pos_class,
                b = r.inter_posw,
                y = r.inter_posh;
                "banner" == e.adType && (b = r.posw, y = r.posh);
                var v = "_spoint=" + s._spoint + "&posid=" + encodeURIComponent(f) + "&posh=" + y + "&posw=" + b + "&posdomain=" + r.posDomain + "&postnum=" + r.postNum + "&adtype=" + encodeURIComponent(e.adType) + "&ishybrid=" + s.isHybrid + "&platform=" + s.platform + "&posclass=" + encodeURIComponent(_) + "&hasBannerCB=" + encodeURIComponent(g);
                d && "undefined" != d && (v += "&appid=" + encodeURIComponent(d)),
                w && "undefined" != w && (v += "&taglist=" + encodeURIComponent(w)),
                l && "undefined" != l && u && "undefined" != u && (v += "&muidtype=" + encodeURIComponent(l) + "&muid=" + encodeURIComponent(u)),
                h && "undefined" != h && "" != h && (v += "&information_info=" + encodeURIComponent(h));
                var A = document.body.clientWidth || document.body.offsetWidth;
                v += "&win_w=" + A,
                v += "&win_h=" + (document.body.clientHeight || document.body.offsetHeight);
                var C = e.containerid || e.container_id,
                T = 0,
                I = 0;
                C && (r.container = c.$("#" + C), m.checkIsHidden(r.container) || (T = "" + r.container.clientWidth, I = "" + r.container.clientHeight, p.BANNER_IFRAME_WIDTH = r.container.clientWidth, T = T.replace(/px/, ""), I = I.replace(/px/, ""), -1 != T.indexOf("%") && (T = 0), -1 != I.indexOf("%") && (I = 0), T && (v += "&conw=" + T) && (A = T), I && (v += "&conh=" + I)));
                var x = A / 320 || 1;
                r.scale = x,
                v += "&scale=" + x,
                v += "&conw=" + T;
                var E = document.location.href;
                if (v += "&visiturl=" + encodeURIComponent(E), v += "&referrerurl=" + encodeURIComponent(window.location != window.parent.location ? document.referrer: ""), v += "&iframeheight=" + p.BANNER_IFRAME_HEIGHT, v += "&iframewidth=" + p.BANNER_IFRAME_WIDTH, C && c.$("#" + C)) {
                    var S = c.$("#" + C).getBoundingClientRect();
                    S && (v += "&iframetop=" + S.top)
                } else {
                    if (R = c.$("#gdt-" + r.posid)) {
                        var N = R.getBoundingClientRect();
                        N && (v += "&iframetop=" + N.top)
                    }
                }
                v += "&documentElementClientHeight=" + document.documentElement.clientHeight;
                var O = c.getCookie("gdt_fp");
                O && "" != O && (v += "&fpid=" + encodeURIComponent(O)),
                a = a.replace(/{HTMLURL}/, i).replace(/{PARAM}/, v + r.getUid());
                var P = document.createElement("div");
                if (P.setAttribute("style", "display:none"), P.id = "gdt_banner_popup_wrap", "banner" == e.adType) {
                    var k = 30,
                    D = 10;
                    P.innerHTML = a.replace(/{OTHER}/, "max-width:1280px;").replace(/{W}/, "100%").replace(/{IFRID}/, "gdt_banner_ifr").replace(/{LOGO}/, '<div id="gdt_logo" style="background-image:url(//qzonestyle.gtimg.cn/open_proj/proj-gdt-toufang/img/ad-sign/logo-ad-s.png);background-size: cover;width:' + k + "px;height:" + D + 'px;position: absolute;right: 0;bottom: 0;"><i ></i></div>').replace(/{H}/, "").replace(/{CLOSEDIV}/, "");
                    var R, L = "fixed" == e.position ? "position:fixed": "";
                    if (C && c.$("#" + C)) L = "",
                    c.$("#" + C).appendChild(P);
                    else(R = c.$("#gdt-" + r.posid)).parentNode.insertBefore(P, R);
                    P.setAttribute("style", L + ";left:0px;bottom:0;width:100%;display:none")
                } else {
                    var B = "width:30px;height: 30px;",
                    H = document.createElement("div");
                    H.id = "gdt_inter_popup_wrap",
                    600 != r.inter_posw && 500 != r.inter_posw || (B = "width:60px;height: 60px;"),
                    r.btn_pos = 9,
                    600 == r.inter_posw && (r.btn_pos = 18);
                    k = 36,
                    D = 12;
                    a = a.replace(/{OTHER}/, 'display: inline-block;"  id="gdth_popup_wrap').replace(/{W}/, r.inter_posw + "px").replace(/{H}/, r.inter_posh + "px").replace(/{LOGO}/, '<div id="gdt_logo" style="background-image:url(//qzonestyle.gtimg.cn/open_proj/proj-gdt-toufang/img/ad-sign/logo-ad-s.png);background-size: cover;width:' + k + "px;height:" + D + 'px;position: absolute;right: 0;bottom: 0;"><i ></i></div>').replace(/{IFRID}/, "gdt_ifr").replace(/{CLOSEDIV}/, '<a href="javascript:" style="' + B + 'position: absolute;right:4px;top:5px;text-indent: -9999px;overflow: hidden;z-index: 100;" onclick="GDT.closeWindow(this)" class="icon_close">鍏抽棴</a>'),
                    H.innerHTML = a,
                    H.style.display = "none",
                    document.body.appendChild(H)
                }
                window.postMessage ? s.initPostMsg() : "banner" == e.adType && s.showBannerWin()
            },
            setOnorientationChangeScale: function(e) {
                var t = document.body.clientWidth / 320 || 1;
                s.scale = t,
                s.showBannerWin(),
                m.postMessage(e, {
                    scale: t,
                    flag: "onorientationchange"
                },
                s.adDomain)
            },
            onorientationChange: function(e) {
                var t = this;
                window.addEventListener("onorientationchange" in window ? "orientationchange": "resize",
                function() {
                    setTimeout(function() {
                        t.setOnorientationChangeScale(e)
                    },
                    100),
                    setTimeout(function() {
                        t.setOnorientationChangeScale(e)
                    },
                    400)
                },
                !1)
            },
            initPostMsg: function() {
                s.bindPostMsg || (s.bindPostMsg = !0, s.onorientationChange("banner"), c.addEvent(window, "message",
                function(e) {
                    var t = e.origin;
                    if ((t = c.skipHttpOrHttpsProtocol(t)) && t == s.adDomain && e && e.data) {
                        var n = "string" == typeof e.data ? JSON.parse(e.data) : e.data;
                        if (o || n) {
                            var o = n.result;
                            if ("fail" == o) s.closeWindow(),
                            s.IntersCb.onFail && s.IntersCb.onFail();
                            else if ("success" == o) s.showBannerWin();
                            else if (n.op) if ("checkToLoadTBS" == n.op) f.isTBSsupported() && f.tbsLoad();
                            else if ("mqzoneclick" == n.op) c.pingHot("mqzoneclicked"),
                            QZAppExternal.callSchema(function(e) {},
                            {
                                url: "mqzone://arouse/webview?source=push&url=" + n.url + "&safari=0&version=1"
                            });
                            else if ("mclick" === n.op) {
                                var i = n.isApp;
                                window.mqq && window.mqq.ui && window.mqq.ui.openUrl({
                                    url: decodeURIComponent(n.url),
                                    target: i ? 2 : 1,
                                    style: 3
                                })
                            } else if ("androidAppOtherClick" === n.op) location.href = decodeURIComponent(n.url);
                            else if ("loaededad" === n.op) s.adready = !0,
                            s.IntersCb.onInterstitialLoaded(),
                            c.$(".gdth_popup_floater").style.marginBottom = -this.inter_posh / 2 + "px";
                            else if ("googleInterstitialLoaded" === n.op) s.adready = !0,
                            s.IntersCb.onInterstitialLoaded(),
                            c.$("#gdt_logo").style.display = "none",
                            c.$(".gdth_popup_floater").style.marginBottom = -this.inter_posh / 2 + "px";
                            else if ("showbigsize" == n.op) s.adready = !0,
                            s.IntersCb.onInterstitialLoaded(),
                            c.$("#gdt_ifr").style.width = "580px",
                            c.$("#gdt_ifr").style.height = "900px",
                            c.$("#gdt_logo").style.right = "0",
                            c.$(".gdth_popup_floater").style.marginBottom = "-450px",
                            s.fixFullAdPos(290, 450),
                            window.addEventListener("orientationchange",
                            function(e) {
                                s.fixFullAdPos(290, 450)
                            });
                            else if ("checkHidden" == n.op) {
                                var a = n.type,
                                r = n.posid,
                                d = n.flag,
                                l = m.getBaseNode(a);
                                u.checkHidden(l, r, a, d)
                            } else if ("exposeCheck" == n.op) {
                                a = n.type,
                                r = n.posid;
                                var g = n.apurl,
                                h = n.tplType;
                                u.prepare(a, r, g, h, w)
                            } else if ("getImgStatus" == n.op) {
                                a = n.type,
                                r = n.posid;
                                var w = n.isImgComplete;
                                u.imgExposeCheck(a, r, g, h, w)
                            } else if ("showBanner" == n.op) s.showBannerWin();
                            else if ("noAd" == n.op) s.showBannerWin(),
                            s.BannerCb.onBannerLoaded && s.BannerCb.onBannerLoaded({
                                ret: 1,
                                msg: "no ad"
                            });
                            else if ("showGoogleBanner" == n.op) {
                                var _ = s.scale * p.BANNER_IFRAME_HEIGHT;
                                c.$("#gdt_banner_popup_wrap").style.display = "",
                                c.$("#gdt_banner_ifr").style.height = _ + "px",
                                c.$("#gdt_banner_popup_wrap").style.height = _ + "px",
                                c.$("#gdt_logo").style.display = "none"
                            }
                        }
                    }
                }))
            },
            posWinW: 0,
            posWinH: 0,
            fixNormalAdPos: function() {
                var e = c.$("#gdt_inter_popup_wrap");
                if (e) {
                    e.style.textAlign = "center",
                    e.querySelector(".gdth_popup_floater").style.height = "50%",
                    e.querySelector(".gdth_popup_floater").style.position = "relative";
                    var t = this.inter_posh || 250;
                    e.querySelector(".gdth_popup_floater").style.marginBottom = -t / 2 + "px"
                }
            },
            fixFullAdPos: function(e, t) {
                var n = window.orientation || screen.orientation;
                c.$("#gdth_popup_wrap").style.webkitTransform = !n || 90 != n && -90 != n && 270 != n ? "": "rotate(-90deg)";
                document.body.clientWidth,
                document.body.clientHeight
            },
            getParameter: function(e, t) {
                var n = new RegExp("(\\?|#|&)" + e + "=([^&#]*)(&|#|$)"),
                o = location.href.match(n);
                return o && "" != o || t || (o = window.location.href.match(n)),
                o ? o[2] : ""
            },
            windowShowing: !1,
            showWindow: function() {
                if (!s.windowShowing && s.adready) {
                    s.windowShowing = !0,
                    s.needMask && s.showMask(s.zIndex - 1),
                    c.$("#gdt_inter_popup_wrap").setAttribute("style", "position: absolute;overflow: hidden;width: 100%;height: 100%;left: 0;top: 0;z-index:" + s.zIndex);
                    var e = c.$("#gdt_ifr"),
                    t = s.adDomain;
                    t = c.isHttpsProtocol() ? "https://" + t: "http://" + t,
                    e.contentWindow.postMessage(JSON.stringify({
                        op: "exp"
                    }), t),
                    s.fixNormalAdPos()
                }
            },
            showBannerWin: function() {
                var e = s.scale * p.BANNER_IFRAME_HEIGHT;
                c.$("#gdt_banner_popup_wrap").style.display = "",
                c.$("#gdt_banner_ifr").style.height = e + "px",
                c.$("#gdt_banner_popup_wrap").style.height = e + "px",
                s.showedBannerWindow = !0
            },
            closeWindow: function(e) {
                c.$("#gdt_inter_popup_wrap").setAttribute("style", "display:none;"),
                c.pingHot("close_inters"),
                s.hideMask(),
                s.IntersCb.onClose && s.IntersCb.onClose(),
                s.windowShowing = !1
            },
            MASKID: "gdt_mask",
            showMask: function(e) {
                var t = s.MASKID;
                if (!c.$("#" + t)) {
                    var n = document.createElement("div");
                    n.id = t,
                    n.setAttribute("style", "display:block;position:absolute;left:0px;top:0px;width:100%;height:100%;background-color:black;opacity:.70;-moz-opacity:0.7;filter:alpha(opacity=70);z-index:" + e),
                    document.body.appendChild(n)
                }
            },
            hideMask: function() {
                var e = c.$("#" + s.MASKID);
                e && e.parentNode.removeChild(e)
            },
            IntersCb: {
                onClose: function() {},
                onInterstitialLoaded: function() {}
            },
            initInter: function(e) {
                window.postMessage;
                var t = e;
                s.zIndex = t.zIndex || t.z_index || 9999,
                s.getWidthHeight(),
                s.needMask = !(!t.showmask && !t.show_mask);
                t.load;
                s.IntersCb.onClose = t.onClose,
                s.IntersCb.onInterstitialLoaded = t.onInterstitialLoaded,
                s.renderWindow(t, s.inter_posw, s.inter_posh, s.zIndex)
            },
            collectDPI: function() {
                window.setTimeout(function() {
                    var e = window.screen.width || 1e4,
                    t = 4;
                    e < 100 ? t = 1 : e < 300 ? t = 2 : e < 600 && (t = 3);
                    var n = "" + window.devicePixelRatio;
                    n && (n = n.replace(/\./g, "_")),
                    c.pingHot("screen" + t + ".dpi" + n);
                    var o = "ns";
                    window.URL && URL.createObjectURL && (o = "ss"),
                    c.pingHot(o + "." + s.getOs())
                },
                500)
            }
        },
        p = {
            VALID_VISUAL_DISTANCE: 40,
            BANNER_IFRAME_HEIGHT: 50,
            BANNER_IFRAME_WIDTH: document.body.clientWidth || document.body.offsetWidth
        },
        c = a = {
            webpEnabled: !1,
            loadJS: function(e, t) {
                var n = document.getElementsByTagName("head")[0],
                o = document.createElement("script");
                o.onload = o.onreadystatechange = o.onerror = function() {
                    o && o.readyState && /^(?!(?:loaded|complete)$)/.test(o.readyState) || (o.onload = o.onreadystatechange = o.onerror = null, o.src = "", o.parentNode.removeChild(o), o = null, "function" == typeof t && t())
                },
                o.charset = "utf-8",
                o.src = e;
                try {
                    n.appendChild(o)
                } catch(e) {
                    console.log(e)
                }
            },
            getByteLen: function(e) {
                for (var t = 0,
                n = 0; n < e.length; n++) null !== e[n].match(/[^x00-xff]/gi) ? t += 2 : t += 1;
                return t
            },
            getParameter: function(e, t) {
                var n = new RegExp("(\\?|#|&)" + e + "=([^&#]*)(&|#|$)"),
                o = location.href.match(n);
                return o && "" != o || t || (o = window.location.href.match(n)),
                o ? o[2] : ""
            },
            checkParam: function(e) {
                return ! new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~锛丂#锟モ€︹€�&*锛堬級&mdash;鈥攟{}銆愩€戔€橈紱锛氣€濃€�'銆傦紝銆侊紵]").test(e)
            },
            skipHttpOrHttpsProtocol: function(e) {
                return e ? ( - 1 !== e.indexOf("http://") ? e = e.substring(7) : -1 !== e.indexOf("https://") && (e = e.substring(8)), e) : e
            },
            isHttpsProtocol: function() {
                return - 1 === location.protocol.indexOf("http:") && -1 !== location.protocol.indexOf("https:")
            },
            pingHot: function(e, t) {
                var n = t || {},
                o = ["//pingfore.qq.com/pingd", "?dm=gdt.qq.com.hot", "&url=", escape(location.pathname), "&tt=-", "&hottag=h5_inter." + e, "&hotx=" + (n.x || 9999), "&hoty=" + (n.y || 9999), "&rand=", Math.random()].join(""); (new Image).src = o
            },
            extendIframe: function(e, t) {
                var n = c.$("#gdt_ifr");
                n.width = t + "px",
                n.height = e + "px",
                n.style.width = t + "px",
                n.style.height = e + "px"
            },
            addEvent: function(e, t, n) {
                window.attachEvent ? e.attachEvent("on" + t, n) : e.addEventListener(t, n, !1)
            },
            $: function(e) {
                return document.querySelector(e)
            },
            isInteger: function(e) {
                return "number" == typeof e && e % 1 == 0
            },
            isValidMuid: function(e) {
                return ! new RegExp("[^a-f0-9]").test(e)
            },
            isValidMuidtype: function(e) {
                return !! parseInt(e) && !new RegExp("[^1-3]").test(e)
            },
            checkWebp: function(e) {
                var t = new Image;
                t.onerror = function() {
                    a.webpEnabled = !1,
                    e && e()
                },
                t.onload = function() {
                    a.webpEnabled = !0,
                    e && e()
                },
                t.src = "data:image/webp;base64,UklGRiwAAABXRUJQVlA4ICAAAAAUAgCdASoBAAEAL/3+/3+CAB/AAAFzrNsAAP5QAAAAAA=="
            },
            debugTest: function() {
                var e = document.createElement("div");
                e.style.position = "fixed",
                e.style.backgroundColor = "gray";
                var t = document.body.firstChild;
                document.body.insertBefore(e, t),
                s.divObj = e,
                s.divObj.innerHTML = ""
            },
            log: function(e) {
                s.divObj.innerHTML += e + "</br>"
            },
            getCookie: function(e) {
                var t = null,
                n = new RegExp("(^| )" + e + "=([^;]*)(;|$)");
                return document.cookie.match(n) ? (t = document.cookie.match(n), unescape(t[2])) : null
            },
            setCookie: function(e, t, n) {
                try {
                    document.cookie = e + "=" + escape(t) + ";expires=" + n.toGMTString()
                } catch(e) {
                    console.error(e)
                }
            }
        },
        l = (d = {},
        (r = {}).init = function(e, t, n) {
            d.apurl = e,
            d.windowClientHeight = t,
            d.posid = n
        },
        r.check = function(e, t) {
            if (t == d.posid) {
                var n = parseInt(window.pageYOffset) + parseInt(d.windowClientHeight) - parseInt(e);
                if ("complete" == document.readyState) return n > p.VALID_VISUAL_DISTANCE;
                setTimeout(function() {
                    r.check(e, t)
                },
                50)
            }
        },
        r),
        u = function() {
            var e = {},
            t = s;
            return e.bindScroll = {},
            e.posTop = 0,
            e.tbsAdInfo = {},
            e.prepare = function(n, o, i, a, r) {
                e.posid = o,
                e.apurl = i,
                f.isTBSsupported() ? (f.tbsAdInfo.adtype = n, f.tbsAdInfo.posid = o, f.tbsAdInfo.apurl = i, t.tbsLoaded && 1 == t.webviewType ? f.tbsExposeCheck() : t.tbsLoaded && 2 == t.webviewType && t.missExpose ? (u.doExpose(n, o, i), t.missExpose = !1) : t.tbsLoaded ? 1 != t.webviewType && 2 != t.webviewType && (e.initExpose(n, o, i, a, r), c.addEvent(document, "scroll",
                function() {
                    e.scrollFunc(n, o, i, a, r)
                }), e.bindScroll[o] = !0) : f.tbsLoad()) : (e.initExpose(n, o, i, a, r), c.addEvent(document, "scroll",
                function() {
                    e.scrollFunc(n, o, i, a, r)
                }), e.bindScroll[o] = !0)
            },
            e.checkHidden = function(e, t, n, o) {
                var i = ""; (i = m.checkIsHidden(e) ? "true": "false") && m.postHiddenStatus(n, i, t, o)
            },
            e.initExpose = function(t, n, o, i, a) {
                if ("complete" == document.readyState) {
                    var r = document.documentElement.clientHeight;
                    l.init(o, r, n),
                    e.commonExposeCheck(t, n, o, i, a)
                } else setTimeout(function() {
                    e.initExpose(t, n, o, i, a)
                },
                50)
            },
            e.calculateElmTop = function(e) {
                return m.getBaseNode(e).offsetTop
            },
            e.commonExposeCheck = function(n, o, i, a, r) {
                a && "tplImg" == a && !r ? (m.postMessage(n, {
                    op: "checkImg",
                    id: o
                },
                t.adDomain), e.imgExposeCheck(n, o, i, a, r)) : e.doExposeCheck(n, o, i, a)
            },
            e.imgExposeCheck = function(t, n, o, i, a) {
                a && e.posid == n ? (o || (o = e.apurl), e.doExposeCheck(t, n, o, i)) : setTimeout(function() {
                    e.imgExposeCheck(t, n, o, i, a)
                },
                50)
            },
            e.doExposeCheck = function(t, n, o, i) {
                var a = e.calculateElmTop(t);
                l.check(a, n) && e.doExpose(t, n, o, a)
            },
            e.doExpose = function(n, o, i, a) {
                e.bindScroll[o] && (document.removeEventListener("scroll", e.scrollFunc, !1), e.bindScroll[o] = !1),
                m.postMessage(n, {
                    op: "doExpose",
                    apurl: i,
                    id: o,
                    posTop: a
                },
                t.adDomain)
            },
            e.scrollFunc = function(n, o, i, a, r) {
                t.handler && (t.handler = null),
                e.bundleSetTimeout(n, o, i, a, r)
            },
            e.bundleSetTimeout = function(n, o, i, a, r) {
                t.handler = window.setTimeout(function() {
                    e.commonExposeCheck(n, o, i, a, r)
                },
                50)
            },
            e
        } (),
        f = function() {
            var e = {},
            t = s;
            return e.tbsAdInfo = {},
            e.isTBSPageView = function() {
                var e = navigator.userAgent;
                return - 1 !== e.indexOf("TBS/") || -1 !== e.indexOf("MQQBrowser/")
            },
            e.isTBSsupported = function() {
                return ! ( - 1 === navigator.userAgent.indexOf("TBS") || void 0 === o(window.tbsJs) || !tbsJs.isTbsJsapiEnabled())
            },
            e.tbsExposeCheck = function() {
                if (e.tbsAdInfo.adtype && e.tbsAdInfo.posid && e.tbsAdInfo.apurl) {
                    var n = u.calculateElmTop(e.tbsAdInfo.adtype);
                    t.tbsWebviewValidateValue > p.VALID_VISUAL_DISTANCE && t.tbsWebviewValidateValue - n > p.VALID_VISUAL_DISTANCE && u.doExpose(e.tbsAdInfo.adtype, e.tbsAdInfo.posid, e.tbsAdInfo.apurl)
                }
            },
            e.tbsReady = function() {
                try {
                    tbs.event.onwebviewvalidate(function(n) {
                        var o = void 0 !== n.webview_type ? n.webview_type: "-1";
                        "-1" === o || "1" === o ? (t.tbsWebviewValidateValue = n.value, t.webviewType = 1, e.tbsExposeCheck()) : "2" === o && (t.webviewType = 2, e.tbsAdInfo.adtype && e.tbsAdInfo.posid && e.tbsAdInfo.apurl ? u.doExpose(e.tbsAdInfo.adtype, e.tbsAdInfo.posid, e.tbsAdInfo.apurl) : t.missExpose = !0)
                    })
                } catch(e) {}
            },
            e.tbsLoad = function() {
                c.loadJS("//res.imtt.qq.com/tbs/tbs.js",
                function() {
                    t.tbsLoaded = !0,
                    f.tbsReady()
                })
            },
            e
        } (),
        m = function() {
            var e = {};
            return e.getBaseNode = function(e) {
                return "banner" == e ? c.$("#gdt_banner_popup_wrap") : c.$("#gdt_inter_popup_wrap")
            },
            e.getIfr = function(e) {
                return "banner" == e ? c.$("#gdt_banner_ifr") : c.$("#gdt_ifr")
            },
            e.checkIsHidden = function(e) {
                for (var t = !1,
                n = e && e.style,
                o = 0; e != document && o <= 20;) if (o++, e != document && n && "none" != n.display && "hidden" != n.visibility && "collapse" != n.visibility) e = e && e.parentNode;
                else if (n && "none" == n.display || n && "hidden" == n.visibility || n && "collapse" == n.visibility) {
                    t = !0;
                    break
                }
                return t
            },
            e.postHiddenStatus = function(t, n, o, i) {
                var a = "",
                r = "";
                s.container && !e.checkIsHidden(s.container) && (a = ("" + s.container.clientWidth) / 320 || 1);
                s.showedBannerWindow && (r = s.showedBannerWindow),
                e.postMessage(t, {
                    isAdHidden: n,
                    scale: a,
                    showedBanner: r,
                    id: o,
                    flag: i
                },
                s.adDomain)
            },
            e.postMessage = function(e, t, n) {
                var o = m.getIfr(e);
                n = c.isHttpsProtocol() ? "https://" + n: "http://" + n,
                o.contentWindow && o.contentWindow.postMessage(JSON.stringify(t), n)
            },
            e
        } ();
        window.GDT = {
            loadGDT: s.loadGDT,
            closeWindow: s.closeWindow,
            showWindow: s.showWindow,
            log: function() {
                console.log(window.TencentGDT),
                console.log(document.location.href),
                console.log(document.head.querySelector("[name=viewport]"))
            },
            init: function(t) {
                var n = window.TencentGDT;
                if (t) s.init(t);
                else for (var o = 0,
                i = n.length; o < i; o++) s.init(n[o]);
                e.checkAndLoadNativeAd()
            }
        },
        s._spoint = +new Date,
        window.TencentGDT.NATIVE = {
            loadAd: e.loadAd,
            loadCallback: e.callback,
            doExpose: e.doExpose,
            doClick: e.doClick,
            renderAd: e.renderTemplateNativeAd,
            rewardVideoAd: i
        },
        window.TencentGDT.TN = {
            doExpose: e.exposeTemplateNativeAd,
            doClick: e.clickTemplateNativeAd,
            adClose: e.closeTemplateNativeAd
        };
        var g = window.TencentGDT,
        h = function() {
            if (g && g.length) {
                if (c.getCookie("gdt_fp") || setTimeout(function() {
                    try { (new Fingerprint2).get(function(e, t) {
                            if (e) {
                                var n = new Date;
                                n.setTime(n.getTime() + 31536e6),
                                c.setCookie("gdt_fp", e, n)
                            }
                        })
                    } catch(e) {}
                },
                2e3), (g = g.sort(function(e, t) {
                    return e.type && "banner" == e.type ? -1 : 1
                }))[0].type && "banner" != g[0].type) {
                    for (var t = 0,
                    n = g.length; t < n; t++) s.init(g[t]);
                    return void e.checkAndLoadNativeAd()
                }
                var o = "//qzonestyle.gtimg.cn/qzone/qzact/act/game/ad/index.js?v=20141119";
                if (1 === g[0].appflag) {
                    var i = document.createElement("script");
                    i.src = o,
                    i.onload = function() {
                        wanbaAd && wanbaAd.init && wanbaAd.init(g)
                    },
                    document.body.appendChild(i)
                } else {
                    window.addEventListener("message",
                    function(t) {
                        var n = t.origin;
                        if ((n = c.skipHttpOrHttpsProtocol(n)) && "qzs.qq.com" == n) {
                            if (!t.data) return;
                            if (1 !== (r = "string" == typeof t.data ? JSON.parse(t.data) : t.data).appflag && 0 !== r.appflag) return;
                            if (r && 0 === r.appflag) {
                                for (var i = 0,
                                a = g.length; i < a; i++) s.init(g[i]);
                                e.checkAndLoadNativeAd()
                            } else {
                                var r; (r = document.createElement("script")).src = o,
                                r.onload = function() {
                                    wanbaAd && wanbaAd.init && wanbaAd.init(g)
                                },
                                document.body.appendChild(r)
                            }
                        }
                    });
                    var a = document.createElement("iframe");
                    a.style = "width:0;height:0;display:none;",
                    a.width = 0,
                    a.height = 0,
                    a.frameBorder = 0,
                    a.src = "//qzs.qq.com/qzone/qzact/act/game/ad/proxy/index.html",
                    document.body.appendChild(a)
                }
            }
        }; !
        function() {
            if (!window.jsInited) {
                if (window.jsInited = !0, f.isTBSPageView()) {
                    var e = document.createElement("script");
                    e.src = "//jsapi.qq.com/get?api=connection.* ",
                    document.body.appendChild(e);
                    var t = document.createElement("script");
                    t.src = "//jsapi.qq.com/get?api=app.*",
                    document.body.appendChild(t);
                    var n = document.createElement("script");
                    n.src = "//res.imtt.qq.com/tbs/tbs.js",
                    document.body.appendChild(n)
                }
                if (!c.getCookie("gdt_fp")) {
                    var o = document.createElement("script");
                    o.src = "//qzonestyle.gtimg.cn/qzone/biz/res/tmpl/js/finger.js",
                    document.body.appendChild(o)
                }
                c.checkWebp(h)
            }
        } ()
    } ()
}]);