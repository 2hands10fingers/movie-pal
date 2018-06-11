document.addEventListener('DOMContentLoaded', function() {
const $ = jQuery;

	function log(string){ console.log(string); }

	function copier(string) {
		var textArea = document.createElement("textarea");
		textArea.value = string;
		document.body.appendChild(textArea);
		textArea.select();
		document.execCommand("Copy");
		textArea.remove();
	}

	function copyText() {

		randNum = Math.round(Math.random() * 1)

		if (randNum === 1) {
			log('YES');
			$('.copy-all').addClass('show');
			setTimeout(function(){$('.copy-all').removeClass('show')}, 3000);
		} else {
			$('.copy-all').addClass('show-two');
			setTimeout(function(){$('.copy-all').removeClass('show-two')}, 3000);
		}
		
	}

	$('.link--wrapper').click(function(){
		let theData = $('.datarow', this);
		
		function attri(str){return theData.data(str);}
		let row = [
				 attri('title'),
				 attri('plot'),
				 attri('boxoffice'),
				 attri('genre'),
				 attri('runtime'),
				 attri('mtc'),
				 attri('imdb'),
				 attri('rotten')
							]
		let arrangeRow = [row];
		let processRow = SheetClip.stringify(arrangeRow);
		
		copier(processRow);
		copyText();

	});

	$('.copy-all').click(function(){
		let classFind = document.getElementsByClassName('datarow')
		let arrangeRow = [];

		for (var i = classFind.length - 1; i >= 0; i--) {
			movie = classFind[i]["dataset"];
			row = [	
					movie["title"],
					movie["plot"],
					movie["boxoffice"],
					movie["genre"],
					movie["runtime"],
					movie["mtc"],
					movie["imdb"],
					movie["rotten"]
				  ];
			
			arrangeRow.push(row);

		let processRow = SheetClip.stringify(arrangeRow);
		
		copier(processRow)
		copyText();

		}
	});

}); //end
