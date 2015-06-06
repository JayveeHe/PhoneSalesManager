/**
 * Created by Jayvee on 2015/5/27.
 */
<!-- 获取表格数据 -->
$(document).ready(function () {
    $.get('/userinfo', null, function (data) {
        var jsondata = JSON.parse(data);
        if (jsondata.stat == 'ok') {
            username = jsondata.username;
            pos = jsondata.pos;
            power = jsondata.power;
            $('#userpos').text('当前分店号：' + pos);
        } else {
            alert('请先登录！');
            window.location.href = '/login';
        }
    });
    loadRemainsData('RemainsRecords');
});

//alert('START');
// $(document).ready(function () {
//     loadRemainsData('PhoneRemains');
// });
var remains_tableObj;
var sales_tableObj;
var remains_dataSet;
var sales_dataSet;
var jsondata;
var theTypeIs;
var currentTable;
var username;
var pos;
var power;

function logout() {
    if (confirm("确认退出登录么？")) {
        window.location.href = '/logout';
    }
}

function loadRemainsData(tablename) {
    $("#sales_div").hide();
    $("#remains_div").show();
    remains_dataSet = [];
    currentTable = "RemainsRecords";
    $.get('/data/' + tablename, null, function (data, status) {
        if (status == "success") {
            //document.getElementById("tables").innerHTML = xmlhttp.responseText;
            //var dataSet = [];
            jsondata = JSON.parse(data);
            //theTypeIs = Object.keys(jsondata[0]);
            for (var i = 0; i < jsondata.length; i++) {
                var data_temp = [];
                data_temp[0] = jsondata[i]['record_id'];
                data_temp[1] = jsondata[i]['item_name'];
                data_temp[2] = jsondata[i]['item_type'];
                data_temp[3] = jsondata[i]['item_id'];
                data_temp[4] = jsondata[i]['sale_pos'];
                data_temp[5] = jsondata[i]['remains'];
                //for (var j = 0; j < theTypeIs.length; j++) {
                //    data_temp[j] = jsondata[i][theTypeIs[j]];
                //}
                data_temp[6] = [];
                remains_dataSet[i] = (data_temp);
            }
            //console.log(remains_dataSet);
            if (!remains_tableObj) {
                remains_tableObj = $("#remains_tables").dataTable({
                    "data": [],
                    "fnCreatedRow": function (nRow, aData, iDataIndex) {
                        $('td:eq(' + (6) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-primary' data-toggle='modal' data-target='#Remains_Update_Modal' onclick=remainsUpdate(" + iDataIndex + ")>修改</button>");
                        $('td:eq(' + (6) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-danger' onclick=removeRemainsRecords(" + iDataIndex + ")>删除</button>");
                    },
                    "columns": [
                        {"title": "序号"},
                        {"title": "名称"},
                        {"title": "类型"},
                        {"title": "编号"},
                        {"title": "分店号"},
                        {"title": "剩余量"},
                        {"title": "操作"}
                    ]
                });
                if (remains_dataSet.length > 0) {
                    remains_tableObj.fnAddData(remains_dataSet);
                }
            }
            else {
                remains_tableObj.fnClearTable();
                if (remains_dataSet.length > 0) {
                    remains_tableObj.fnAddData(remains_dataSet);
                }
                //console.log();
            }
        }
    });
}

function loadSalesData(tablename) {
    $("#sales_div").show();
    $("#remains_div").hide();
    sales_dataSet = [];
    currentTable = "SalesRecords";
    $.get('/data/' + tablename, null, function (data, status) {
        if (status == "success") {
            //document.getElementById("tables").innerHTML = xmlhttp.responseText;
            //var dataSet = [];
            jsondata = JSON.parse(data);
            //theTypeIs = Object.keys(jsondata[0]);
            for (var i = 0; i < jsondata.length; i++) {
                var data_temp = [];
                data_temp[0] = jsondata[i]['record_id'];
                data_temp[1] = jsondata[i]['item_name'];
                data_temp[2] = jsondata[i]['item_type'];
                data_temp[3] = jsondata[i]['item_id'];
                data_temp[4] = jsondata[i]['price'];
                data_temp[5] = jsondata[i]['sale_pos'];
                data_temp[6] = jsondata[i]['sale_time'];
                var timedata = new Date();
                timedata.setTime(parseInt(data_temp[6]));
                //alert(parseInt(data_temp[5]));
                data_temp[6] = timedata.toLocaleString();
                data_temp[7] = jsondata[i]['ps_info'];
                //for (var j = 0; j < theTypeIs.length; j++) {
                //    data_temp[j] = jsondata[i][theTypeIs[j]];
                //}
                data_temp[8] = [];
                sales_dataSet[i] = (data_temp);
            }
            //console.log(sales_dataSet);
            if (!sales_tableObj) {
                sales_tableObj = $("#sales_tables").dataTable({
                    "data": [],
                    "fnCreatedRow": function (nRow, aData, iDataIndex) {
                        $('td:eq(' + (8) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-primary' data-toggle='modal' data-target='#Sales_Update_Modal' onclick=salesUpdate(" + iDataIndex + ")>修改</button>");
                        $('td:eq(' + (8) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-danger' onclick=removeSalesRecords(" + iDataIndex + ")>删除</button>");
                    },
                    "columns": [
                        {"title": "序号"},
                        {"title": "名称"},
                        {"title": "类型"},
                        {"title": "编号"},
                        {"title": "售价"},
                        {"title": "分店号"},
                        {"title": "销售时间"},
                        {"title": "备注"},
                        {"title": "操作"}
                    ]
                });
                if (sales_dataSet.length > 0) {
                    sales_tableObj.fnAddData(sales_dataSet);
                }
            }
            else {
                sales_tableObj.fnClearTable();
                if (sales_dataSet.length > 0) {
                    sales_tableObj.fnAddData(sales_dataSet);
                }
                //console.log();
            }
        }
    });
}

function remainsUpdate(data_index) {
    //var msgText = "";
    //var updateTitles = ["名称", "类型", "分店号", "剩余量"];
    //var ids = ["item_name", 'item_type', 'sale_pos', 'remains'];
    //theTypeIs = Object.keys(jsondata[0]);
    //$("#modal_text").html("修改为：<br>" + msgText);
    //for (var j = 0; j < ids.length; j++) {
    //    var inputHtml = "<input class=\"form-control\" type=\"text\" placeholder=\"Inactive\" value=" + remains_dataSet[data_index][j] + "></input>";
    //    msgText += "<span>" + updateTitles[j] + "</span>" + inputHtml;
    //}
    var dataID = jsondata[data_index]['record_id'];
    //alert(dataID);
    $("#remains_itemname").val(remains_dataSet[data_index][1]);
    $("#remains_itemtype").val(remains_dataSet[data_index][2]);
    $("#remains_itemid").val(remains_dataSet[data_index][3]);
    $("#remains_salepos").val(remains_dataSet[data_index][4]);
    $("#remains_count").val(remains_dataSet[data_index][5]);
    $("#btn_submit_remainsUpdate").one('click', function () {
        var post_data = {
            'remains': $("#remains_count").val(), 'item_type': $("#remains_itemtype").val(),
            'item_name': $("#remains_itemname").val(), 'item_id': $("#remains_itemid").val(), 'sale_pos': $("#remains_salepos").val(), 'record_id': dataID
        };
        $.post("/data/RemainsRecords/update", post_data, function (data) {
            alert(data);
            $("#Remains_Update_Modal").modal('toggle');
            loadRemainsData('RemainsRecords');
        });
    });

}

function salesUpdate(data_index) {
    //var updateTitles = [ "名称", "类型", "售价" , "分店号", "销售时间"];
    //var ids = ["item_name", 'item_type', 'price', 'sale_pos', 'sale_time'];
    //theTypeIs = Object.keys(jsondata[0]);
    //for (var j = 0; j < ids.length; j++) {
    //    var inputHtml = "<input class=\"form-control\" type=\"text\" placeholder=\"Inactive\" value=" + sales_dataSet[data_index][j] + "></input>";
    //    msgText += "<span>" + updateTitles[j] + "</span>" + inputHtml;
    //}
    //$("#modal_text").html("修改为：<br>" + msgText);

    var dataID = jsondata[data_index]['record_id'];
    //alert(dataID);
    $("#sales_itemname").val(sales_dataSet[data_index][1]);
    $("#sales_itemtype").val(sales_dataSet[data_index][2]);
    $("#sales_itemid").val(sales_dataSet[data_index][2]);
    $("#sales_price").val(sales_dataSet[data_index][3]);
    $("#sales_salepos").val(sales_dataSet[data_index][4]);
    $("#sales_time").val(sales_dataSet[data_index][5]);
    $("#sales_ps_info").val(sales_dataSet[data_index][7]);

    $("#btn_submit_salesUpdate").one('click', function () {
        var post_data = {
            'item_type': $("#sales_itemtype").val(), 'item_name': $("#sales_itemname").val(),
            'item_id':$("#sales_itemid").val(),'ps_info':$("#sales_ps_info").val(),
            'price': $("#sales_price").val(), 'sale_pos': $("#sales_salepos").val(),
            'sale_time': $("#sales_time").val(), 'record_id': dataID
        };
        $.post("/data/SalesRecords/update", post_data, function (data) {
            alert(data);
            $("#Sales_Update_Modal").modal('toggle');
            loadSalesData('SalesRecords');
        });
    });

}

/*function onClickSalesUpdate() {
 var post_data = {'item_type': $("#sales_itemtype").val(), 'item_name': $("#sales_itemname").val(),
 'price': $("#sales_price").val(), 'sale_pos': $("#sales_salepos").val(),
 'sale_time': $("#sales_time").val(), 'record_id': dataID};
 $.post("/data/SalesRecords/update", post_data, function () {
 alert('修改成功！');
 $("#Sales_Update_Modal").modal('toggle');
 loadSalesData('SalesRecords');
 });
 }*/


function alertTable(tableName) {
    if (tableName == "RemainsRecords") {
        //增加库存记录
        $("#modal_content").html(
            "<div class='modal-header'>\
                <button type='button' class='close'\
                data-dismiss='modal' aria-hidden='true'>\
                &times;\
                </button>\
                <h4 class='modal-title'>\
                注意！增加库存记录：\
                </h4>\
            </div>\
            <div class='modal-body' id='modal_text'>\
                <span>名称</span>\
                <input class='form-control' type='text' placeholder='输入商品名称' id='alert_itemname'>\
                <span>类型</span>\
                <input class='form-control' type='text' placeholder='输入商品类型' id='alert_itemtype'>\
                <span>编号</span>\
                <input class='form-control' type='text' placeholder='输入商品编号' id='alert_itemid'>\
                <span>分店号</span>\
                <input class='form-control' type='text' disabled='disabled' placeholder='输入商品存放店号' id='alert_salepos'>\
                <span>剩余量</span>\
                <input class='form-control' type='text' placeholder='输入剩余量' id='alert_count'>\
            </div>\
            <div class='modal-footer'>\
                <button type='button' class='btn btn-default'\
                     data-dismiss='modal'>关闭\
                </button>\
                <button type='button' id='btn_submit_salesUpdate' class='btn btn-primary'\
                     onclick='onClickAlertRemainsUpdate()'>\
                     提交更改\
                </button>\
            </div>"
        );
    } else {//增加销售记录
        $("#modal_content").html(
            "<div class='modal-header'>\
                <button type='button' class='close'\
                data-dismiss='modal' aria-hidden='true'>\
                &times;\
                </button>\
                <h4 class='modal-title'>\
                注意！增加销售记录：\
                </h4>\
            </div>\
            <div class='modal-body' id='modal_text'>\
                <span>名称</span>\
                <input class='form-control' type='text' placeholder='输入商品名称' id='alert_itemname'>\
                <span>类型</span>\
                <input class='form-control' type='text' placeholder='输入商品类型' id='alert_itemtype'>\
                <span>编号</span>\
                <input class='form-control' type='text' placeholder='输入商品编号' id='alert_itemid'>\
                <span>售价</span>\
                <input class='form-control' type='text' placeholder='输入价格' id='alert_price'>\
                <span>备注</span>\
                <input class='form-control' type='text' placeholder='输入备注' id='alert_ps_info'>\
                <span>分店号</span>\
                <input class='form-control' type='text'  disabled='disabled' placeholder='输入销售分店号' id='alert_salepos'>\
            </div>\
            <div class='modal-footer'>\
                <button type='button' class='btn btn-default'\
                     data-dismiss='modal'>关闭\
                </button>\
                <button type='button' id='btn_submit_salesUpdate' class='btn btn-primary'\
                     onclick='onClickAlertSalesUpdate()'>\
                     提交更改\
                </button>\
            </div>"
        );
    }
    $('#alert_salepos').val(pos);
}


function onClickAlertRemainsUpdate() {
    var alertData = {
        'item_type': $("#alert_itemtype").val(),
        'item_name': $("#alert_itemname").val(),
        'sale_pos': $("#alert_salepos").val(),
        'remains': $("#alert_count").val(),
        'item_id': $("#alert_itemid").val()
    };
    $.post('/data/RemainsRecords/alert', alertData, function (data, status) {
        alert("添加成功！");
        $("#Alert_Modal").modal('toggle');
        loadRemainsData('RemainsRecords');
    });
}

function onClickAlertSalesUpdate() {
    var alertData = {
        'item_type': $("#alert_itemtype").val(),
        'item_name': $("#alert_itemname").val(),
        'item_id': $("#alert_itemid").val(),
        'sale_pos': $("#alert_salepos").val(),
        'price': $("#alert_price").val(),
        'ps_info': $("#alert_ps_info").val(),
        'sale_time': new Date().getTime(),
        'remains': $("#alert_count").val()
    };
    //alert(alertData.sale_time);
    $.post('/data/SalesRecords/alert', alertData, function (data, status) {
        alert(data);
        $("#Alert_Modal").modal('toggle');
        loadSalesData('SalesRecords');
    });
}

function removeSalesRecords(data_index) {
    var record_id = jsondata[data_index]['record_id'];
    var isDelete = confirm("是否删除ID为  " + record_id + "  的记录");
    if (isDelete) {
        $.post('/data/SalesRecords/remove', {'record_id': record_id}, function (data, status) {
                alert('删除成功！');
//        $("#Alert_Modal").modal('toggle');
                loadSalesData('SalesRecords');
            }
        );
    }
}

function removeRemainsRecords(data_index) {
    var record_id = jsondata[data_index]['record_id'];

    var isDelete = confirm("是否删除ID为  " + record_id + "  的记录");
    if (isDelete) {
        $.post('/data/RemainsRecords/remove', {'record_id': record_id}, function (data, status) {
                alert('删除成功！');
//        $("#Alert_Modal").modal('toggle');
                loadRemainsData('RemainsRecords');
            }
        );
    }

}

function exportCSV() {
    var timestamp = Date.now();
    if (currentTable == 'RemainsRecords') {
        if (confirm("导出库存记录表格？")) {
            $.post('/data/RemainsRecords', {'timestamp': timestamp}, function () {
                window.location.href = '/static/csvfiles/' + timestamp + '.csv';
            })
        }
    } else if (currentTable == 'SalesRecords') {
        if (confirm("导出销售记录表格？")) {
            $.post('/data/SalesRecords', {'timestamp': timestamp}, function () {
                window.location.href = '/static/csvfiles/' + timestamp + '.csv';
            })
        }
    }
}