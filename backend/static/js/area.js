var areaClass = {
	area: '',
	path: '',
	father: '',
	init: function (path) {
		this.initDom();
		this.path = path;
		this.getJson();
    },
	// 初始化地区串联选择元素
	initDom: function () {
		this.father.append('<select name="province" id="s_province"></select>' +
			'<select name="city" id="s_city"><option value="">地级市</option></select>' +
			'<select name="county" id="s_county"> <option value="">区/县</option></select>');
    },
	// 获取地区json
	getJson: function () {
		$.getJSON(this.path, function (result) {
			areaClass.area = result;
            areaClass.display(1);
            areaClass.bindEvent();
            areaClass.last();
        });
    },
	// select值变化
	change: function (level) {
		var pv = $("#s_province").val();
		var cv = $("#s_city").val();
		if (level == 1) {
            $("#s_city").empty();
            this.display(2, pv, cv);
        }
        $("#s_county").empty();
		this.display(3, pv, cv);
    },
	// 根据上一级变化渲染下一级选项
	display: function (level, p, c) {
		if (level == 1) {
			var dom = '<option value="">省份</option>';
			for (var i in this.area) {
				dom += '<option value="'+i+'">'+i+'</option>';
			}
			$("#s_province").append(dom);
		} else if (level == 2) {
			var dom = '';
			if (p.indexOf('省')>0 || p.indexOf('自治区')>0) {
				dom += '<option value="省级">省级</option>';
			} else {
				dom += '<option value="">地级市</option>';
			}
			for (var i in this.area[p]) {
				dom += '<option value="'+i+'">'+i+'</option>';
			}
			$("#s_city").append(dom);
		} else {
			var dom = '<option value="">区/县</option>';
			for (var i in this.area[p][c]) {
				dom += '<option value="'+this.area[p][c][i]+'">'+this.area[p][c][i]+'</option>';
			}
			$("#s_county").append(dom);
		}
    },
	// 绑定省市变化事件
	bindEvent: function () {
		$("#s_province").change(function () {
            areaClass.change(1);
        });
        $("#s_city").change(function () {
            areaClass.change(2);
        });
    },
	// 最后执行事件
	last: function () {}
};