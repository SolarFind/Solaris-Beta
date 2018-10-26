// swal("ALL IS OK!", "JSTEST");
$.getJSON("http://alphase.ru:8121/search?s=hello&p=1", function(res){
    console.log(res);

    var name;
    var url;
    var desc;
    var yvod;
    
    for (var i = 0; i < res.data.length; i++) {
        
        name = res.data[i][0];
        url = res.data[i][1];
        desc = res.data[i][2];
        //console.log(name);
        yvod = $('<div class="search_element"></div>');
        // Do smth,
        yvod.append('<a href="'+url+'">'+name+"&nbsp</a>");
        yvod.append('<p>'+desc+'&nbsp</p>');
        // after:
        console.log(yvod);
        yvod.appendTo('#search-results');
        yvod.after("<br>");
    }
    
});