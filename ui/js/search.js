function grabTitle(queryCommand, query) {
    var dataClass = $(".data")
    var theKey = config["config"]["key"]
    const urlFunc = (type, param) => {
      return `https://www.omdbapi.com/?${type}${param}&apikey=${theKey}`}

    function singleTitleCall(queryType, query) {
      
      $.getJSON(urlFunc(queryType, query), data => {
        let returnedData = Object.keys(data)
        let builder = '<div class="section">'
        dataClass.empty()
        
        let movieObj = {
          "title"   : '', "plot" : '', "boxoffice" : '', "genre" : '',
          "runtime" : '', "imdb" : '', "rotten"    : '', "mtc"   : ''
      }
        var key = movieObj
        returnedData.forEach( i => {
            builder += `<p class="title-data">
                        <strong>${i}:</strong> ${data[i]}
                        </p><hr>`      
          }) 
        builder += '</div>'
        dataClass.append(builder)
      })
    }

    switch(queryCommand) {
      case "title":
        singleTitleCall('t=', query)
        break
      case 'search':
        $.getJSON(urlFunc("s=", query), data => {
          let items = data["Search"]
          
          dataClass.empty()
          
          if (items === undefined)
            dataClass.append('<p>Having trouble? Try a different query!</p>')
           
            items.forEach(i => {          
              var theBuilder = `<div class="section">`
            
            for (x in i) {
              item = i[x]
              switch(x) {
                case "Poster":
                  (item == "N/A") ? 
                    null : theBuilder += `<p style="text-align:center;"><img src=${item}></p>`
                  break
                case "Title":
                    theBuilder += `
                      <div class="year-title-top">
                      <p 
                      style="margin-bottom:0;
                            font-size:2rem;
                            text-align:center;">
                       ${item}
                      </p>`
                      break
                case "Year":
                      theBuilder += `
                      <p style="text-align:center;">
                        ${item} 
                        </p></div>`
                        break
                case "imdbID":
                      theBuilder += `
                      <div class="databuttons">
                      <a 
                        target="_blank"
                        href="https://www.imdb.com/title/${item}">Visit Site</a> 
                      <span 
                        onclick=idSearch("${item}")>Get Data</span>
                      </div>
                      </p>`
                 break
                case "Type":
                  break
                default:
                  theBuilder += `<p><strong>${x}:</strong>${item}</p>`
                  break
          }
        }
            theBuilder += `<hr></div>`
            dataClass.append(theBuilder)
        })
      })
      break
    
    case 'getdata':
        singleTitleCall('i=', query)
        break
  }
}

function idSearch(id) {
  grabTitle('getdata', id)
  document.getElementById("search").value = ''
}

function inputGrabber() {
  let queryType = 'title'
  let apikey = config["config"]["key"]
  let inputValue = document.getElementById("search").value
  if ( apikey === "KEYHERE" || apikey === "")
      alert("API Key Missing!")

  if ($('.searchinput')[0].checked) 
      queryType = 'search'
    
  if (inputValue === "") {
      alert("Name must be filled out")
      return false
  }

  grabTitle(queryType, inputValue)
  inputValue = ""
}