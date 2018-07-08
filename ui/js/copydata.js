document.addEventListener('DOMContentLoaded', function() {
const $ = jQuery;
var atrributes = ["title", "plot", "boxoffice", "genre", 
				  "runtime", "mtc", "imdb", "rotten"]
				  
	function copier(string) {
		var textArea = document.createElement('textarea');
        textArea.value = string;
		document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("Copy");
		textArea.remove();
    }

	function copyText() {
		let randNum, speechSelections, copyAll;
		speechSelections = [
		'ROGER THAT!', 
		'COPIED!', 
		"EXCELLENT CHOICE!", 
		"AS YOU WISH!",
		"It's probably not better than Die Hard, but here you go!"]
		randNum = Math.round(Math.random() * speechSelections.length - 1)
		copyAll = $('.copy-all')
		copyAll.attr("data-copy", speechSelections[randNum]).addClass('show')
		setTimeout(() => { copyAll.removeClass('show') }, 3000)
	}

	$('.link--wrapper').on('click', function() {
		let theData, arrangeRow, processRow;
		theData = $('.datarow', this);			
		arrangeRow = [ atrributes.map( x => theData.data(x)) ]
		processRow = SheetClip.stringify(arrangeRow);
		copier(processRow);
		copyText();
	});

	$('.copy-all').on('click', function() {
		let classFind, arrangeRow, processRow;
		classFind = document.querySelectorAll('.datarow')
		arrangeRow = [];
		classFind.forEach( movie => { 
			arrangeRow.push( atrributes.map( datapoint => movie["dataset"][datapoint] ) ) 
		})
		processRow = SheetClip.stringify(arrangeRow);
		copier(processRow)
		copyText();
	});
}); //end

// function fix() { 
    
//     function copiier(string) {
        
//         var textArea = document.createElement('textarea');
// 		console.log(string)
//         textArea.className += " otherclass"
//         textArea.value = string;
//         document.body.appendChild(textArea);
//         textArea.select();
//         document.execCommand("Copy");
//         textArea.remove();
//     }
    

// 		let theData = $('.data .datarow');
// 		console.log(theData)
//         function attri(str){return theData.data(str);}
//         let row = [
//                 attri('title'),
//                 attri('plot'),
//                 attri('boxoffice'),
//                 attri('genre'),
//                 attri('runtime'),
//                 attri('mtc'),
//                 attri('imdb'),
//                 attri('rotten')
//                             ]
//         let arrangeRow = [row];
//         let processRow = SheetClip.stringify(arrangeRow);
//         copiier(processRow);
        
//   }
    