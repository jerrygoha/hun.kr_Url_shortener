$(function() {
	"use strict";
	 $('#submitButton').click(function () {
	 	var isUrl = checkUrlValid($('#url').val());
	 	if (isUrl) {
			$.ajax({
				type: "POST",
				url: "/shorten/",
				data: {
					'url': $('#url').val(),
					'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
				},
				success: returnSuccess,
				dataType: 'json'
			});
		}else{
	 		$('#url-result').text("잘못 입력하셨습니다. 정상적인 url을 입력해주세요.");
		}
	 });

	 // 결과 출력
	function returnSuccess(data, textStatus, jqXHR) {
        if (data.url) {
            $('#url-result').text(data.url);
            $('#url').val("");
        }
    }

    // url 유효성 검사
	function checkUrlValid(input){
	 	var input_url = input;
	 	var UrlCheck = /((\w+)[.])+(asia|biz|cc|cn|com|de|eu|in|info|jobs|jp|kr|mobi|mx|name|net|nz|org|travel|tv|tw|uk|us)(\/(\S*))*$/i;
	 	var urlTest = UrlCheck.test(input_url);

	 	return urlTest;
	};

		var	$body = document.querySelector('body');
			// Methods/polyfills.
		// classList | (c) @remy | github.com/remy/polyfills | rem.mit-license.org
			!function(){function t(t){this.el=t;for(var n=t.className.replace(/^\s+|\s+$/g,"").split(/\s+/),i=0;i<n.length;i++)e.call(this,n[i])}function n(t,n,i){Object.defineProperty?Object.defineProperty(t,n,{get:i}):t.__defineGetter__(n,i)}if(!("undefined"==typeof window.Element||"classList"in document.documentElement)){var i=Array.prototype,e=i.push,s=i.splice,o=i.join;t.prototype={add:function(t){this.contains(t)||(e.call(this,t),this.el.className=this.toString())},contains:function(t){return-1!=this.el.className.indexOf(t)},item:function(t){return this[t]||null},remove:function(t){if(this.contains(t)){for(var n=0;n<this.length&&this[n]!=t;n++);s.call(this,n,1),this.el.className=this.toString()}},toString:function(){return o.call(this," ")},toggle:function(t){return this.contains(t)?this.remove(t):this.add(t),this.contains(t)}},window.DOMTokenList=t,n(Element.prototype,"classList",function(){return new t(this)})}}();
		// canUse
			window.canUse=function(p){if(!window._canUse)window._canUse=document.createElement("div");var e=window._canUse.style,up=p.charAt(0).toUpperCase()+p.slice(1);return p in e||"Moz"+up in e||"Webkit"+up in e||"O"+up in e||"ms"+up in e};
		// window.addEventListener
			(function(){if("addEventListener"in window)return;window.addEventListener=function(type,f){window.attachEvent("on"+type,f)}})();

	// 페이드인 애니메이션
		window.addEventListener('load', function() {
			window.setTimeout(function() {
				$body.classList.remove('is-preload');
			}, 100);
		});

	// 배경화면 전환
		(function() {
			// Settings.
				var settings = {
					// Images (in the format of 'url': 'alignment').
						images: {
							'static/images/bg01.jpg': 'center',
							'static/images/bg02.jpg': 'center',
							'static/images/bg03.jpg': 'center'
						},
					// Delay.
						delay: 4000
				};
			// Vars.
				var	pos = 0, lastPos = 0,
					$wrapper, $bgs = [], $bg,
					k, v;

			// Create BG wrapper, BGs.
				$wrapper = document.createElement('div');
					$wrapper.id = 'bg';
					$body.appendChild($wrapper);

				for (k in settings.images) {
					// Create BG.
						$bg = document.createElement('div');
							$bg.style.backgroundImage = 'url("' + k + '")';
							$bg.style.backgroundPosition = settings.images[k];
							$wrapper.appendChild($bg);

					// Add it to array.
						$bgs.push($bg);
				}

			// Main loop.
				$bgs[pos].classList.add('visible');
				$bgs[pos].classList.add('top');

				// Bail if we only have a single BG or the client doesn't support transitions.
					if ($bgs.length == 1
					||	!canUse('transition'))
						return;

				window.setInterval(function() {
					lastPos = pos;
					pos++;
					// Wrap to beginning if necessary.
						if (pos >= $bgs.length)
							pos = 0;

					// Swap top images.
						$bgs[lastPos].classList.remove('top');
						$bgs[pos].classList.add('visible');
						$bgs[pos].classList.add('top');

					// Hide last image after a short delay.
						window.setTimeout(function() {
							$bgs[lastPos].classList.remove('visible');
						}, settings.delay / 2);
				}, settings.delay);

		})();

	// Shortener Form.
		(function() {
			// Vars.
				var $form = document.querySelectorAll('#shortener-form')[0],
					$submit = document.querySelectorAll('#shortener-form input[type="submit"]')[0],
					$message;

			// Bail if addEventListener isn't supported.
				if (!('addEventListener' in $form))
					return;

			// Message.
				$message = document.createElement('span');
					$message.classList.add('message');
					$form.appendChild($message);

				$message._show = function(type, text) {

					$message.innerHTML = text;
					$message.classList.add(type);
					$message.classList.add('visible');

					window.setTimeout(function() {
						$message._hide();
					}, 3000);

				};

				$message._hide = function() {
					$message.classList.remove('visible');
				};

			// Events.
				$form.addEventListener('submit', function(event) {
					event.stopPropagation();
					event.preventDefault();
					// Hide message.
						$message._hide();
					// Disable submit.
						$submit.disabled = true;
					// Process form.
						window.setTimeout(function() {
							// Reset form.
								$form.reset();
							// Enable submit.
								$submit.disabled = false;
							// Show message.
								$message._show('success', 'Done!');
						}, 750);
				});
		})();
})();