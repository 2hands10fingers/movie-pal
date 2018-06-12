  
  function grabTitle(queryCommand, query) {
    const dataClass = $(".data");
    const theKey = config["config"]["key"]

  function urlFunc(type, param) {
    return "https://www.omdbapi.com/?"+ type + param +"&apikey=" + theKey;
  }

  function singleTitleCall(queryType, query) {
    $.getJSON(urlFunc(queryType, query), function(data){
      let returnedData = Object.keys(data)

      dataClass.empty()
      
      var builder = '<div class="section">'
      for (var i = 0; i < returnedData.length; i++) {
          builder += '<p class="title-data"><strong>' + returnedData[i] + ":</strong> "+ data[returnedData[i]] + '</p><hr>';
      }
      builder += '</div>'
      dataClass.append(builder)
    });
  }

  if (queryCommand === "title") {
    
    singleTitleCall('t=', query);
    

  } else if (queryCommand === 'search') {
      $.getJSON(urlFunc("s=", query), function(data){
        let items = data["Search"];
        
        dataClass.empty();
        

        if (items === undefined) {
          dataClass.append('<p>Having trouble? Try a different query!</p>');
        }
        
        for (var i = 0; i < items.length; i++) {
          var theBuilder = '<div class="section">';  
          
          for (x in items[i]) {

            if (x === "Poster") {
              if (items[i][x] == "N/A") {
                // pass
              } else {
                theBuilder += '<p style="text-align:center;"><img src=' + items[i][x] + '></p>';
              }
                
            } else if (x === "Title")  {
              theBuilder += '<div class="year-title-top"><p style="margin-bottom:0;font-size:2rem;text-align:center;">' 
                         + items[i][x] + '</p>';

            } else if (x === "Year")  {
              theBuilder += '<p style="text-align:center;">' 
                         + items[i][x] + '</p></div>';
            } else if (x === "imdbID")  {
              theBuilder += '<div class="databuttons"><a target="_blank" href="https://www.imdb.com/title/' 
                         + items[i][x] + '" >Visit Site</a> <span onclick=idSearch("'+ items[i][x] +'")>Get Data</span></div></p>';
            } else if (x === "Type")  {
              //pass
            } else {
              theBuilder += '<p><strong>'+ x + ":</strong> "+ items[i][x] + '</p>';
            } 
        }
          
          theBuilder += '<hr></div>';
          dataClass.append(theBuilder);
      }
    });
  } else if (queryCommand === 'getdata') {
      
    singleTitleCall('i=', query);

  }
}


function idSearch(id){
  let x = document.getElementById("search").value;
  let queryType = 'getdata';
  grabTitle(queryType, id);
  x = '';
}

function inputGrabber() {
  let queryType = 'title';
  
  if (config["config"]["key"] === "KEYHERE" || config["config"]["key"] === ""){
    alert("API Key Missing!");
  }

  if ($('.searchinput')[0].checked === true) {
      queryType = 'search'  
    }

    let x = document.getElementById("search").value;
    if (x == "") {
        alert("Name must be filled out");
        return false;
    }
    
      grabTitle(queryType, x);
      x = "";
}