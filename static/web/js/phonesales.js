/**
 * Created by Jayvee on 2015/5/27.
 */
<!-- 获取表格数据 -->
$(document).ready(function () {
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
function loadRemainsData(tablename) {
    $("#sales_div").hide();
    $("#remains_div").show();
    remains_dataSet = [];
    $.get('/data/' + tablename, null, function (data, status) {
        if (status == "success") {
            //document.getElementById("tables").innerHTML = xmlhttp.responseText;
            //var dataSet = [];
            jsondata = eval(data);
            theTypeIs = Object.keys(jsondata[0]);
            for (var i = 0; i < jsondata.length; i++) {
                var data_temp = [];
                data_temp[0] = jsondata[i]['item_name'];
                data_temp[1] = jsondata[i]['item_type'];
                data_temp[2] = jsondata[i]['sale_pos'];
                data_temp[3] = jsondata[i]['remains'];
                //for (var j = 0; j < theTypeIs.length; j++) {
                //    data_temp[j] = jsondata[i][theTypeIs[j]];
                //}
                data_temp[4] = [];
                remains_dataSet[i] = (data_temp);
            }
            console.log(remains_dataSet);
            if (!remains_tableObj) {
                remains_tableObj = $("#remains_tables").dataTable({
                    "data": [],
                    "fnCreatedRow": function (nRow, aData, iDataIndex) {
                        $('td:eq(' + (4) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-primary' data-toggle='modal' data-target='#Remains_Update_Modal' onclick=remainsUpdate(" + iDataIndex + ")>修改</button>");
                        $('td:eq(' + (4) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-danger' onclick=rowclick(" + iDataIndex + ")>删除</button>");
                    },
                    "columns": [
                        { "title": "名称" },
                        { "title": "类型" },
                        { "title": "分店号" },
                        { "title": "剩余量"},
                        {"title": "操作"}
                    ]
                });
                remains_tableObj.fnAddData(remains_dataSet);
            }
            else {
                remains_tableObj.fnClearTable();
                remains_tableObj.fnAddData(remains_dataSet);
                //console.log();
            }
        }
    });
}

function loadSalesData(tablename) {
    $("#sales_div").show();
    $("#remains_div").hide();
    sales_dataSet = [];
    $.get('/data/' + tablename, null, function (data, status) {
        if (status == "success") {
            //document.getElementById("tables").innerHTML = xmlhttp.responseText;
            //var dataSet = [];
            jsondata = eval(data);
            theTypeIs = Object.keys(jsondata[0]);
            for (var i = 0; i < jsondata.length; i++) {
                var data_temp = [];
                data_temp[0] = jsondata[i]['item_name'];
                data_temp[1] = jsondata[i]['item_type'];
                data_temp[2] = jsondata[i]['price'];
                data_temp[3] = jsondata[i]['sale_pos'];
                data_temp[4] = jsondata[i]['sale_time'];
                //for (var j = 0; j < theTypeIs.length; j++) {
                //    data_temp[j] = jsondata[i][theTypeIs[j]];
                //}
                data_temp[5] = [];
                sales_dataSet[i] = (data_temp);
            }
            console.log(sales_dataSet);
            if (!sales_tableObj) {
                sales_tableObj = $("#sales_tables").dataTable({
                    "data": [],
                    "fnCreatedRow": function (nRow, aData, iDataIndex) {
                        $('td:eq(' + (5) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-primary' data-toggle='modal' data-target='#Sales_Update_Modal' onclick=salesUpdate(" + iDataIndex + ")>修改</button>");
                        $('td:eq(' + (5) + ')', nRow)
                            .append("<button style ='float:center' class='btn btn-danger' onclick=rowclick(" + iDataIndex + ")>删除</button>");
                    },
                    "columns": [
                        { "title": "名称" },
                        { "title": "类型" },
                        { "title": "售价" },
                        { "title": "分店号"},
                        { "title": "销售时间" },
                        { "title": "操作"}
                    ]
                });
                sales_tableObj.fnAddData(sales_dataSet);
            }
            else {
                sales_tableObj.fnClearTable();
                sales_tableObj.fnAddData(sales_dataSet);
                //console.log();
            }
        }
    });
}

function remainsUpdate(data_index) {
    var msgText = "";
    var updateTitles = ["名称", "类型", "分店号", "剩余量"];
    var ids = ["item_name", 'item_type', 'sale_pos', 'remains'];
    theTypeIs = Object.keys(jsondata[0]);
    //$("#modal_text").html("修改为：<br>" + msgText);
    //for (var j = 0; j < ids.length; j++) {
    //    var inputHtml = "<input class=\"form-control\" type=\"text\" placeholder=\"Inactive\" value=" + remains_dataSet[data_index][j] + "></input>";
    //    msgText += "<span>" + updateTitles[j] + "</span>" + inputHtml;
    //}
    var dataID = jsondata[data_index]['record_id'];
    //alert(dataID);
    $("#remains_itemname").val(remains_dataSet[data_index][0]);
    $("#remains_itemtype").val(remains_dataSet[data_index][1]);
    $("#remains_salepos").val(remains_dataSet[data_index][2]);
    $("#remains_count").val(remains_dataSet[data_index][3]);
    $("#btn_submit_remainsUpdate").one('click', function () {
        var post_data = {'remains': $("#remains_count").val(), 'item_type': $("#remains_itemtype").val(),
            'item_name': $("#remains_itemname").val(), 'sale_pos': $("#remains_salepos").val(), 'record_id': dataID};
        $.post("/data/RemainsRecords/update", post_data, function () {
            alert('修改成功！');
            $("#Remains_Update_Modal").modal('toggle');
            loadRemainsData('RemainsRecords');
        });
    });

}

function salesUpdate(data_index) {
    var updateTitles = [ "名称", "类型", "售价" , "分店号", "销售时间"];
    var ids = ["item_name", 'item_type', 'price', 'sale_pos', 'sale_time'];
    theTypeIs = Object.keys(jsondata[0]);
    //for (var j = 0; j < ids.length; j++) {
    //    var inputHtml = "<input class=\"form-control\" type=\"text\" placeholder=\"Inactive\" value=" + sales_dataSet[data_index][j] + "></input>";
    //    msgText += "<span>" + updateTitles[j] + "</span>" + inputHtml;
    //}
    //$("#modal_text").html("修改为：<br>" + msgText);

    var dataID = jsondata[data_index]['record_id'];
    //alert(dataID);
    $("#sales_itemname").val(sales_dataSet[data_index][0]);
    $("#sales_itemtype").val(sales_dataSet[data_index][1]);
    $("#sales_price").val(sales_dataSet[data_index][2]);
    $("#sales_salepos").val(sales_dataSet[data_index][3]);
    $("#sales_time").val(sales_dataSet[data_index][4]);

    $("#btn_submit_salesUpdate").one('click', function () {
        var post_data = {'item_type': $("#sales_itemtype").val(), 'item_name': $("#sales_itemname").val(),
            'price': $("#sales_price").val(), 'sale_pos': $("#sales_salepos").val(),
            'sale_time': $("#sales_time").val(), 'record_id': dataID};
        $.post("/data/SalesRecords/update", post_data, function () {
            alert('修改成功！');
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
