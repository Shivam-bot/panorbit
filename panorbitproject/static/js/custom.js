var baseurl = window.location.origin;


function  myFunction() {
  let text = document.getElementById("search-input").value;
  search_url = baseurl+"/get_search_result"
  	var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
    var select_Html = ""
  $.post("/get_search_result", { csrfmiddlewaretoken: csrfmiddlewaretoken, search_text: text })
  .done(function (response){
              Object.keys(response).forEach(function(key) {
                 response[key].forEach((
                name, index
                )=> {
               select_Html += '<option value='+ name[0].replaceAll(" ","_") + ','+key.replaceAll(" ", "_" )+'>'+ name[0] + '        ' + key +'</option>'
                ;});
            });
          response_length = Object.keys(response).length;


  document.getElementById("search_result").innerHTML = "<select  name=search id=reg_search onchange=fetchDataAll()>" + select_Html + "</select>";

  })

}





function fetchDataAll(){

  	var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

            var selectedValue = reg_search.options[reg_search.selectedIndex].value;

            var selectedValueArray = selectedValue.split(",");
            let data = new Object();
            data["name"] = selectedValueArray[0].replaceAll("_", " ")
            data["search_for"] = selectedValueArray[1].replaceAll("_", " ")
            data["csrfmiddlewaretoken"]= csrfmiddlewaretoken

            $.post("/search_value", data).done( function (response){
            let countryData = response["country_data"]
            let head_array = response["head"]
            var parent = document.getElementById("parent_search")
            parent.style = 'display:none'
            var table_div = document.getElementById('table-content');
            var table_html = '<table class="table table-bordered table-responsive">'
            var table_head = '<thead class="table-secondary"><tr>'
            var table_body ='<tbody>'
            head_array.forEach((head) =>{
            table_head += '<th scope="col">'+ head + '</th>'
            })
            Object.keys(countryData).forEach(function(key){
            let data1 = countryData[key]

            Object.keys(data1).forEach(function(key){

            data1[key].forEach((asd)=> {
            let countryName = asd["country_name"]
            let languageName = ""
            let official = ""
            let percentage = ""

            let cityArray = asd["city"]
            let languageArray = asd["language"]
            languageArray.forEach((lng)=> {
            languageName += lng["language"] + ","
            official +=lng["official"] + ","
            percentage +=lng["language_percentage"] + ","
            });
            cityArray.forEach((city)=>{
            table_body += '<tr><td><a href = # onclick =fetchData('+countryName.replaceAll(" ", "_")+',country' +') >'+countryName +'</td>' +  '<td>' + city["city_name"] +'</td>' + '<td>' + city["district"] +'</td>'+ '<td>' + city["population"] +'</td>' + '<td>' + languageName +'</td>'+ '<td>' + official +'</td>' +  '<td>' + percentage +'</td></tr>'
            });
            table_body += "</tbody>"
            })
            })
            })
            table_head += '</tr></thead>'
            table_html += table_head +table_body+ '</table>'
            table_div.innerHTML = table_html;
            });

}


function fetchData(name, search_for){

  	    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();


            let data = new Object();
            data["name"] = name.replaceAll("_", " ")
            data["search_for"] = search_for.replaceAll("_", " ")

            $.post("/search_value", data).done( function (response){
            let countryData = response["country_data"]
            let head_array = response["head"]
            var parent = document.getElementById("parent_search")
            parent.style = 'display:none'
            var table_div = document.getElementById('table-content');
            var table_html = '<table class="table table-bordered table-responsive">'
            var table_head = '<thead class="table-secondary"><tr>'
            var table_body ='<tbody>'
            head_array.forEach((head) =>{
            table_head += '<th scope="col">'+ head + '</th>'
            })
            Object.keys(countryData).forEach(function(key){
            let data1 = countryData[key]

            Object.keys(data1).forEach(function(key){

            data1[key].forEach((asd)=> {
            let countryName = asd["country_name"]
            let languageName = ""
            let official = ""
            let percentage = ""

            let cityArray = asd["city"]
            let languageArray = asd["language"]
            languageArray.forEach((lng)=> {
            languageName += lng["language"] + ","
            official +=lng["official"] + ","
            percentage +=lng["language_percentage"] + ","
            });
            cityArray.forEach((city)=>{
            table_body += '<tr><td><a href = # onclick =fetchData('+countryName.replaceAll(" ", "_")+',country' +') >'+countryName +'</a></td>' +  '<td>' + city["city_name"] +'</td>' + '<td>' + city["district"] +'</td>'+ '<td>' + city["population"] +'</td>' + '<td>' + languageName +'</td>'+ '<td>' + official +'</td>' +  '<td>' + percentage +'</td></tr>'
            });
            table_body += "</tbody>"
            })
            })
            })
            table_head += '</tr></thead>'
            table_html += table_head +table_body+ '</table>'
            table_div.innerHTML = table_html;
            });

}
function  searchAll() {
  let text = document.getElementById("search-input").value;
  console.log(text + "text")
  search_url = baseurl+"/get_search_result"
  	var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
    var select_Html = ""

  $.post("/get_search_result", { csrfmiddlewaretoken: csrfmiddlewaretoken, search_text: text })
  .done(function (response){
              Object.keys(response).forEach(function(key) {
                 response[key].forEach((
                name, index
                )=> {
                fetchData(name[0].replaceAll(" ","_"),key.replaceAll(" ", "_" ) )
                ;});
            });
          response_length = Object.keys(response).length;



  })

}